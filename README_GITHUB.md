# 🎫 Coupon Scraper

[![Test Status](https://github.com/yourusername/coupon-scrapper/workflows/Test%20Coupon%20Scraper/badge.svg)](https://github.com/yourusername/coupon-scrapper/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Scrapy](https://img.shields.io/badge/scrapy-2.5+-green.svg)](https://scrapy.org/)
[![Zyte Ready](https://img.shields.io/badge/zyte-ready-orange.svg)](https://www.zyte.com/)

A powerful, production-ready coupon scraper built with Scrapy and optimized for deployment on Zyte Scrapy Cloud.

## 🚀 Features

- 🕷️ **Scrapy-powered** - Robust, scalable web scraping framework
- ☁️ **Zyte Cloud Ready** - Optimized for Zyte Scrapy Cloud deployment
- 🔄 **Auto-deployment** - GitHub integration for continuous deployment
- 🧹 **Data Cleaning** - Built-in validation and deduplication pipelines
- 🎭 **User Agent Rotation** - Respectful crawling with rotating user agents
- 📊 **Structured Output** - Clean JSON data with comprehensive coupon information
- 🧪 **Test Suite** - Comprehensive testing and validation
- 🐳 **Docker Support** - Containerized deployment option

## 📋 Scraped Data Structure

```json
{
  "title": "20% Off Sitewide",
  "code": "SAVE20",
  "description": "Get 20% off your entire order",
  "expiry_date": "2025-12-31",
  "store": "Example Store",
  "url": "https://example.com/coupon",
  "discount_percentage": 20,
  "category": "clothing",
  "terms_conditions": "Valid on full-price items only",
  "scraped_at": "2025-07-09T10:30:00"
}
```

## 🛠️ Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/coupon-scrapper.git
cd coupon-scrapper

# Install dependencies
pip install -r requirements.txt

# Run the demo spider
scrapy crawl demo_coupons -o demo.json

# Test the scraper
python test_scraper.py
```

### Using the Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

## 🕷️ Usage

### Local Development

```bash
# Run demo spider (generates sample data)
scrapy crawl demo_coupons -o demo_coupons.json

# Run main coupon spider
scrapy crawl coupons -o coupons.json

# Run with custom settings
scrapy crawl coupons -s DOWNLOAD_DELAY=3 -s CONCURRENT_REQUESTS=1
```

### Available Spiders

| Spider | Description | Output |
|--------|-------------|--------|
| `demo_coupons` | Generates sample coupon data for testing | Demo JSON data |
| `coupons` | Scrapes real coupon websites | Real coupon data |

## ☁️ Deployment to Zyte Scrapy Cloud

### Option 1: GitHub Integration (Recommended)

1. **Push to GitHub:**
   ```bash
   git push origin main
   ```

2. **Connect to Zyte:**
   - Go to your [Zyte dashboard](https://app.scrapinghub.com/)
   - Connect your GitHub repository
   - Enable auto-deployment

3. **Deploy:**
   - Automatic deployment on push, or
   - Manual deploy from Zyte dashboard

### Option 2: Direct Deployment

```bash
# Install Zyte tools
pip install shub

# Login to Zyte
shub login

# Deploy
shub deploy
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Zyte Configuration
SCRAPINGHUB_API_KEY=your_api_key
SCRAPINGHUB_PROJECT_ID=your_project_id

# Scraping Settings
DOWNLOAD_DELAY=2
CONCURRENT_REQUESTS=8
USER_AGENT=coupon_scraper (+http://yourdomain.com)
```

### Scrapy Settings

Key settings in `coupon_scraper/settings.py`:

- `DOWNLOAD_DELAY`: Delay between requests
- `CONCURRENT_REQUESTS`: Number of concurrent requests
- `AUTOTHROTTLE_ENABLED`: Automatic throttling
- `ROBOTSTXT_OBEY`: Respect robots.txt

## 🧪 Testing

```bash
# Run test suite
python test_scraper.py

# Test specific spider
scrapy parse --spider=demo_coupons

# Check for errors
scrapy check
```

## 📊 Monitoring & Analytics

- **Zyte Dashboard**: Monitor jobs, logs, and performance
- **Built-in Logging**: Comprehensive logging for debugging
- **Item Statistics**: Track scraped items and success rates
- **Error Handling**: Robust error detection and reporting

## 🛡️ Best Practices

- ✅ Respects `robots.txt` by default
- ✅ Implements polite crawling delays
- ✅ Rotates user agents
- ✅ Handles errors gracefully
- ✅ Validates and cleans data
- ✅ Removes duplicates automatically

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Notice

This scraper is for educational and research purposes. Always:
- Check website terms of service
- Respect robots.txt
- Don't overload servers
- Follow applicable laws and regulations

## 🔗 Links

- [Scrapy Documentation](https://docs.scrapy.org/)
- [Zyte Scrapy Cloud](https://www.zyte.com/scrapy-cloud/)
- [GitHub Actions](https://github.com/features/actions)

## 📞 Support

- 🐛 [Report Issues](https://github.com/yourusername/coupon-scrapper/issues)
- 💡 [Feature Requests](https://github.com/yourusername/coupon-scrapper/issues/new)
- 📖 [Documentation](DEPLOYMENT.md)
