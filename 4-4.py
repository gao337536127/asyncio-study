import asyncio

from aiohttp import AsyncResolver, ClientSession
import aiohttp
from utils import DOMESTIC_DNS_SERVERS, async_timed, delay


@async_timed()
async def wrong_main() -> None:
    # 错误地使用带有列表推导式的任务
    delay_times = [3, 3, 3]
    [await asyncio.create_task(delay(seconds)) for seconds in delay_times]


@async_timed()
async def right_main() -> None:
    # 正确的列表推导式
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]


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


@async_timed()
async def gather_main() -> None:
    tasks = [main() for _ in range(10)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(wrong_main())
    asyncio.run(right_main())
    asyncio.run(gather_main())
