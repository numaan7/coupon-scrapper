import scrapy
import re
from datetime import datetime
from urllib.parse import urljoin
from coupon_scraper.items import CouponItem


class CouponsSpider(scrapy.Spider):
    name = 'coupons'
    allowed_domains = ['retailmenot.com', 'coupons.com', 'groupon.com']
    start_urls = [
        'https://www.retailmenot.com/deals',
        'https://www.coupons.com/coupon-codes',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    }

    def parse(self, response):
        """Parse the main coupon listing pages"""
        self.logger.info(f'Parsing: {response.url}')
        
        if 'retailmenot.com' in response.url:
            yield from self.parse_retailmenot(response)
        elif 'coupons.com' in response.url:
            yield from self.parse_coupons_com(response)
    
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
    
    def parse_coupons_com(self, response):
        """Parse Coupons.com pages"""
        # Similar structure but different selectors
        coupon_selectors = [
            '.coupon-item',
            '.offer-item',
            '.deal-item'
        ]
        
        coupons = []
        for selector in coupon_selectors:
            coupons.extend(response.css(selector))
            if coupons:
                break
        
        for coupon in coupons[:20]:  # Limit for demo
            item = CouponItem()
            
            # Extract basic information
            title = self.extract_first_text(coupon, ['.title::text', 'h3::text', 'h2::text'])
            if not title:
                continue
                
            item['title'] = title.strip()
            
            # Extract other fields similar to RetailMeNot
            code = self.extract_first_text(coupon, ['.code::text', '.promo::text'])
            if code:
                item['code'] = code.strip()
            
            description = self.extract_first_text(coupon, ['.description::text', 'p::text'])
            if description:
                item['description'] = description.strip()
            
            item['url'] = response.url
            item['category'] = 'general'
            
            yield item
    
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
