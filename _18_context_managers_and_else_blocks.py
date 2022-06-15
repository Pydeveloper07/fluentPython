def example_with_for_else():
    my_list = [1, 2, 3, 4, 5, 6]
    for number in my_list:
        if number == 7:
            break
    else:
        raise ValueError("Number 7 not found")


def example_with_for_else_continue():
    my_list = [1, 2, 3, 4, 5, 6]
    for number in my_list:
        if number == 6:
            break
    else:
        raise ValueError("Number 6 not found")

    print("Match")


def example_with_proper_try_else_block():
    def dangerous_function(code: int):
        if code == 3:
            raise OSError("Malicious function call.")
        else:
            pass

    def after_call():
        print("No malicious function call detected.")

    try:
        dangerous_function(3)
    except OSError as e:
        print(e)
    else:
        after_call()

    print("*" * 20)

    try:
        dangerous_function(1)
    except OSError as e:
        print(e)
    else:
        after_call()


def example_with_with_context_manager():
    import sys

    class LookingGlass:
        def __enter__(self):
            self.original_write = sys.stdout.write
            sys.stdout.write = self.patched_write
            return "JHNGKLAI"

        def patched_write(self, text):
            self.original_write(text[::-1])

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.write = self.original_write
            if exc_type is ZeroDivisionError:
                print("Do not divide by zero!")
                return True

    with LookingGlass() as mirror:
        print("Hey! What's up?")
        print(mirror)

    print("Hey! What's up?")
    print(mirror)


def example_with_generator_context_manager():
    from contextlib import contextmanager
    import sys

    @contextmanager
    def looking_glass():
        original_write = sys.stdout.write

        def patched_write(text):
            return original_write(text[::-1])

        sys.stdout.write = patched_write
        try:
            yield "BLACKTIGER"
        except ZeroDivisionError:
            print("Do not divide by zero!")
        finally:
            sys.stdout.write = original_write

    with looking_glass() as mirror:
        print("Hey! What's dude?")
        print(mirror)

    print(mirror)


if __name__ == "__main__":
    example_with_generator_context_manager()
