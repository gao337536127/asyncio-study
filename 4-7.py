import asyncio
from utils import delay


async def main():
    result = await asyncio.gather(delay(3), delay(1))
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
