import functools
import math
import reprlib
from array import array
from functools import reduce
import operator


class Vector(object):
    typecode = "d"

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['): -1]
        return "Vector({})".format(components)

    def __str__(self):
        return str(tuple(self))

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def __hash__(self):
        hashes = map(hash, self._components)
        return reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __len__(self):
        return len(self._components)

    # # Returns just an array
    # def __getitem__(self, index):
    #     return self._components[index]

    # Returns a single integer or a Vector type
    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, int):
            return self._components[index]
        else:
            raise TypeError("{cls.__name__} indices must be integers.".format(cls=cls))

    shortcut_names = "xyzt"

    def __getattr__(self, item):
        if len(item) == 1:
            pos = self.shortcut_names.find(item)
            if 0 <= pos <= len(self._components):
                return self._components[pos]

        raise AttributeError("{.__name__!r} does not have attribute {!r}".format(type(self), item))

    def __setattr__(self, key, value):
        if len(key) == 1:
            cls = type(self)
            if key in cls.shortcut_names:
                error = "readonly attribute {attr_name!r}"
            elif key.lower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ""
            if error:
                raise AttributeError(error.format(cls_name=cls.__name__, attr_name=key))
        super().__setattr__(key, value)

    @classmethod
    def from_bytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


def example_with_simple_vector():
    vector = Vector([1, 2, 3, 4, 5])
    print(vector)
    print(bytes(vector))
    vector_2 = Vector.from_bytes(bytes(vector))
    print(vector_2)
    print(vector is vector_2)
    print(vector == vector_2)
    print("Length of the vector: %s" % len(vector))
    print("2nd coordinate of the vector: %s" % vector[1])
    sub_vector = vector[:3]
    print(type(sub_vector))
    print(sub_vector)


def example_with_vector_using_advanced_get_item():
    vector = Vector(range(10))
    sub_vector = vector[:5]
    print(type(sub_vector))
    coordinate = vector[1]
    print(type(coordinate))
    try:
        print(vector[1.0])
    except TypeError as e:
        print(e)


def example_with_vector_using_getattr():
    vector = Vector(range(1, 10))
    print(vector.x)
    print(vector.t)
    try:
        print(vector.w)
    except AttributeError as e:
        print(e)
    vector.x = 100
    print(vector.x)
    print(vector[0])


def example_with_vector_using_setattr():
    vector = Vector(range(1, 10))
    vector.name = "Super Vector"
    print(vector.name)
    try:
        vector.x = 10
    except AttributeError as e:
        print(e)
    try:
        vector.w = 100
    except AttributeError as e:
        print(e)


def example_with_factorial_using_reduce():
    n = 5
    result = functools.reduce(lambda a, b: a * b, range(1, n + 1))
    print("%s factorial is %s" % (n, result))


def example_with_vector_hashing():
    vector = Vector(range(1, 15))
    print(hash(vector))


if __name__ == "__main__":
    example_with_simple_vector()
