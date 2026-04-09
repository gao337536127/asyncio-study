# gather中的异常
import asyncio

from aiohttp import AsyncResolver, ClientSession
import aiohttp

from utils import DOMESTIC_DNS_SERVERS, async_timed


# @async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


# @async_timed()
async def main():
    resolver = AsyncResolver(nameservers=DOMESTIC_DNS_SERVERS)
    connector = aiohttp.TCPConnector(
        resolver=resolver,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        urls = [
            "https://www.baidu.com",
            "https://www.163.com",
            "python://www.baidu.com",
            "https://www.sina.com.cn",
        ]
        tasks = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*tasks, return_exceptions=True)
        for status_code in status_codes:
            if isinstance(status_code, Exception):
                print(status_code)
            else:
                print(status_code)


async def fetch_status_with_delay(
    session: ClientSession, url: str, delay: int = 0
) -> int:
    await asyncio.sleep(delay)
    return await fetch_status(session, url)


async def main_with_as_completed():
    resolver = AsyncResolver(nameservers=DOMESTIC_DNS_SERVERS)
    connector = aiohttp.TCPConnector(
        resolver=resolver,
    )
    async with aiohttp.ClientSession(connector=connector) as session:
        fetchers = [
            fetch_status_with_delay(session, "https://www.baidu.com", delay=1),
            fetch_status_with_delay(session, "https://www.163.com", delay=3),
            fetch_status_with_delay(session, "python://www.baidu.com", delay=1),
            fetch_status_with_delay(session, "https://www.sina.com.cn", delay=1),
        ]
        for finished_task in asyncio.as_completed(fetchers):
            try:
                status_code = await finished_task
                print(status_code)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    asyncio.run(main_with_as_completed())
