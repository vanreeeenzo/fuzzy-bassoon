"""
# Script for DNS Record Lookup with Logging

This script is designed to discover various DNS records associated with a domain.
It uses the `dnspython` library to perform DNS lookups and logs the process for each record type.

## Why This File Bypasses Cloudflare Security:
1. **Origin IP Address Discovery**:
   - By finding the origin IP address of a website, attackers can bypass Cloudflare by directly targeting the server.
   - DNS records, SSL certificates, and email headers can reveal the server's IP address, circumventing Cloudflare's protection.

## Usage:
- Replace the `domain` variable with the target domain name.
- Ensure `dnspython` is installed: `pip install dnspython`.

## Code:
"""

import dns.resolver
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_dns_records(domain):
    records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [rdata.to_text() for rdata in answers]
            logging.info(f'Found {record_type} records for {domain}: {records[record_type]}')
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.resolver.Timeout):
            records[record_type] = []
            logging.warning(f'No {record_type} records found for {domain}')

    return records


if __name__ == '__main__':
    domains = str(input("Enter Domain Name: "))
    dns_records = get_dns_records(domains)

    for record_typing, record_list in dns_records.items():
        print(f'{record_typing} records: ')
        for record in record_list:
            print(f' - {record}')
