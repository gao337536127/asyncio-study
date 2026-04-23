import asyncio
from utils import delay


async def main():
    while True:
        delay_time = input("Enter delay time (or 'exit' to quit): ")
        if delay_time.lower() == "exit":
            print("Exiting...")
            break
        else:
            try:
                delay_time = float(delay_time)
                asyncio.create_task(delay(delay_time))
            except ValueError:
                print("Please enter a valid number for delay time.")


if __name__ == "__main__":
    asyncio.run(main())
