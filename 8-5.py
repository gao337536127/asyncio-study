import asyncio
from asyncio import StreamReader
import sys
from utils import delay


async def create_stdin_reader() -> StreamReader:
    stream_reader = StreamReader()
    protocal = asyncio.StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocal, sys.stdin)
    return stream_reader


async def main():
    stdin_reader = await create_stdin_reader()
    while True:
        delay_time = await stdin_reader.readline()
        print(f"Received input: {delay_time.decode().strip()}")
        # delay_time = delay_time.decode().strip()
        # if delay_time.lower() == "exit":
        #     print("Exiting...")
        #     break
        # else:
        #     try:
        #         delay_time = float(delay_time)
        #         asyncio.create_task(delay(delay_time))
        #     except ValueError:
        #         print("Please enter a valid number for delay time.")


if __name__ == "__main__":
    asyncio.run(main())
