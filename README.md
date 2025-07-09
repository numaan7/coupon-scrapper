# Coupon Scraper

A simple Python coupon scraper built with Scrapy and deployable to Zyte's Scrapy Cloud.

## Features

- Scrapes coupon codes and deals from popular coupon websites
- Built with Scrapy for robust web scraping
- Ready for deployment to Zyte Scrapy Cloud
- Structured data output in JSON format
- Configurable settings and user agents

## Project Structure

```
coupon-scrapper/
├── coupon_scraper/
│   ├── __init__.py
│   ├── items.py          # Data models for scraped items
│   ├── middlewares.py    # Custom middlewares
│   ├── pipelines.py      # Data processing pipelines
│   ├── settings.py       # Scrapy settings
│   └── spiders/
│       ├── __init__.py
│       └── coupons_spider.py  # Main spider
├── scrapy.cfg           # Scrapy configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the spider locally:
```bash
scrapy crawl coupons -o output.json
```

## Deployment to Zyte Scrapy Cloud

1. Install shub (Scrapinghub CLI):
```bash
pip install shub
```

2. Login to your Zyte account:
```bash
shub login
```

3. Deploy the project:
```bash
shub deploy
```

4. Schedule or run the spider on Scrapy Cloud through the web interface.

## Configuration

Edit `coupon_scraper/settings.py` to customize:
- Download delays
- User agents
- Concurrent requests
- Output formats

## Output

The spider outputs JSON with the following structure:
```json
{
  "title": "Coupon Title",
  "code": "SAVE20",
  "description": "20% off all items",
  "expiry_date": "2025-12-31",
  "store": "Example Store",
  "url": "https://example.com/coupon",
  "scraped_at": "2025-07-09T10:30:00"
}
```
