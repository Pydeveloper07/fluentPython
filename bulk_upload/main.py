import asyncio
import concurrent.futures


def f(a, b, c, d):
    print(a, b, c, d)
    return a + b + c + d


async def main():
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        response = await loop.run_in_executor(executor, f, 1, 2, 3, 4)
    print(response)

asyncio.run(main())
