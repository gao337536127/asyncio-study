import asyncio
import aiohttp
from aiohttp import ClientSession
from utils import async_timed
from aiohttp import AsyncResolver
from utils import DOMESTIC_DNS_SERVERS


@async_timed()
async def fetch_status_with_delay(
    session: ClientSession, url: str, delay: int = 0
) -> int:
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    resolver = AsyncResolver(nameservers=DOMESTIC_DNS_SERVERS)
    connector = aiohttp.TCPConnector(
        resolver=resolver,
    )
    async with aiohttp.ClientSession(connector=connector) as session:
        fetchers = [
            asyncio.create_task(
                fetch_status_with_delay(session, "https://www.baidu.com", delay=1)
            ),
            asyncio.create_task(
                fetch_status_with_delay(session, "https://www.163.com", delay=3)
            ),
            asyncio.create_task(
                fetch_status_with_delay(session, "python://www.baidu.com", delay=2)
            ),
            asyncio.create_task(
                fetch_status_with_delay(session, "https://www.sina.com.cn", delay=2)
            ),
        ]
        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_EXCEPTION
        )
        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")
        for done_task in done:
            if done_task.exception():
                print(done_task.exception())
            else:
                print(done_task.result())

        for pending_task in pending:
            pending_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
