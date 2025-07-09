#!/usr/bin/env python3
"""
Coupons.com Scraper Runner
Easy script to scrape coupons from coupons.com with various options
"""

import subprocess
import sys
import json
import argparse
from datetime import datetime


def run_scraper(spider_name='coupons_com', output_file=None, max_pages=None, category=None):
    """Run the coupons.com scraper with specified options"""
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"coupons_com_{timestamp}.json"
    
    # Build scrapy command
    cmd = ['scrapy', 'crawl', spider_name, '-o', output_file]
    
    # Add custom settings
    if max_pages:
        cmd.extend(['-s', f'CLOSESPIDER_PAGECOUNT={max_pages}'])
    
    if category:
        print(f"Note: Category filtering for '{category}' will be applied during scraping")
    
    print(f"Running: {' '.join(cmd)}")
    print(f"Output: {output_file}")
    print("-" * 50)
    
    try:
        # Run the scraper
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=60)  # 60 second timeout
        
        if process.returncode == 0:
            print("✅ Scraping completed successfully!")
            print("Last few lines of output:")
            print(stdout.split('\n')[-10:])
            
            # Try to read and display summary
            try:
                import os
                if os.path.exists(output_file):
                    with open(output_file, 'r') as f:
                        data = json.load(f)
                    
                    print(f"\n📊 Results Summary:")
                    print(f"   Total coupons: {len(data)}")
                    
                    if data:
                        categories = {}
                        codes_found = 0
                        
                        for item in data:
                            cat = item.get('category', 'unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                            
                            if item.get('code'):
                                codes_found += 1
                        
                        print(f"   Coupons with codes: {codes_found}")
                        print(f"   Categories: {categories}")
                        
                        # Show first coupon as example
                        print(f"\n📋 Example coupon:")
                        example = data[0]
                        print(f"   Title: {example.get('title', 'N/A')}")
                        if example.get('code'):
                            print(f"   Code: {example['code']}")
                        if example.get('description'):
                            print(f"   Description: {example['description'][:100]}...")
                else:
                    print(f"Warning: Output file {output_file} not found")
                
            except Exception as e:
                print(f"Could not read output file: {e}")
        else:
            print("❌ Scraping failed!")
            print("STDOUT:", stdout[-500:] if stdout else "None")
            print("STDERR:", stderr[-500:] if stderr else "None")
            
    except subprocess.TimeoutExpired:
        print("⏰ Scraping timed out after 60 seconds")
        process.kill()
    except Exception as e:
        print(f"❌ Error running scraper: {e}")


def main():
    parser = argparse.ArgumentParser(description='Scrape coupons from coupons.com')
    parser.add_argument('--output', '-o', help='Output JSON file name')
    parser.add_argument('--pages', '-p', type=int, help='Maximum pages to scrape')
    parser.add_argument('--category', '-c', help='Filter by category (food, clothing, electronics, etc.)')
    parser.add_argument('--spider', '-s', default='coupons_com', 
                       choices=['coupons_com', 'coupons', 'demo_coupons'],
                       help='Spider to use')
    
    args = parser.parse_args()
    
    print("🕷️  Coupons.com Scraper")
    print("=" * 40)
    
    run_scraper(
        spider_name=args.spider,
        output_file=args.output,
        max_pages=args.pages,
        category=args.category
    )


if __name__ == "__main__":
    main()
