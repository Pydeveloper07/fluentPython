from copy import copy, deepcopy


def example_with_tuple_relative_immutability():
    t1 = (1, 2, 3, [4, 5])
    t2 = (1, 2, 3, [4, 5])

    assert t1 == t2
    assert t1 is not t2
    t2[-1].append(6)

    assert t1 != t2
    print("Success!")


def example_with_shallow_copy():
    l1 = [1, 2]
    l2 = [l1, 3]
    l3 = list(l2)

    assert l3 == l2
    assert l3 is not l2
    assert l3[0] is l2[0] is l1
    l1.append(5)
    assert l3[0] == l2[0] == l1
    print("Success!")


def example_with_deep_and_shallow_copy():
    class Bus:
        def __init__(self, passengers):
            self.passengers = list(passengers) if passengers else []

        def pick(self, name: str):
            self.passengers.append(name)

        def drop(self, name: str):
            self.passengers.remove(name)

    bus_1 = Bus(["John", "Snow"])
    bus_2 = copy(bus_1)

    assert bus_1 is not bus_2
    assert bus_1.passengers is bus_2.passengers

    bus_2.pick("Michael")
    assert bus_1.passengers == bus_2.passengers
    print("Success shallow copy check!")

    bus_3 = deepcopy(bus_1)

    assert bus_1.passengers is not bus_3.passengers
    assert bus_1.passengers == bus_3.passengers
    bus_3.pick("Lucy")
    assert bus_3.passengers != bus_1.passengers
    print("Success deep copy check!")


def example_with_cyclic_deep_copy_handling():
    a = [10, 20]
    b = [a, 30]
    a.append(b)
    print("a: ", a, id(a))
    assert a[2] is b
    assert a[2][0] is a
    assert a[2][0][2][0][2][0][2][0] is a
    c = deepcopy(a)
    try:
        assert a == c
    except RecursionError as e:
        print(e)

    assert a is not c
    print("c: ", c, id(c))
    print("Success")


def example_with_default_mutable_value_for_parameter():
    class HauntedBus:
        def __init__(self, passengers=[]):
            self.passengers = passengers

        def pick(self, name: str):
            self.passengers.append(name)

        def drop(self, name: str):
            self.passengers.remove(name)

    # It works as expected if we pass some value
    bus1 = HauntedBus(["Alice", "Bob"])
    bus1.pick("Michael")
    print(bus1.passengers)

    # The danger lies when no value is passed and default value is used
    bus2 = HauntedBus()
    bus2.pick("Michael")
    print(bus2.passengers)

    bus3 = HauntedBus()
    print(bus3.passengers)
    assert bus3.passengers != []


def example_with_garbage_collection():
    import weakref

    s1 = {1, 2, 3}
    s2 = s1

    def bye():
        print("Gone with the wind...")

    ender = weakref.finalize(s1, bye)
    print(ender.alive)
    del s1
    print(ender.alive)
    s2 = 'spam'


def example_with_weakref():
    # below code makes i a local variable
    for i in range(1, 5):
        continue
    # List comprehensions do not make i a local variable
    # s = [i for i in range(5)]

    print(i)


def example_with_weakref_2():
    import weakref

    class Cheese:
        def __init__(self, kind):
            self.kind = kind

    # stock has a weak reference to each cheese object
    # when an object is garbage-collected, stock disposes of it as well
    # if regular dictionary used, the objet would never be garbage-collected, because of strong reference.
    stock = weakref.WeakValueDictionary()
    catalog = [Cheese("Dodo"), Cheese("Apex"), Cheese("Otchopar")]
    for cheese in catalog:
        stock[cheese.kind] = cheese
    print("Before deletion of catalog", list(stock.keys()))
    del catalog
    print("After deletion of catalog", list(stock.keys()))
    del cheese
    print(list(stock.keys()))


if __name__ == "__main__":
    example_with_weakref_2()

