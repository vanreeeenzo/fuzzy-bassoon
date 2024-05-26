"""
# Script to Bypass Cloudflare Using Cloudscraper with Logging

This script leverages the `cloudscraper` library to bypass Cloudflare's "I'm Under Attack Mode" (IUAM).
It mimics a real browser to solve the JavaScript challenges set by Cloudflare.

## Why This File Bypasses Cloudflare Security:
1. **Cloudscraper**:
   - Cloudflare uses JavaScript challenges to distinguish between bots and humans.
   - `cloudscraper` bypasses these challenges by simulating browser behavior, allowing automated access to Cloudflare-protected sites.

## Usage:
- Replace the `url` variable with the target URL.
- Ensure `cloudscraper` is installed: `pip install cloudscraper`.

## Code:
"""

import cloudscraper as cs
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def bypass_cloudflare(url):
    scraper = cs.create_scraper()
    response = scraper.get(url)

    if response.status_code == 200:
        logging.info(f"Successfully bypassed Cloudflare. Status Code: {response.status_code}")
        logging.info(f'Reponse: {response.text[:500]}')
    else:
        logging.error(f'Failed to bypass Cloudflare. Status Code: {response.status_code}')


if __name__ == '__main__':
    url = 'TARGET SITE'
    bypass_cloudflare(url)
