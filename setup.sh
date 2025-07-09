#!/bin/bash

# Simple setup script for the coupon scraper

echo "Setting up Coupon Scraper..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install additional tools for Zyte deployment
echo "Installing Zyte tools..."
pip install shub

echo "Setup complete!"
echo ""
echo "To run the scraper:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the demo spider: scrapy crawl demo_coupons -o demo_output.json"
echo "3. Run the main spider: scrapy crawl coupons -o output.json"
echo ""
echo "To deploy to Zyte Scrapy Cloud:"
echo "1. Login: shub login"
echo "2. Deploy: shub deploy"
