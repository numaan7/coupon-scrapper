import re
from datetime import datetime
from scrapy.exceptions import DropItem
try:
    from itemadapter import ItemAdapter
except ImportError:
    # Fallback for older Scrapy versions
    class ItemAdapter:
        def __init__(self, item):
            self.item = item
        
        def get(self, key, default=None):
            return self.item.get(key, default)
        
        def __setitem__(self, key, value):
            self.item[key] = value


class CouponValidationPipeline:
    """Pipeline to validate coupon data"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Validate required fields
        if not adapter.get('title'):
            spider.logger.warning(f"Missing title for item: {item}")
            return item
            
        # Clean and validate coupon code
        code = adapter.get('code', '')
        if code:
            # Remove extra whitespace and convert to uppercase
            adapter['code'] = re.sub(r'\s+', '', code).upper()
        
        # Validate and format expiry date
        expiry = adapter.get('expiry_date')
        if expiry:
            try:
                # Try to parse common date formats
                if isinstance(expiry, str):
                    # Add more date parsing logic as needed
                    adapter['expiry_date'] = expiry.strip()
            except Exception as e:
                spider.logger.warning(f"Could not parse expiry date {expiry}: {e}")
        
        return item


class DuplicatesPipeline:
    """Pipeline to filter duplicate items"""
    
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Create a unique identifier based on title and code
        title = adapter.get('title', '').strip().lower()
        code = adapter.get('code', '').strip().lower()
        store = adapter.get('store', '').strip().lower()
        
        unique_id = f"{title}:{code}:{store}"
        
        if unique_id in self.ids_seen:
            spider.logger.info(f"Duplicate item found: {unique_id}")
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.ids_seen.add(unique_id)
            return item


class CleanDataPipeline:
    """Pipeline to clean and format data"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Clean title
        title = adapter.get('title', '')
        if title:
            adapter['title'] = ' '.join(title.split())
        
        # Clean description
        description = adapter.get('description', '')
        if description:
            adapter['description'] = ' '.join(description.split())
        
        # Extract discount percentage if not present
        if not adapter.get('discount_percentage'):
            title_text = f"{title} {description}".lower()
            percentage_match = re.search(r'(\d+)%', title_text)
            if percentage_match:
                adapter['discount_percentage'] = int(percentage_match.group(1))
        
        return item
