import asyncio
import random
from concurrent import futures


def random_str(n: int):
    chars = list("abcdefghijklmnopqrstuvwxyz1234567890")
    return "".join([random.choice(chars) for _ in range(n)])


async def gather_futures(futures, chunk_size: int = 10):
    total = len(futures)
    chunked_futures = [futures[i:i + chunk_size] for i in range(0, len(futures), chunk_size)]
    for i, chunk in enumerate(chunked_futures):
        print(f"{(i + 1) * len(chunk)}/{total}")
        await asyncio.gather(*chunk)


async def product_generator(count, client, loop=False, query=None):
    page = 1
    while True:
        products = await client.get_products(query=query, page=page, limit=count)
        if not products:
            if loop:
                page = 1
                continue
            else:
                break
        yield products
        page += 1


async def variant_generator(count, client, loop=False, query=None):
    page = 100
    while True:
        variants = await client.get_variants(query=query, page=page, limit=count)
        if not variants:
            if loop:
                page = 1
                continue
            else:
                break
        yield variants
        page += 1


def run_async_function(async_func, *args, **kwargs):
    print(*args, **kwargs)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_func(*args, **kwargs))
    return result


def run_in_multiple_processes(workers: int, async_func, *args, **kwargs):
    executor = futures.ProcessPoolExecutor(max_workers=workers)
    executor.submit(run_async_function, async_func, *args, **kwargs)
