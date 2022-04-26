import math
from math import hypot


class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __repr__(self):
        return "Vector(%r, %r)" % (self.x, self.y)


v1 = Vector(1, 4)
v2 = Vector(2, 5)
print("Magnitude: {}".format(abs(v1)))
print("Magnitude of 3 times v1: {}".format(abs(v1 * 3)))
print("v1 + v2: {}".format(v1 + v2))
