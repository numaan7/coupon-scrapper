# Zyte Scrapy Cloud Deployment Guide

## Prerequisites

1. Create a Zyte account at https://app.scrapinghub.com/
2. Create a new project in your Zyte dashboard
3. Get your API key from your account settings

## Setup

1. **Install shub (already done if you ran the setup script):**
   ```bash
   pip install shub
   ```

2. **Configure your credentials:**
   ```bash
   shub login
   ```
   Enter your API key when prompted.

3. **Update scrapy.cfg with your project details:**
   Edit the `scrapy.cfg` file and replace:
   - `YOUR_USERNAME` with your Zyte username
   - `YOUR_API_KEY` with your API key
   - `YOUR_PROJECT_ID` with your project ID from Zyte dashboard

## Deployment

1. **Deploy your spider:**
   ```bash
   shub deploy
   ```

2. **Schedule or run your spider:**
   - Go to your Zyte dashboard
   - Select your project
   - Click "Jobs" > "Schedule"
   - Select your spider (`coupons` or `demo_coupons`)
   - Configure any settings and run

## GitHub Deployment (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial coupon scraper setup"
   git branch -M main
   git remote add origin https://github.com/yourusername/coupon-scrapper.git
   git push -u origin main
   ```

2. **Connect GitHub to Zyte:**
   - Go to your Zyte project dashboard
   - Click "Settings" > "Code & Deploys"
   - Click "Connect to GitHub"
   - Authorize Zyte to access your GitHub account
   - Select your `coupon-scrapper` repository

3. **Configure auto-deployment:**
   - Choose the branch to deploy from (usually `main`)
   - Enable "Auto-deploy on push" for continuous deployment
   - Set up deployment triggers (optional)

4. **Deploy:**
   - Click "Deploy" in the Zyte dashboard, or
   - Push changes to your configured branch for auto-deployment

**Benefits of GitHub deployment:**
- ✅ Version control and change tracking
- ✅ Automatic deployments on code changes
- ✅ Easy collaboration with team members
- ✅ Rollback capabilities
- ✅ Integration with CI/CD workflows

## Alternative: Deploy via Web Interface

1. **Create a ZIP file of your project:**
   ```bash
   zip -r coupon_scraper.zip . -x "*.pyc" "__pycache__/*" "venv/*" "*.git*"
   ```

2. **Upload via Zyte dashboard:**
   - Go to your project settings
   - Click "Deploy Code"
   - Upload the ZIP file

## Environment Variables

You can set environment variables in the Zyte dashboard:

1. Go to your project settings
2. Click "Settings" > "Environment Variables"
3. Add any required variables from your `.env.example` file

## Monitoring

- **Jobs:** Monitor running and completed jobs
- **Logs:** View detailed logs for debugging
- **Items:** Download scraped data
- **Stats:** View performance metrics

## Tips

1. **Test locally first:** Always test your spider locally before deploying
2. **Use small batches:** Start with small scraping jobs to test
3. **Monitor rate limits:** Be respectful of target websites
4. **Check robots.txt:** Ensure your spider respects robots.txt
5. **Use proxies:** For large-scale scraping, consider using Zyte's proxy services

## Troubleshooting

- **Import errors:** Make sure all dependencies are in requirements.txt
- **Permission errors:** Check robots.txt compliance
- **Rate limiting:** Adjust DOWNLOAD_DELAY and CONCURRENT_REQUESTS
- **Memory issues:** Process items in batches, don't store large amounts in memory
