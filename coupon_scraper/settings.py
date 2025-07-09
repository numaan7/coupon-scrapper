BOT_NAME = 'coupon_scraper'

SPIDER_MODULES = ['coupon_scraper.spiders']
NEWSPIDER_MODULE = 'coupon_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure delays for requests (be respectful)
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = 0.5

# Configure concurrent requests (reduced for politeness)
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Enable autothrottling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# User agent
USER_AGENT = 'coupon_scraper (+http://www.yourdomain.com)'

# Configure a list of user agents for rotation
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
]

# Configure pipelines
ITEM_PIPELINES = {
    'coupon_scraper.pipelines.CouponValidationPipeline': 300,
    'coupon_scraper.pipelines.DuplicatesPipeline': 400,
}

# Configure middlewares
DOWNLOADER_MIDDLEWARES = {
    'coupon_scraper.middlewares.RotateUserAgentMiddleware': 400,
}

# Configure caching (disable in production)
HTTPCACHE_ENABLED = False

# Configure logging
LOG_LEVEL = 'INFO'

# Feed settings
FEEDS = {
    'coupons.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,
        'indent': 4,
    },
}
