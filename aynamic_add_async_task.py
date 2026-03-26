import asyncio
from threading import Thread
import time


async def show_time(name: str, n=30):
    for i in range(n):
        print(
            f"async name: {name}, time = {time.time()}, loop = {id(asyncio.get_running_loop())}"
        )
        await asyncio.sleep(1)
    return n


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    t1 = Thread(target=lambda: loop.run_forever())
    t1.start()

    time.sleep(5)
    f1 = asyncio.run_coroutine_threadsafe(show_time("add1", n=20), loop=loop)

    time.sleep(5)
    f2 = asyncio.run_coroutine_threadsafe(show_time("add2", n=10), loop=loop)

    time.sleep(25)
    print(f"f1 result: {f1.result()}")
    print(f"f2 result: {f2.result()}")

    t1.join()
