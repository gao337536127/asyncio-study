import functools
import time
import requests
import asyncio
from utils import async_timed
from concurrent.futures import ProcessPoolExecutor

pool = None


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main(executor):
    loop = asyncio.get_running_loop()
    urls = ["https://www.baidu.com" for _ in range(100)]
    tasks = [
        loop.run_in_executor(executor, functools.partial(get_status_code, url))
        for url in urls
    ]
    results = await asyncio.gather(*tasks)
    print(results)


if __name__ == "__main__":
    pool = ProcessPoolExecutor(max_workers=30)
    asyncio.run(main(None))
    time.sleep(1)
    asyncio.run(main(pool))
