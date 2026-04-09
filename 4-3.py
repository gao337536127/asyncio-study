import asyncio
import aiohttp
from aiohttp import AsyncResolver, ClientSession
from utils import DOMESTIC_DNS_SERVERS


async def fetch_status(session: ClientSession, url: str) -> int:
    # aiohttp超时
    ten_millis = aiohttp.ClientTimeout(total=0.01)
    async with session.get(url, timeout=ten_millis) as result:
        return result.status


async def main():
    resolver = AsyncResolver(nameservers=DOMESTIC_DNS_SERVERS)
    connector = aiohttp.TCPConnector(
        resolver=resolver,
    )
    session_timeout = aiohttp.ClientTimeout(total=1, connect=0.1)
    async with aiohttp.ClientSession(
        timeout=session_timeout, connector=connector
    ) as session:
        await fetch_status(session, "https://www.baidu.com")


if __name__ == "__main__":
    asyncio.run(main())
