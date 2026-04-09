import asyncio
import socket
import aiohttp
from aiohttp import AsyncResolver, ClientSession
from utils import DOMESTIC_DNS_SERVERS, async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        peername = result.connection
        print(f"Peer name: {peername}")
        return result.status


@async_timed()
async def main():
    resolver = AsyncResolver(nameservers=DOMESTIC_DNS_SERVERS)
    connector = aiohttp.TCPConnector(
        resolver=resolver,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        status = await fetch_status(session, "https://www.baidu.com")
        print(f"Status: {status}")


if __name__ == "__main__":
    asyncio.run(main())
