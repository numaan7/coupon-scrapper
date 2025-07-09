import scrapy
from datetime import datetime


class CouponItem(scrapy.Item):
    """Item class for coupon data"""
    title = scrapy.Field()
    code = scrapy.Field()
    description = scrapy.Field()
    expiry_date = scrapy.Field()
    store = scrapy.Field()
    url = scrapy.Field()
    scraped_at = scrapy.Field()
    discount_percentage = scrapy.Field()
    category = scrapy.Field()
    terms_conditions = scrapy.Field()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['scraped_at'] = datetime.now().isoformat()
