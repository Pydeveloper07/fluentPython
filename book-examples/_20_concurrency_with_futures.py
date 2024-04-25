import random
import time
import sys

# sys.setswitchinterval(100000000)

def example_with_sequential_download():
    import os
    import sys
    import time
    import requests

    POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()

    BASE_URL = 'http://flupy.org/data/flags'

    DEST_DIR = 'downloads/'

    def save_flag(img, filename):
        path = os.path.join(DEST_DIR, filename)
        with open(path, "wb") as fp:
            fp.write(img)

    def get_flag(cc):
        url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
        resp = requests.get(url)
        return resp.content

    def show(text):
        print(text, end=' ')
        sys.stdout.flush()

    def download_many(cc_list):
        for cc in sorted(cc_list):
            image = get_flag(cc)
            show(cc)
            save_flag(image, cc.lower() + '.gif')

        return len(cc_list)

    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


def example_with_concurrent_download():
    import os
    import sys
    import time
    import requests
    from concurrent import futures

    POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()

    BASE_URL = 'http://flupy.org/data/flags'

    DEST_DIR = 'downloads/'

    MAX_WORKERS = 20

    def save_flag(img, filename):
        path = os.path.join(DEST_DIR, filename)
        with open(path, "wb") as fp:
            fp.write(img)

    def get_flag(cc):
        url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
        resp = requests.get(url)
        return resp.content

    def show(text):
        print(text, end=' ')
        sys.stdout.flush()

    def download_one(cc):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
        return cc

    def download_many(cc_list):
        workers = min(MAX_WORKERS, len(cc_list))
        with futures.ThreadPoolExecutor(workers) as executor:
            res = executor.map(download_one, sorted(cc_list))

        return len(list(res))

    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


def example_with_future_demonstration():
    import os
    import sys
    import time
    import requests
    from concurrent import futures

    POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()

    BASE_URL = 'http://flupy.org/data/flags'

    DEST_DIR = 'downloads/'

    def save_flag(img, filename):
        path = os.path.join(DEST_DIR, filename)
        with open(path, "wb") as fp:
            fp.write(img)

    def get_flag(cc):
        url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
        resp = requests.get(url)
        return resp.content

    def show(text):
        print(text, end=' ')
        sys.stdout.flush()

    def download_one(cc):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
        return cc

    def download_many(cc_list):
        cc_list = cc_list[:5]
        results = []
        with futures.ThreadPoolExecutor(max_workers=3) as executor:
            to_do = []
            for cc in sorted(cc_list):
                future = executor.submit(download_one, cc)
                to_do.append(future)
                msg = "Scheduled for {}: {}"
                print(msg.format(cc, future))

            for future in futures.as_completed(to_do):
                res = future.result()
                msg = '{} result: {!r}'
                print(msg.format(future, res))
                results.append(res)
        return len(results)

    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


def example_with_thread_pool_executor():
    from concurrent import futures
    from multiprocessing import Pool
    from time import time
    from cryptography.fernet import Fernet
    import string

    CHARS = string.ascii_lowercase + string.ascii_uppercase

    def random_string(length) -> str:
        return bytes("".join(random.choices(CHARS, k=length)).encode())

    key = Fernet.generate_key()
    f = Fernet(key)

    random_strings = []
    for i in range(1, 10000):
        random_strings.append(random_string(i))

    def encrypt_without_threading():
        t0 = time()
        results = []
        for s in random_strings:
            results.append(f.encrypt(s))
        t1 = time()
        print("Without threading -> ")
        print("Time taken: {} seconds".format(t1 - t0))

    def encrypt_with_threading():
        t0 = time()
        with futures.ProcessPoolExecutor(8) as executor:
            results = executor.map(f.encrypt, random_strings)
        t1 = time()
        print("With threading -> ")
        print("Time taken: {} seconds".format(t1 - t0))

    encrypt_without_threading()
    encrypt_with_threading()


def main(num):
    if num == 1:
        time.sleep(5)
    start = time.time()
    print(f"start worker {num}")
    print(sum(range(200000000)))
    print(f"end worker {num}")
    print(time.time() - start)


if __name__ == "__main__":
    from concurrent import futures

    executor = futures.ProcessPoolExecutor(max_workers=5)
    executor.submit(main, 1)
    executor.submit(main, 2)
    executor.submit(main, 3)
    executor.submit(main, 4)
    executor.submit(main, 5)

