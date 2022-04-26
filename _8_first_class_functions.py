import random


def factorial(n):
    """returns n!"""
    return 1 if n == 0 else n*factorial(n-1)


def fact_to_map():
    fact = factorial
    print(fact(5))
    print(type(fact))
    # map() function returns a map object(which is an iterator) of the results after applying the given
    # function to each item of a given iterable (list, tuple etc.)
    m = map(fact, range(11))
    print(list(m))


def sort_by_word_length():
    fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
    sorted_fruits = sorted(fruits, key=len, reverse=True)
    print(sorted_fruits)


def replacement_for_map_and_filter():
    fact = factorial
    print(list(map(fact, range(6))))
    print([fact(n) for n in range(6)])
    print(list(map(fact, filter(lambda x: x % 2, range(6)))))
    print([fact(n) for n in range(6) if n % 2])


class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pop(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError("pick from empty BingoCage")

    def __call__(self, *args, **kwargs):
        return self.pop()


def bingo_cage_example_with_callable():
    bingo_cage = BingoCage(range(6))
    print(bingo_cage.pop())
    print(bingo_cage())
    print(callable(bingo_cage))


class Student(object):
    def __init__(self, first_name=None, last_name=None, age=0):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = age

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def __call__(self, *args, **kwargs):
        return "%s %s" % (self.__first_name, self.__last_name)

    def __sub__(self, other):
        return self.__age - other.__age


def student_example_with_callable():
    student_1 = Student("John", "Snow", 25)
    student_2 = Student("Michael", "Jai", 20)
    print(student_1 - student_2)
    print(student_1.get_first_name())
    print(student_1.get_last_name())
    print(student_1)
    print(student_1())


# HTML tag generator
def tag(name, *content, cls=None, **attrs):
    if cls is not None:
        attrs["class"] = cls

    attrs_str = ""
    if attrs:
        attrs_str = "".join([f' {key}="{value}"' for key, value in attrs.items()])
    if content:
        return "\n".join([f'<{name}{attrs_str}>{c}</{name}>' for c in content])
    else:
        return f'<{name} {attrs_str} />'


def html_tag_generator_example():
    print(tag('p', 'Hello World'))
    print(tag('p', 'Hello World', id="specialTag"))
    print(tag('h1', 'Hello World', id="specialTag", style="border-width: 1px"))


if __name__ == "__main__":
    # print(factorial(42))
    # print(factorial.__doc__)
    # fact_to_map()
    replacement_for_map_and_filter()
    # bingo_cage_example_with_callable()
    # print(type(factorial))
    # html_tag_generator_example()


