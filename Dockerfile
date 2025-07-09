# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a non-root user
RUN useradd -m scraper && chown -R scraper:scraper /app
USER scraper

# Set environment variables
ENV PYTHONPATH=/app
ENV SCRAPY_SETTINGS_MODULE=coupon_scraper.settings

# Default command (can be overridden)
CMD ["scrapy", "crawl", "demo_coupons", "-o", "output.json"]
