def example_with_spinner_threading():
    import sys
    import itertools
    import threading
    import time

    class Signal:
        go = True

    def spin(msg, signal):
        write, flush = sys.stdout.write, sys.stdout.flush
        for char in itertools.cycle('|/-\\'):
            status = char + ' ' + msg
            write(status)
            flush()
            time.sleep(0.1)
            write('\x08' * len(status))
            if not signal.go:
                break
        write(' ' * len(status) + '\x08' * len(status))

    def slow_function():
        time.sleep(3)
        return 42

    def supervisor():
        signal = Signal()
        spinner = threading.Thread(target=spin, args=('thinking!', signal))
        print("Spinner object - ", spinner)
        spinner.start()
        result = slow_function()
        signal.go = False
        spinner.join()
        print(result)

    supervisor()


def example_with_spinner_asyncio():
    import asyncio
    import sys
    import itertools

    async def spin(msg):
        write, flush = sys.stdout.write, sys.stdout.flush
        for char in itertools.cycle('|/-\\'):
            status = char + ' ' + msg
            write(status)
            flush()
            try:
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
            write("\x08" * len(status))
        write("\x08" * len(status))

    async def slow_function():
        await asyncio.sleep(3)
        return 42

    async def supervisor():
        spinner = asyncio.ensure_future(spin("thinking!"))
        print("Spinner object - ", spinner)
        print("Awaiting...")
        result = await slow_function()
        spinner.cancel()
        return result

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print(result)


def example_download_flag_with_asyncio():
    import os
    import aiohttp
    import sys
    import asyncio
    import time

    POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()

    BASE_URL = 'http://flupy.org/data/flags'

    DEST_DIR = 'downloads/'

    def save_flag(img, filename):
        path = os.path.join(DEST_DIR, filename)
        with open(path, "wb") as fp:
            fp.write(img)

    async def get_flag(cc):
        url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                image = await resp.read()

        return image

    def show(text):
        print(text, end=' ')
        sys.stdout.flush()

    async def download_one(cc, loop):
        image = await get_flag(cc)
        show(cc)
        loop.run_in_executor(None, save_flag, image, cc.lower() + '.gif')
        # save_flag(image, cc + ".gif")
        return cc

    def download_many(cc_list):
        loop = asyncio.get_event_loop()
        to_do = [download_one(cc, loop) for cc in cc_list]
        wait_coro = asyncio.wait(to_do)
        resp, _ = loop.run_until_complete(wait_coro)
        return len(resp)

    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == "__main__":
    example_with_spinner_asyncio()
