import asyncio
import time
import random
from ipaddress import IPv4Address, ip_address
from random import shuffle
from urllib.request import urlretrieve as download
from dns import asyncresolver
import json

# Ограничение количества одновременных запросов
SEMAPHORE_LIMIT = 100
DELAY_RANGE = (1, 3)  # задержка между запросами от 1 до 3 секунд

semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

type IPList = list[IPv4Address]

def get_ip_fetcher():
    from yaml import load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    ares = asyncresolver.Resolver(configure=False)

    # load resolvers from dns_resolvers.yaml
    with open('dns_resolvers.json', mode='r', encoding='utf-8') as resolvers_file:
        ares.nameservers = json.load(resolvers_file)

    # specify timeout and lifetime
    ares.timeout = 10
    ares.lifetime = 10

    # shuffle resolvers in hopes of finding more ips
    shuffle(ares.nameservers)

    async def ip_fetcher(domain: str, query: str, ipList: IPList, retries: int = 3):
        for attempt in range(retries):
            current_resolver = ares.nameservers[attempt % len(ares.nameservers)]
            resolver = asyncresolver.Resolver(configure=False)
            resolver.nameservers = [current_resolver]
            resolver.timeout = ares.timeout
            resolver.lifetime = ares.lifetime

            async with semaphore:
                try:
                    # Добавляем рандомную задержку перед запросом
                    await asyncio.sleep(random.uniform(*DELAY_RANGE))

                    # get ips
                    ips = await resolver.resolve(domain, query)
                    ips = [ip_address(i) for i in ips]

                    # filter only IPv4 addresses
                    ips = [ip for ip in ips if isinstance(ip, IPv4Address)]

                    # print ips format 'example.com IN A [192.0.2.1, ...]'
                    print(domain, 'IN', query, ips)

                    # append the ips for listing
                    ipList += ips
                    return  # Успех, выходим из функции
                except Exception as e:
                    print(f"Error resolving {domain} with resolver {current_resolver}: {e}")

        print(f"All attempts to resolve {domain} failed.")
        
    return ip_fetcher


def read_ips(ipv4List: list[IPv4Address]):
    with open('ipv4_list.txt', mode='r', encoding='utf-8') as f:
        for ip in f.readlines():
            ip = ip.strip()
            try:
                ip = ip_address(ip)
                if isinstance(ip, IPv4Address):
                    ipv4List.append(ip)
            except ValueError:
                if ip != '':
                    print('%s is not a valid IPv4 address!' % ip)

    # de-duplicate list entries
    ipv4List = list(set(ipv4List))


def download_youtubeparsed():
    url = 'https://raw.githubusercontent.com/EikeiDev/test_block/refs/heads/main/youtubeparsed'
    download(url, 'youtubeparsed')


def get_coroutines(ipv4List: list[IPv4Address], ip_fetcher):
    coroutines = []

    with open('youtubeparsed', mode='r', encoding='utf-8') as f:
        for url in f.readlines():
            url = url.strip()
            if url == '' or url.startswith('#'):
                continue
            coroutines.append(ip_fetcher(url, 'A', ipv4List))

    return coroutines


def write_ips(ipv4List: list[IPv4Address]):
    ipv4Set = set(ipv4List)
    ipv4Set.discard(ip_address('0.0.0.0'))
    ipv4List = list(ipv4Set)
    ipv4List.sort()

    with open('ipv4_list.txt', mode='w', encoding='utf-8') as f:
        f.write('\n'.join(map(str, ipv4List)) + '\n')


async def main():
    ipv4List: list[IPv4Address] = []
    read_ips(ipv4List)
    previousIpv4s = len(ipv4List)
    download_youtubeparsed()
    ip_fetcher = get_ip_fetcher()
    coroutines = get_coroutines(ipv4List, ip_fetcher)

    # Ограничиваем количество одновременно запущенных корутин
    for i in range(0, len(coroutines), SEMAPHORE_LIMIT):
        await asyncio.gather(*coroutines[i:i+SEMAPHORE_LIMIT])

    ipv4List = list(set(ipv4List))
    print('Read', previousIpv4s, 'ipv4\'s from ipv4_list.txt')
    print('Number of new ipv4 addresses found:', len(ipv4List) - previousIpv4s)
    read_ips(ipv4List)
    write_ips(ipv4List)


if __name__ == '__main__':
    asyncio.run(main())
