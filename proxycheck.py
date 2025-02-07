import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
import time

async def check_proxy(session, proxy):
    """
    Check a single proxy by sending a GET request to httpbin.org/ip.
    Returns a tuple (proxy, True) if working; otherwise (proxy, False).
    """
    url = 'https://httpbin.org/ip'
    try:
        start = time.monotonic()
        if proxy.startswith('socks4://') or proxy.startswith('socks5://'):
            connector = ProxyConnector.from_url(proxy)
            async with aiohttp.ClientSession(connector=connector) as proxy_session:
                async with proxy_session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        elapsed = time.monotonic() - start
                        print(f"{proxy} is working. Response time: {elapsed:.2f}s, IP: {data.get('origin')}")
                        return proxy, True
                    else:
                        print(f"{proxy} is not working. HTTP status: {response.status}")
                        return proxy, False
        else:
            async with session.get(url, proxy=proxy, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    elapsed = time.monotonic() - start
                    print(f"{proxy} is working. Response time: {elapsed:.2f}s, IP: {data.get('origin')}")
                    return proxy, True
                else:
                    print(f"{proxy} is not working. HTTP status: {response.status}")
                    return proxy, False
    except Exception as e:
        print(f"{proxy} failed: {e}")
        return proxy, False

async def check_proxies(proxy_list):
    """
    Concurrently check a list of proxies.
    Returns a list of tuples (proxy, status).
    """
    connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification if needed
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_proxy(session, proxy) for proxy in proxy_list]
        results = await asyncio.gather(*tasks)
    return results

def load_proxies_from_file(file_path):
    """
    Load proxies from a text file, one per line.
    """
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

if __name__ == '__main__':
    proxy_file = 'proxies.txt'  # Path to your proxy list file
    proxies = load_proxies_from_file(proxy_file)

    results = asyncio.run(check_proxies(proxies))
    working_proxies = [proxy for proxy, status in results if status]

    print("\nWorking proxies:")
    for proxy in working_proxies:
        print(proxy)
