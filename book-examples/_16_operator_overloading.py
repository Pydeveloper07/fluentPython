import itertools
import math
import numbers
import operator
import reprlib
from array import array
from functools import reduce


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
        if isinstance(other, self.__class__):
            return (len(self) == len(other)) and all(a == b for a, b in zip(self, other))
        else:
            return NotImplemented

    def __hash__(self):
        hashes = map(hash, self._components)
        return reduce(operator.xor, hashes, 0)

    def __neg__(self):
        return Vector(-x for x in self)

    def __pos__(self):
        return Vector(self)

    def __add__(self, other):
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector(x + y for x, y in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Real):
            return Vector(x * scalar for x in self)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __matmul__(self, other):
        try:
            pairs = zip(self, other)
            return reduce(lambda x, y: x + y[0] * y[1], [0, *pairs])
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __len__(self):
        return len(self._components)

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


def example_with_vector_addition():
    v1 = Vector([1, 2, 3])
    v2 = Vector([4])
    print(v1 + v2)
    print(v1 + (2, 3, 5))
    # For this to work __radd__ special method should be implemented
    try:
        print((5, 8, 9) + v1)
    except TypeError as e:
        print(e)

    print(v1 + 1)


def example_with_vector_multiplication_by_scalar():
    from fractions import Fraction
    v1 = Vector([1, 2, 3])
    print(v1 * 3)
    print(3 * v1)
    try:
        print(v1 * 'A')
    except TypeError as e:
        print(e)
    print(v1 * True)
    print(v1 * Fraction(1, 3))


def example_with_vector_dot_product():
    v1 = Vector([1, 2, 3])
    v2 = Vector([3, 2, 1])
    print(v1 @ v2)
    try:
        print(v1 @ 2)
    except TypeError as e:
        print(e)
    print([3, 5, 6] @ v1)
    print([3, 5] @ v1)


def example_with_vector_rich_operators():
    v1 = Vector([1, 2, 3])
    v2 = Vector([3, 2, 1])
    v3 = Vector([1, 2, 3])
    print(v1 == v2)
    print(v1 == [1, 2, 3])
    print([1, 2, 3] == v1)
    print(v1 == 1)
    print(v1 == v3)


if __name__ == "__main__":
    example_with_vector_rich_operators()
