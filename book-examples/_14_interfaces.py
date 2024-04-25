import random
import abc


class Tombola(abc.ABC):
    @abc.abstractmethod
    def load(self, iterable):
        """Add items from an iterable"""

    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it.
        This method should raise 'LookupError' when the instance is empty."""

    def loaded(self):
        """Return 'True' if there is at least 1 item, 'False' otherwise"""
        return bool(self.inspect())

    def inspect(self):
        """Return a sorted tuple with the items currently inside."""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))


class BingoCage(Tombola):
    def __init__(self, items):
        self._random = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(list(items))
        self._random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError("Pick from an empty cage.")

    def __call__(self, *args, **kwargs):
        return self.pick()


class LotteryBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(list(iterable))

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError("Pick from an empty lottery blower.")
        return self._balls[position]

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(sorted(self._balls))


@Tombola.register
class TomboList(list):
    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('Pop from empty TomboList.')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))


def example_with_tombo_list():
    print(isinstance(TomboList(), Tombola))
    print(issubclass(TomboList, Tombola))
    print(TomboList.__mro__)


if __name__ == "__main__":
    example_with_tombo_list()
