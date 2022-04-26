def example_how_decorator_works():
    def deco(func):
        def inner():
            print("Running inner()")
        return inner

    @deco
    def target():
        print("Running target()")

    target()


def example_when_decorator_execution_starts():
    registry = []

    def register(func):
        print("running register(%s)" % func)
        registry.append(func)
        return func

    @register
    def f1():
        print("running f1()")

    @register
    def f2():
        print("running f2()")

    def f3():
        print("running f3()")

    print("running main()")
    print("registry -> ", registry)
    f1()
    f2()
    f3()


def example_with_variable_scope():
    b = 9

    def f1(a):
        print("Inside f1: ")
        print(a)
        print(b)

    def f2(a):
        print("Inside f2: ")
        print(a)
        try:
            print(b)
        except UnboundLocalError:
            print("variable b is used before assignment.")
            return
        b = 4

    f1(3)
    f2(3)


def example_with_average_with_class():
    class Average(object):
        def __init__(self):
            self.__series = []

        def __call__(self, new_value):
            self.__series.append(new_value)
            return sum(self.__series) / len(self.__series)

    avg = Average()
    print(avg(10))
    print(avg(20))
    print(avg(30))


def example_with_average_with_higher_order_function():
    def make_averager():
        series = []

        def handler(new_value):
            series.append(new_value)
            return sum(series) / len(series)
        return handler

    avg = make_averager()
    print("Local variables: %s" % avg.__code__.co_varnames)
    print("Free variables: %s" % avg.__code__.co_freevars)
    print("Closure cell content: %s" % avg.__closure__[0].cell_contents)
    print("Average: %f" % avg(10))
    print("Closure cell content: %s" % avg.__closure__[0].cell_contents)
    print("Average: %f" % avg(20))
    print("Closure cell content: %s" % avg.__closure__[0].cell_contents)
    print("Average: %f" % avg(30))
    print("Closure cell content: %s" % avg.__closure__[0].cell_contents)


def example_with_a_broken_higher_order_function():
    def make_averager():
        count = 0
        total = 0

        def average(new_value):
            count += 1
            total += new_value
            return total / count
        return average

    avg = make_averager()
    print(avg(10))


def example_with_a_correct_higher_order_function():
    def make_averager():
        count = 0
        total = 0

        def average(new_value):
            nonlocal count, total
            count += 1
            total += new_value
            return total / count
        return average

    avg = make_averager()
    print(avg(10))


def example_clock_decorator():
    import time

    def clock(func):
        def handler(*args):
            t0 = time.perf_counter()
            result = func(*args)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args_str = ", ".join([repr(arg) for arg in args])
            print("[%0.8fs] %s(%s) -> %s" % (elapsed, name, args_str, result))
            return result

        return handler

    @clock
    def factorial(n):
        return 1 if n == 0 else n * factorial(n - 1)

    @clock
    def snooze(seconds):
        time.sleep(seconds)

    factorial(5)
    snooze(2)


def example_clock_decorator_with_keyword_arguments():
    import time
    import functools

    def clock(func):
        @functools.wraps(func)
        def handler(*args, **kwargs):
            t0 = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args_list = []
            if args:
                args_list.append(", ".join([repr(arg) for arg in args]))
            if kwargs:
                for key, val in kwargs.items():
                    args_list.append("%s=%s" % (key, val))
            args_str = ", ".join(args_list)
            print("[%0.8fs] %s(%s) -> %s" % (elapsed, name, args_str, result))
            return result

        return handler

    @clock
    def sum_(start, end, step=1):
        result = 0
        for i in range(start, end+1, step):
            result += i

        return result

    sum_(start=1, end=10, step=2)


def example_with_lru_cache():
    import time
    import functools

    def clock(func):
        @functools.wraps(func)
        def handler(*args, **kwargs):
            t0 = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args_list = []
            if args:
                args_list.append(", ".join(repr(arg) for arg in args))
            if kwargs:
                for key, value in kwargs.items():
                    args_list.append("%s=%s" % (key, value))
            args_str = ", ".join(args_list)
            print("[%0.8fs] %s(%s) -> %s" % (elapsed, name, args_str, result))

            return result

        return handler

    @functools.lru_cache()
    @clock
    def fibonacci(n):
        return 1 if n in [0, 1] else fibonacci(n - 2) + fibonacci(n - 1)

    t0 = time.perf_counter()
    print(fibonacci(500))
    print("Elapsed: %ss" % (time.perf_counter() - t0))


def example_single_dispatch():
    """
        A function that performs different operations according to type of the argument passed.
        str -> return the list of characters in the string
        float -> return the square of the float number
        int -> return the cube of the int number
        list -> return the elements of the list as comma-separated string
    """
    import functools

    class Student:
        first_name = "John"
        last_name = "Snow"

    @functools.singledispatch
    def function(var):
        print("General variable!")
        return var

    @function.register(str)
    def _(text):
        print("Text type argument received.")
        return list(text)

    @function.register(float)
    def _(number):
        print("Float type argument received.")
        return number ** 2

    @function.register(int)
    def _(number):
        print("Int type argument received.")
        return number ** 3

    @function.register(list)
    def _(list_):
        print("List type argument received.")
        return ",".join(str(s) for s in list_)

    @function.register(Student)
    def _(student_: Student):
        print("Student type argument received.")
        return " ".join([student_.first_name, student_.last_name])

    student = Student()
    print(function(student))


def example_api_dispatcher_passing_arg_to_decorator():
    api_dispatcher = dict()

    def api(url):
        def decorator(func):
            api_dispatcher[url] = func
            return func
        return decorator

    @api("/")
    def home(request):
        print("Response to url '/' is %s." % request["data"])

    @api("listings/")
    def listings(request):
        print("Response to url 'listings/' is %s." % request["data"])

    @api("listing/")
    def listing(request):
        print("Response to url 'listing/' is %s." % request["data"])

    api_dispatcher["/"](dict(data="Home"))
    api_dispatcher["listings/"](dict(data=[dict(id=1, name="Samsung"), dict(id=2, name="Apple")]))
    api_dispatcher["listing/"](dict(data=dict(id=1, name="Samsung", number_of_phones=867)))


def example_with_parameterized_clock_decorator():
    import functools
    import time

    DEFAULT_FMT = "[{elapsed:0.8f}s {name}({args}) -> {result}]"

    def clock(fmt=DEFAULT_FMT):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                t0 = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - t0
                name = func.__name__
                args = ", ".join([str(arg) for arg in args])
                print(fmt.format(**locals()))
                return result
            return wrapper
        return decorator

    @clock()
    def fibonacci(n):
        return 1 if n < 2 else fibonacci(n - 2) + fibonacci(n - 1)

    fibonacci(4)


if __name__ == "__main__":
    example_with_parameterized_clock_decorator()
