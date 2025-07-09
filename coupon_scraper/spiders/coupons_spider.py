import scrapy
import re
from datetime import datetime
from urllib.parse import urljoin
from coupon_scraper.items import CouponItem


class CouponsSpider(scrapy.Spider):
    name = 'coupons'
    allowed_domains = ['coupons.com', 'retailmenot.com']
    start_urls = [
        'https://www.coupons.com/',
        'https://www.coupons.com/coupon-codes/',
        'https://www.coupons.com/printable-coupons/',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ROBOTSTXT_OBEY': True,
    }

    def parse(self, response):
        """Parse the main coupon listing pages"""
        self.logger.info(f'Parsing: {response.url}')
        
        if 'coupons.com' in response.url:
            yield from self.parse_coupons_com(response)
        elif 'retailmenot.com' in response.url:
            yield from self.parse_retailmenot(response)
    
    def parse_coupons_com(self, response):
        """Parse Coupons.com pages with updated selectors"""
        self.logger.info(f'Parsing Coupons.com: {response.url}')
        
        # Modern coupons.com selectors based on actual site structure
        coupon_selectors = [
            '[data-testid="coupon-card"]',
            '.coupon-card',
            '.offer-card',
            '.deal-card',
            '.coupon-item',
            '[class*="coupon"]',
            '[class*="offer"]'
        ]
        
        coupons = []
        for selector in coupon_selectors:
            found_coupons = response.css(selector)
            if found_coupons:
                coupons = found_coupons
                self.logger.info(f'Found {len(coupons)} coupons using selector: {selector}')
                break
        
        if not coupons:
            # Fallback: look for any card-like elements
            coupons = response.css('[class*="card"], .item, [class*="tile"]')
            self.logger.info(f'Using fallback selector, found {len(coupons)} potential coupons')
        
        for i, coupon in enumerate(coupons[:25]):  # Limit to 25 for testing
            try:
                item = self.extract_coupon_data(coupon, response.url, 'coupons.com')
                if item and item.get('title'):
                    yield item
                    
            except Exception as e:
                self.logger.warning(f'Error parsing coupon {i}: {e}')
                continue
        
        # Look for pagination or "load more" links
        next_page_selectors = [
            'a[aria-label="Next"]::attr(href)',
            '.pagination .next::attr(href)',
            '[data-testid="next-page"]::attr(href)',
            'a:contains("Next")::attr(href)',
            'a:contains("More")::attr(href)'
        ]
        
        for selector in next_page_selectors:
            next_page = response.css(selector).get()
            if next_page:
                yield response.follow(next_page, self.parse)
                break
    
    def parse_retailmenot(self, response):
        """Parse RetailMeNot coupon pages"""
        # Look for coupon cards/containers
        coupon_selectors = [
            '.offer-card',
            '.coupon-card',
            '.deal-card',
            '[data-testid="offer-card"]'
        ]
        
        coupons = []
        for selector in coupon_selectors:
            coupons.extend(response.css(selector))
            if coupons:
                break
        
        for coupon in coupons[:20]:  # Limit to first 20 for demo
            item = CouponItem()
            
            # Extract title
            title_selectors = [
                '.offer-title::text',
                '.coupon-title::text', 
                '.deal-title::text',
                'h3::text',
                'h2::text'
            ]
            title = self.extract_first_text(coupon, title_selectors)
            if not title:
                continue
                
            item['title'] = title.strip()
            
            # Extract coupon code
            code_selectors = [
                '.coupon-code::text',
                '.promo-code::text',
                '[data-clipboard-text]::attr(data-clipboard-text)',
                '.code::text'
            ]
            code = self.extract_first_text(coupon, code_selectors)
            if code:
                item['code'] = code.strip()
            
            # Extract description
            desc_selectors = [
                '.offer-description::text',
                '.coupon-description::text',
                '.deal-description::text',
                'p::text'
            ]
            description = self.extract_first_text(coupon, desc_selectors)
            if description:
                item['description'] = description.strip()
            
            # Extract store/brand
            store_selectors = [
                '.store-name::text',
                '.brand-name::text',
                '.merchant-name::text'
            ]
            store = self.extract_first_text(coupon, store_selectors)
            if store:
                item['store'] = store.strip()
            
            # Extract expiry date
            expiry_selectors = [
                '.expiry-date::text',
                '.expires::text',
                '[data-expiry]::attr(data-expiry)'
            ]
            expiry = self.extract_first_text(coupon, expiry_selectors)
            if expiry:
                item['expiry_date'] = expiry.strip()
            
            item['url'] = response.url
            item['category'] = 'general'
            
            yield item
    
    def extract_coupon_data(self, coupon_element, source_url, site_name):
        """Enhanced method to extract coupon data from various selectors"""
        item = CouponItem()
        
        # Extract title with multiple fallback selectors
        title_selectors = [
            '[data-testid="coupon-title"]::text',
            '.coupon-title::text',
            '.offer-title::text',
            '.title::text',
            'h1::text', 'h2::text', 'h3::text', 'h4::text',
            '.headline::text',
            '[class*="title"]::text',
            'strong::text',
            'b::text'
        ]
        
        title = self.extract_first_text(coupon_element, title_selectors)
        if not title or len(title.strip()) < 3:
            return None
        
        item['title'] = title.strip()
        
        # Extract coupon code
        code_selectors = [
            '[data-testid="coupon-code"]::text',
            '.coupon-code::text',
            '.promo-code::text',
            '.code::text',
            '[data-clipboard-text]::attr(data-clipboard-text)',
            '[class*="code"]::text',
            'code::text'
        ]
        
        code = self.extract_first_text(coupon_element, code_selectors)
        if code:
            # Clean up the code
            clean_code = re.sub(r'[^\w\d]', '', code.strip().upper())
            if clean_code and len(clean_code) >= 3:
                item['code'] = clean_code
        
        # Extract description
        description_selectors = [
            '[data-testid="coupon-description"]::text',
            '.coupon-description::text',
            '.offer-description::text',
            '.description::text',
            'p::text',
            '.details::text',
            '[class*="description"]::text'
        ]
        
        description = self.extract_first_text(coupon_element, description_selectors)
        if description:
            item['description'] = description.strip()
        
        # Extract store/brand
        store_selectors = [
            '[data-testid="store-name"]::text',
            '.store-name::text',
            '.brand-name::text',
            '.merchant-name::text',
            '.store::text',
            '[class*="store"]::text',
            '[class*="brand"]::text'
        ]
        
        store = self.extract_first_text(coupon_element, store_selectors)
        if store:
            item['store'] = store.strip()
        else:
            item['store'] = site_name
        
        # Extract expiry date
        expiry_selectors = [
            '[data-testid="expiry-date"]::text',
            '.expiry-date::text',
            '.expires::text',
            '.expiration::text',
            '[data-expiry]::attr(data-expiry)',
            '[class*="expir"]::text'
        ]
        
        expiry = self.extract_first_text(coupon_element, expiry_selectors)
        if expiry:
            item['expiry_date'] = self.clean_expiry_date(expiry.strip())
        
        # Extract discount percentage
        discount_text = f"{title} {description or ''}"
        percentage = self.extract_discount_percentage(discount_text)
        if percentage:
            item['discount_percentage'] = percentage
        
        # Extract category
        category_selectors = [
            '[data-testid="category"]::text',
            '.category::text',
            '[class*="category"]::text'
        ]
        
        category = self.extract_first_text(coupon_element, category_selectors)
        if category:
            item['category'] = category.strip().lower()
        else:
            item['category'] = self.guess_category(title, description or '')
        
        # Extract terms and conditions
        terms_selectors = [
            '.terms::text',
            '.conditions::text',
            '.fine-print::text',
            '[class*="terms"]::text'
        ]
        
        terms = self.extract_first_text(coupon_element, terms_selectors)
        if terms:
            item['terms_conditions'] = terms.strip()
        
        item['url'] = source_url
        
        return item
    
    def clean_expiry_date(self, expiry_text):
        """Clean and standardize expiry date format"""
        if not expiry_text:
            return None
        
        # Remove common prefixes
        expiry_text = re.sub(r'^(expires?:?\s*|exp:?\s*|until:?\s*)', '', expiry_text, flags=re.IGNORECASE)
        
        # Look for date patterns
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
            r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, expiry_text)
            if match:
                return match.group()
        
        return expiry_text.strip()
    
    def guess_category(self, title, description):
        """Guess category based on title and description"""
        text = f"{title} {description}".lower()
        
        categories = {
            'clothing': ['clothing', 'apparel', 'fashion', 'dress', 'shirt', 'pants', 'shoes'],
            'food': ['food', 'restaurant', 'dining', 'meal', 'pizza', 'burger'],
            'electronics': ['electronics', 'tech', 'computer', 'phone', 'gadget'],
            'travel': ['travel', 'hotel', 'flight', 'vacation', 'trip'],
            'beauty': ['beauty', 'cosmetics', 'makeup', 'skincare'],
            'home': ['home', 'furniture', 'decor', 'garden'],
            'automotive': ['auto', 'car', 'vehicle', 'automotive']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'general'
    
    def extract_first_text(self, selector_obj, selectors):
        """Helper method to extract first non-empty text from multiple selectors"""
        for selector in selectors:
            try:
                result = selector_obj.css(selector).get()
                if result and result.strip():
                    return result.strip()
            except:
                continue
        return None
    
    def extract_discount_percentage(self, text):
        """Extract discount percentage from text"""
        if not text:
            return None
        
        match = re.search(r'(\d+)%', text)
        if match:
            return int(match.group(1))
        return None


# Alternative spider for demo data
class DemoCouponsSpider(scrapy.Spider):
    name = 'demo_coupons'
    
    def start_requests(self):
        """Generate demo coupon data for testing"""
        demo_data = [
            {
                'title': '20% Off Sitewide',
                'code': 'SAVE20',
                'description': 'Get 20% off your entire order',
                'store': 'Demo Store',
                'expiry_date': '2025-12-31',
                'discount_percentage': 20,
                'category': 'clothing'
            },
            {
                'title': 'Free Shipping on Orders Over $50',
                'code': 'FREESHIP50',
                'description': 'Free shipping when you spend $50 or more',
                'store': 'Demo Store',
                'expiry_date': '2025-11-30',
                'category': 'shipping'
            },
            {
                'title': 'Buy 2 Get 1 Free',
                'code': 'BUY2GET1',
                'description': 'Buy any 2 items and get the 3rd free',
                'store': 'Demo Electronics',
                'expiry_date': '2025-10-15',
                'category': 'electronics'
            }
        ]
        
        for data in demo_data:
            item = CouponItem()
            for key, value in data.items():
                item[key] = value
            item['url'] = 'https://demo.example.com'
            yield item
