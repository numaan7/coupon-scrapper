# 🎫 How to Scrape Coupons.com

This guide shows you how to scrape coupons from https://www.coupons.com/ using our specialized spider.

## 🚀 Quick Start

### Method 1: Using the Custom Runner Script (Recommended)

```bash
# Basic scraping - saves to timestamped file
python run_coupons_scraper.py

# Save to specific file
python run_coupons_scraper.py -o my_coupons.json

# Limit to 5 pages
python run_coupons_scraper.py -p 5

# Filter by category (note: this is basic text-based filtering)
python run_coupons_scraper.py -c food
```

### Method 2: Direct Scrapy Commands

```bash
# Run the specialized coupons.com spider
scrapy crawl coupons_com -o coupons_output.json

# Run with custom settings
scrapy crawl coupons_com -o coupons_output.json -s DOWNLOAD_DELAY=5 -s CLOSESPIDER_PAGECOUNT=3

# Run the general coupons spider (includes multiple sites)
scrapy crawl coupons -o general_coupons.json
```

## 🎯 Available Spiders

| Spider Name | Description | Target Sites |
|-------------|-------------|--------------|
| `coupons_com` | Specialized for coupons.com | coupons.com only |
| `coupons` | General coupon spider | coupons.com, retailmenot.com |
| `demo_coupons` | Demo data generator | Generates sample data |

## 📊 Output Data Structure

The scraped data includes:

```json
{
  "title": "20% Off Electronics",
  "code": "SAVE20",
  "description": "Get 20% off all electronics",
  "store": "Best Buy",
  "expiry_date": "2025-12-31",
  "discount_percentage": 20,
  "category": "electronics",
  "terms_conditions": "Valid on orders over $50",
  "url": "https://www.coupons.com/...",
  "scraped_at": "2025-07-09T23:19:39.951281"
}
```

## ⚙️ Customization Options

### Adjust Scraping Speed

Edit `coupon_scraper/settings.py`:

```python
# Slower, more polite scraping
DOWNLOAD_DELAY = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Faster scraping (use carefully)
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 3
```

### Custom User Agents

The spider rotates between multiple user agents automatically. You can add more in `settings.py`:

```python
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    # Add more user agents here
]
```

### Filter by Category

You can filter results after scraping using a simple Python script:

```python
import json

# Load scraped data
with open('coupons_output.json', 'r') as f:
    coupons = json.load(f)

# Filter by category
food_coupons = [c for c in coupons if c.get('category') == 'food']

# Save filtered results
with open('food_coupons.json', 'w') as f:
    json.dump(food_coupons, f, indent=2)
```

## 🛡️ Best Practices

### 1. Respect Rate Limits
```bash
# Use delays between requests
scrapy crawl coupons_com -s DOWNLOAD_DELAY=3
```

### 2. Check robots.txt
```bash
# The spider respects robots.txt by default
# To check manually: curl https://www.coupons.com/robots.txt
```

### 3. Monitor for Changes
```bash
# Test with small samples first
scrapy crawl coupons_com -s CLOSESPIDER_PAGECOUNT=1 -o test.json
```

### 4. Handle Errors Gracefully
```bash
# Enable detailed logging
scrapy crawl coupons_com -L DEBUG -o output.json
```

## 📈 Advanced Usage

### Scrape Specific Categories

Target specific category pages:

```python
# Create a custom spider start_urls
start_urls = [
    'https://www.coupons.com/categories/food',
    'https://www.coupons.com/categories/clothing',
    # Add more category URLs
]
```

### Continuous Monitoring

Set up scheduled scraping:

```bash
# Using cron (Linux/Mac)
# Add to crontab: 0 9 * * * cd /path/to/scraper && python run_coupons_scraper.py

# Using Windows Task Scheduler
# Create a batch file that runs the scraper
```

### Data Processing Pipeline

```python
import json
import pandas as pd

# Load and process data
with open('coupons_output.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame for analysis
df = pd.DataFrame(data)

# Analyze data
print(f"Total coupons: {len(df)}")
print(f"Categories: {df['category'].value_counts()}")
print(f"Average discount: {df['discount_percentage'].mean():.1f}%")

# Export to CSV
df.to_csv('coupons_analysis.csv', index=False)
```

## 🔧 Troubleshooting

### Common Issues

1. **No coupons found**
   - Check if the website structure changed
   - Verify selectors in the spider code
   - Test with `-L DEBUG` for detailed logs

2. **403/404 Errors**
   - Website might be blocking scrapers
   - Try different user agents
   - Increase download delays

3. **Duplicate items**
   - This is normal - the pipeline removes duplicates
   - Check `item_dropped_count` in logs

### Debug Commands

```bash
# Check spider syntax
scrapy check coupons_com

# Test URL parsing without running full spider
scrapy parse --spider=coupons_com https://www.coupons.com/

# View detailed stats
scrapy crawl coupons_com -s LOGSTATS_INTERVAL=10
```

## 📞 Support

- 🐛 Issues with the scraper? Check the logs first
- 🔄 Website changed? You may need to update selectors
- 📚 More examples? Check the `test_scraper.py` file

## ⚠️ Legal Considerations

- ✅ Respect robots.txt (enabled by default)
- ✅ Use reasonable delays between requests
- ✅ Don't overwhelm the server
- ✅ Check website terms of service
- ✅ Use data responsibly

---

Happy scraping! 🕷️
