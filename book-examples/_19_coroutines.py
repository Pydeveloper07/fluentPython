import typing


def example_with_simple_coroutine():
    def simple_coroutine():
        print("-> Coroutine started")
        x = yield
        print("-> Coroutine ended")

    coroutine = simple_coroutine()
    next(coroutine)
    coroutine.send(7)


def example_with_coroutine_2():
    from inspect import getgeneratorstate

    def simple_coro_2(a):
        print(f"Received a = {a}")
        b = yield a
        print(f"Received b = {b}")
        c = yield a + b
        print(f"Received c = {c}")

    coro = simple_coro_2(7)
    print(getgeneratorstate(coro))
    print(next(coro))
    print(getgeneratorstate(coro))
    print(coro.send(14))
    print(coro.send(21))


def example_with_averager_coroutine():
    from inspect import getgeneratorstate

    def averager_coroutine():
        total = 0
        count = 0
        average = None
        while True:
            entry = yield average
            total += entry
            count += 1
            average = total / count

    sequence = []
    averager = averager_coroutine()
    # Activate coroutine
    next(averager)

    sequence.append(7)
    print("Average of %s: %s" % (sequence, averager.send(7)))
    sequence.append(10)
    print("Average of %s: %s" % (sequence, averager.send(10)))
    sequence.append(13)
    print("Average of %s: %s" % (sequence, averager.send(13)))
    sequence.append(22)
    print("Average of %s: %s" % (sequence, averager.send(22)))
    averager.close()
    print(getgeneratorstate(averager))


def example_with_averager_coroutine_with_priming_decorator():
    from functools import wraps

    def coroutine(func):
        @wraps(func)
        def primer(*args, **kwargs):
            resp = func(*args, **kwargs)
            next(resp)
            return resp
        return primer

    @coroutine
    def averager_coroutine():
        total = 0
        count = 0
        average = None
        while True:
            entry = yield average
            total += entry
            count += 1
            average = total / count

    sequence = []
    averager = averager_coroutine()

    sequence.append(7)
    print("Average of %s: %s" % (sequence, averager.send(7)))
    sequence.append(10)
    print("Average of %s: %s" % (sequence, averager.send(10)))
    sequence.append(13)
    print("Average of %s: %s" % (sequence, averager.send(13)))
    sequence.append(22)
    print("Average of %s: %s" % (sequence, averager.send(22)))
    averager.close()


def example_coroutine_exc_handling():
    class DemoException(Exception):
        pass

    def demo_exc_handling():
        print("Coroutine started")
        while True:
            try:
                x = yield
            except DemoException:
                print("Demo exception handled. Continuing...")
            else:
                print("Received value x -> %s" % x)
        raise RuntimeError("This line should never run!")

    coro = demo_exc_handling()
    next(coro)
    coro.send(2)
    coro.throw(DemoException("exception happened"))
    coro.send(5)


def example_with_coroutine_exc_finally():
    def demo_finally():
        try:
            while True:
                try:
                    x = yield
                except ZeroDivisionError:
                    print("Handled ZeroDivisionError exception. Continuing execution...")
                else:
                    print("Received value for x: %s" % x)
        finally:
            print("-> coroutine ending")

    coro = demo_finally()
    next(coro)
    coro.send(7)
    coro.throw(ZeroDivisionError)
    coro.send(20)
    coro.send(TypeError)


def example_with_coroutine_returning_value_at_the_end():
    from collections import namedtuple

    Result = namedtuple("Result", "average, count, terms")

    def averager():
        total, count, terms, average = 0, 0, [], None
        while True:
            term = yield
            if term is None:
                break
            try:
                total += term
                count += 1
            except TypeError:
                print("Type error happened. Skipping %s" % term)
                continue
            average = total / count
            terms.append(term)
        return Result(average, count, terms)

    coro = averager()
    next(coro)

    coro.send(7)
    coro.send(21)
    coro.send("wq")
    coro.send([1, 2, 3])
    try:
        coro.send(None)
    except StopIteration as exc:
        result = exc.value
    print(result)


def example_with_coroutine_with_yield_from():
    from collections import namedtuple

    Result = namedtuple("Result", "average, count, terms")

    def averager(res: list):
        def inner_coroutine():
            total, count, terms, average = 0, 0, [], None
            while True:
                term = yield
                if term is None:
                    break
                try:
                    total += term
                    count += 1
                except TypeError:
                    print("Type error happened. Skipping %s" % term)
                    continue
                average = total / count
                terms.append(term)
            return Result(average, count, terms)
        while True:
            r = yield from inner_coroutine()
            res.append(r)

    results = []
    coro = averager(results)
    next(coro)

    for i in range(7):
        coro.send(i)
    else:
        coro.send(None)

    for i in range(9, 11):
        coro.send(i)
    else:
        coro.send(None)

    print(results)


if __name__ == "__main__":
    example_with_coroutine_with_yield_from()
