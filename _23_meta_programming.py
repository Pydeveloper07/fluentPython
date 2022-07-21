def example_dynamic_class_creation():
    def record_factory(cls_name, field_names):
        try:
            field_names = field_names.replace(",", " ").split()
        except AttributeError:
            field_names = tuple(field_names)

        def __init__(self, *args, **kwargs):
            attrs = dict(zip(self.__slots__, args))
            attrs.update(kwargs)
            for name, value in attrs.items():
                setattr(self, name, value)

        def __iter__(self):
            for name in self.__slots__:
                yield getattr(self, name)

        def __repr__(self):
            attrs = ", ".join(["{}={!r}".format(name, getattr(self, name)) for name in self.__slots__])
            repr_ = "{}({})".format(self.__class__.__name__, attrs)
            return repr_

        cls_attrs = dict(
            __init__=__init__,
            __slots__=field_names,
            __iter__=__iter__,
            __repr__=__repr__
        )

        return type(cls_name, (object,), cls_attrs)

    Dog = record_factory("Dog", "name age")
    dog = Dog(name="Simba", age=10)
    print(dog)
    Person = record_factory("Person", "first_name,last_name,age")
    person = Person("John", "Snow", 27)
    print(person)


def example_with_class_decoration():
    import abc

    class AutoStorage:
        __counter = 0
        def __init__(self):
            cls = self.__class__
            index = cls.__counter
            self.storage_name = "_{}#{}".format(cls.__name__, index)
            cls.__counter += 1

        def __get__(self, instance, owner):
            return getattr(instance, self.storage_name)

        def __set__(self, instance, value):
            setattr(instance, self.storage_name, value)

    class Validated(abc.ABC, AutoStorage):
        def __set__(self, instance, value):
            value = self.validate(value)
            super().__set__(instance, value)

        @abc.abstractmethod
        def validate(self, value):
            pass

    class Quantity(Validated):
        def validate(self, value):
            if value < 0:
                raise ValueError("value cannot be less than 0.")
            return value

    def entity(cls):
        for key, attr in cls.__dict__.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = "_{}#{}".format(type_name, key)
        return cls

    @entity
    class LineItem:
        price = Quantity()
        quantity = Quantity()
        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        def __repr__(self):
            repr_ = "{}({}, {})".format(self.__class__.__name__, self.name, self.price)
            return repr_

    order_line = LineItem("Fanta", 2000, 1)
    print(order_line)
    print(dir(order_line)[:2])
    try:
        order_line.price = -500
    except ValueError as e:
        print(e)
    print(order_line)


def example_with_meta_class():
    import abc
    import collections

    class AutoStorage:
        __counter = 0

        def __init__(self):
            cls = self.__class__
            index = cls.__counter
            self.storage_name = "_{}#{}".format(cls.__name__, index)
            cls.__counter += 1

        def __get__(self, instance, owner):
            return getattr(instance, self.storage_name)

        def __set__(self, instance, value):
            setattr(instance, self.storage_name, value)

    class Validated(abc.ABC, AutoStorage):
        def __set__(self, instance, value):
            value = self.validate(value)
            super().__set__(instance, value)

        @abc.abstractmethod
        def validate(self, value):
            pass

    class Quantity(Validated):
        def validate(self, value):
            if value < 0:
                raise ValueError("value cannot be less than 0.")
            return value

    class EntityMeta(type):
        @classmethod
        def __prepare__(metacls, name, bases):
            return collections.OrderedDict()

        def __init__(cls, name, bases, attr_dict):
            super().__init__(name, bases, attr_dict)
            cls._field_names = []
            for key, attr in cls.__dict__.items():
                if isinstance(attr, Validated):
                    type_name = type(attr).__name__
                    attr.storage_name = "_{}#{}".format(type_name, key)
                    cls._field_names.append(key)

    class Entity(metaclass=EntityMeta):
        @classmethod
        def field_names(cls):
            for name in cls._field_names:
                yield name

    class LineItem(Entity):
        price = Quantity()
        quantity = Quantity()

        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        def __repr__(self):
            repr_ = "{}({}, {})".format(self.__class__.__name__, self.name, self.price)
            return repr_

    order_line = LineItem("Fanta", 2000, 1)
    print(order_line)
    print(dir(order_line)[:2])
    try:
        order_line.price = -500
    except ValueError as e:
        print(e)
    print(order_line)
    for attr in LineItem.field_names():
        print(attr)


if __name__ == "__main__":
    example_with_meta_class()
