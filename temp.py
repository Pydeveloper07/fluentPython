import asyncio
import concurrent.futures
import time


def blocking():
    print("Blocking started")
    time.sleep(3)
    print("Blocking finished")


async def non_blocking():
    print("Non-blocking started")
    await asyncio.sleep(1)
    print("Non-blocking finished")


async def blocking_wrapper():
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, blocking)
    return result


async def main():
    results = await asyncio.gather(blocking_wrapper(), non_blocking())
    print(results)


if __name__ == '__main__':
    asyncio.run(main())
