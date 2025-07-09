#!/usr/bin/env python3
"""
Test script for the coupon scraper
"""

import json
import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def test_scrapy_installation():
    """Test if Scrapy is properly installed"""
    print("Testing Scrapy installation...")
    success, stdout, stderr = run_command("python -c 'import scrapy; print(scrapy.__version__)'")
    
    if success:
        print(f"✓ Scrapy is installed (version: {stdout.strip()})")
        return True
    else:
        print(f"✗ Scrapy installation failed: {stderr}")
        return False


def test_demo_spider():
    """Test the demo spider"""
    print("\nTesting demo spider...")
    
    # Run the demo spider
    success, stdout, stderr = run_command("scrapy crawl demo_coupons -o test_demo.json --loglevel=ERROR")
    
    if not success:
        print(f"✗ Demo spider failed: {stderr}")
        return False
    
    # Check if output file was created
    output_file = Path("test_demo.json")
    if not output_file.exists():
        print("✗ Demo spider didn't create output file")
        return False
    
    # Check if output contains valid JSON
    try:
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        if not data:
            print("✗ Demo spider produced empty output")
            return False
        
        print(f"✓ Demo spider created {len(data)} items")
        
        # Print first item as example
        if data:
            print("Example item:")
            print(json.dumps(data[0], indent=2))
        
        # Clean up test file
        output_file.unlink()
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ Demo spider output is not valid JSON: {e}")
        return False


def test_project_structure():
    """Test if all required files exist"""
    print("\nTesting project structure...")
    
    required_files = [
        "scrapy.cfg",
        "requirements.txt",
        "coupon_scraper/__init__.py",
        "coupon_scraper/items.py",
        "coupon_scraper/settings.py",
        "coupon_scraper/pipelines.py",
        "coupon_scraper/middlewares.py",
        "coupon_scraper/spiders/__init__.py",
        "coupon_scraper/spiders/coupons_spider.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✓ All required files exist")
        return True


def main():
    """Run all tests"""
    print("Coupon Scraper Test Suite")
    print("=" * 40)
    
    tests = [
        test_project_structure,
        test_scrapy_installation,
        test_demo_spider
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your scraper is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
