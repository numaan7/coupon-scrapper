import scrapy
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from coupon_scraper.items import CouponItem


class CouponsComSpider(scrapy.Spider):
    name = 'coupons_com'
    allowed_domains = ['coupons.com']
    start_urls = [
        'https://www.coupons.com/',
        'https://www.coupons.com/coupon-codes/',
        'https://www.coupons.com/printable-coupons/',
        'https://www.coupons.com/deals/',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        """Parse coupons.com main pages"""
        self.logger.info(f'Parsing Coupons.com: {response.url}')
        
        # Try multiple selectors that coupons.com might use
        coupon_selectors = [
            # Modern React-based selectors
            '[data-testid*="coupon"]',
            '[data-testid*="offer"]',
            '[data-testid*="deal"]',
            
            # Common CSS class patterns
            '.coupon-card',
            '.offer-card',
            '.deal-card',
            '.coupon-tile',
            '.offer-tile',
            
            # Generic card selectors
            '[class*="card"][class*="coupon"]',
            '[class*="card"][class*="offer"]',
            '[class*="tile"][class*="coupon"]',
            
            # Fallback selectors
            '.coupon',
            '.offer',
            '.deal',
            '[class*="coupon"]',
            '[class*="offer"]'
        ]
        
        found_coupons = []
        working_selector = None
        
        for selector in coupon_selectors:
            coupons = response.css(selector)
            if len(coupons) > 0:
                found_coupons = coupons
                working_selector = selector
                self.logger.info(f'Found {len(coupons)} coupons using selector: {selector}')
                break
        
        if not found_coupons:
            # Last resort: look for any structured content
            found_coupons = response.css('article, .item, [class*="card"], [class*="tile"]')
            self.logger.warning(f'Using fallback selector, found {len(found_coupons)} potential items')
        
        # Extract coupon data
        coupon_count = 0
        for i, coupon in enumerate(found_coupons[:30]):  # Limit to 30 items
            try:
                item = self.extract_coupon_info(coupon, response.url)
                if item and self.is_valid_coupon(item):
                    coupon_count += 1
                    yield item
                    
            except Exception as e:
                self.logger.error(f'Error extracting coupon {i}: {e}')
                continue
        
        self.logger.info(f'Successfully extracted {coupon_count} valid coupons from {response.url}')
        
        # Look for pagination or more content
        yield from self.follow_pagination(response)
    
    def extract_coupon_info(self, coupon_element, source_url):
        """Extract coupon information with comprehensive selectors"""
        item = CouponItem()
        
        # Extract title (most important field)
        title = self.extract_text_from_selectors(coupon_element, [
            '[data-testid*="title"]',
            '[data-testid*="headline"]',
            '.title',
            '.headline',
            '.offer-title',
            '.coupon-title',
            '.deal-title',
            'h1', 'h2', 'h3', 'h4', 'h5',
            '.name',
            '[class*="title"]',
            '[class*="headline"]',
            'strong',
            'b'
        ])
        
        if not title or len(title.strip()) < 5:
            return None
        
        item['title'] = self.clean_text(title)
        
        # Extract coupon code
        code = self.extract_text_from_selectors(coupon_element, [
            '[data-testid*="code"]',
            '.coupon-code',
            '.promo-code',
            '.discount-code',
            '.code',
            '[data-clipboard-text]',
            'code',
            '[class*="code"]'
        ], attr='data-clipboard-text')
        
        if code:
            clean_code = re.sub(r'[^\w\d]', '', code.upper())
            if clean_code and len(clean_code) >= 3:
                item['code'] = clean_code
        
        # Extract description
        description = self.extract_text_from_selectors(coupon_element, [
            '[data-testid*="description"]',
            '.description',
            '.offer-description',
            '.coupon-description',
            '.details',
            '.summary',
            'p',
            '[class*="description"]',
            '[class*="detail"]'
        ])
        
        if description:
            item['description'] = self.clean_text(description)
        
        # Extract store/brand
        store = self.extract_text_from_selectors(coupon_element, [
            '[data-testid*="store"]',
            '[data-testid*="brand"]',
            '.store-name',
            '.brand-name',
            '.merchant',
            '.retailer',
            '.store',
            '.brand',
            '[class*="store"]',
            '[class*="brand"]',
            '[class*="merchant"]'
        ])
        
        if store:
            item['store'] = self.clean_text(store)
        else:
            item['store'] = 'Coupons.com'
        
        # Extract expiry date
        expiry = self.extract_text_from_selectors(coupon_element, [
            '[data-testid*="expir"]',
            '[data-testid*="expire"]',
            '.expiry',
            '.expires',
            '.expiration',
            '.valid-until',
            '[class*="expir"]',
            '[data-expiry]'
        ])
        
        if expiry:
            item['expiry_date'] = self.parse_expiry_date(expiry)
        
        # Extract discount percentage
        all_text = f"{item.get('title', '')} {item.get('description', '')}"
        percentage = self.extract_percentage(all_text)
        if percentage:
            item['discount_percentage'] = percentage
        
        # Set other fields
        item['url'] = source_url
        item['category'] = self.categorize_coupon(all_text)
        
        # Extract terms if available
        terms = self.extract_text_from_selectors(coupon_element, [
            '.terms',
            '.conditions',
            '.restrictions',
            '.fine-print',
            '[class*="terms"]',
            '[class*="condition"]'
        ])
        
        if terms:
            item['terms_conditions'] = self.clean_text(terms)
        
        return item
    
    def extract_text_from_selectors(self, element, selectors, attr=None):
        """Try multiple selectors to extract text"""
        for selector in selectors:
            try:
                if attr:
                    result = element.css(f'{selector}::attr({attr})').get()
                else:
                    result = element.css(f'{selector}::text').get()
                
                if result and result.strip():
                    return result.strip()
            except Exception:
                continue
        return None
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return None
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common prefixes/suffixes
        text = re.sub(r'^(deal|offer|coupon):\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s*(deal|offer|coupon)$', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def parse_expiry_date(self, expiry_text):
        """Parse and clean expiry date"""
        if not expiry_text:
            return None
        
        # Remove common prefixes
        expiry_text = re.sub(r'^(expires?:?\s*|exp:?\s*|valid until:?\s*)', '', expiry_text, flags=re.IGNORECASE)
        
        # Look for date patterns
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
            r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY
            r'\w+ \d{1,2}, \d{4}',     # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, expiry_text)
            if match:
                return match.group()
        
        return expiry_text.strip()
    
    def extract_percentage(self, text):
        """Extract discount percentage from text"""
        if not text:
            return None
        
        # Look for percentage patterns
        percentage_patterns = [
            r'(\d+)%\s*off',
            r'save\s*(\d+)%',
            r'(\d+)%\s*discount',
            r'(\d+)%\s*savings',
            r'(\d+)%'
        ]
        
        for pattern in percentage_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        
        return None
    
    def categorize_coupon(self, text):
        """Categorize coupon based on text content"""
        text = text.lower()
        
        categories = {
            'food': ['food', 'restaurant', 'dining', 'pizza', 'burger', 'meal', 'grocery'],
            'clothing': ['clothing', 'fashion', 'apparel', 'dress', 'shirt', 'shoes', 'style'],
            'electronics': ['electronics', 'tech', 'computer', 'phone', 'gadget', 'software'],
            'travel': ['travel', 'hotel', 'flight', 'vacation', 'trip', 'airline'],
            'beauty': ['beauty', 'cosmetics', 'makeup', 'skincare', 'hair'],
            'home': ['home', 'furniture', 'decor', 'garden', 'kitchen'],
            'automotive': ['auto', 'car', 'vehicle', 'automotive', 'tire'],
            'health': ['health', 'medical', 'pharmacy', 'vitamin', 'fitness']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'general'
    
    def is_valid_coupon(self, item):
        """Validate if the extracted item is a valid coupon"""
        if not item or not item.get('title'):
            return False
        
        title = item['title'].lower()
        
        # Skip if title is too short or generic
        if len(title) < 5:
            return False
        
        # Skip navigation elements, ads, etc.
        skip_keywords = ['menu', 'navigation', 'footer', 'header', 'sidebar', 'advertisement']
        if any(keyword in title for keyword in skip_keywords):
            return False
        
        return True
    
    def follow_pagination(self, response):
        """Follow pagination links"""
        pagination_selectors = [
            'a[aria-label="Next"]::attr(href)',
            '.pagination .next::attr(href)',
            '[data-testid*="next"]::attr(href)',
            'a:contains("Next")::attr(href)',
            'a:contains("More")::attr(href)',
            '.next-page::attr(href)'
        ]
        
        for selector in pagination_selectors:
            next_page = response.css(selector).get()
            if next_page:
                self.logger.info(f'Following pagination: {next_page}')
                yield response.follow(next_page, self.parse)
                break
