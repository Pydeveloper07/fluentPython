import math
from array import array


class Vector2d(object):
    __slots__ = ("__x", "__y")

    typecode = "d"

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def angle(self):
        return math.atan2(self.y, self.x)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        return "{}({!r}, {!r})".format(type(self).__name__, *self)

    def __str__(self):
        return "({}, {})".format(*self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __format__(self, format_spec: str = ''):
        if format_spec.endswith("p"):
            format_spec = format_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = "<{}, {}>"
        else:
            coords = self
            outer_fmt = "({}, {})"
        components = (format(i, format_spec) for i in coords)
        return outer_fmt.format(*components)

    def __hash__(self):
        # use ^ - bitwise XOR operator to combine hashes of components
        return hash(self.x) ^ hash(self.y)


def example_with_vector2d():
    v1 = Vector2d(1, 0)
    print(v1)
    x, y = v1
    print(x, y)
    v2 = eval(repr(v1))
    print(v1 == v2)
    v0 = Vector2d(0, 0)
    print(bool(v0))
    print(bytes(v1))


def example_with_import_from_binary_sequence():
    v = Vector2d(3, 4)
    octets = bytes(v)
    v1 = Vector2d.frombytes(octets)
    print(v1)


def example_with_formatted_displays():
    print(format(1 / 241, "0.4f"))
    print("{:0.4f}".format(1 / 241))
    print(format(2 / 3, "0.2%"))
    print(format(100, "b"))
    print("{:b}".format(100))


def example_vector_with_format_special_method():
    # __format__ method of the class should be implemented for this to work
    v = Vector2d(3, 4)
    print("{}".format(v))


def example_with_customer_formatter():
    # if format specifier ends with p, it returns the polar representation
    # of the vector in the format of <magnitude, theta(angle)>
    v = Vector2d(3, 3)
    print("{:0.1f}".format(v))


def example_with_read_only_vector():
    # decorate getter of the attr with @property decorator and make
    # actual attrs private
    v = Vector2d(3, 4)
    try:
        v.x = 4
    except AttributeError as e:
        print(e)


def example_with_hashable_vector():
    # implement the special __hash__ method to make Vector2d objects hashable
    # note: it should return an int
    # note: the __eq__ special method should also be implemented
    v1 = Vector2d(3, 4)
    v2 = Vector2d(2, 5)
    print(hash(v1))
    print(hash(v2))
    print(v1 == v2)
    print({v1, v2})


def example_with_private_property():
    v = Vector2d(2, 3)
    print(v.__dict__)
    print(v._Vector2d__x)
    try:
        v.x = 100
    except AttributeError as e:
        print(e)
        v._Vector2d__x = 100
    print(v.x)


def example_with_slots_attribute():
    # Vector2d class should have a special __slots__ field initialized
    v = Vector2d(3, 4)
    try:
        v.z = 4
    except AttributeError as e:
        print(e)
    try:
        print(v.__dict__)
    except AttributeError as e:
        print(e)


if __name__ == "__main__":
    example_with_slots_attribute()
