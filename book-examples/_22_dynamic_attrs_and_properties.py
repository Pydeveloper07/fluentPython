from collections import abc


class FrozenJSON:
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            result = []
            for item in arg:
                if isinstance(item, abc.Mapping):
                    result.append(cls(item))
                else:
                    result.append(item)
            return result
        else:
            return arg

    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, item):
        if self.__data.get(item):
            return FrozenJSON(self.__data[item])
        else:
            msg = "Object of type {} does not have attribute {}"
            raise AttributeError(msg.format(self.__class__, item))


def example_with_frozen_json():
    from urllib.request import urlopen
    import os
    import warnings
    import json

    URL = 'https://mobileapp.pythonanywhere.com/mobilephone/brands/'
    JSON = 'data/data.json'

    def load():
        if not os.path.exists(JSON):
            msg = "downloading from {} to {}"
            warnings.warn(msg.format(URL, JSON))
            with urlopen(URL) as remote, open(JSON, "wb") as local:
                local.write(remote.read())

        with open(JSON) as fp:
            return json.load(fp)

    data = load()
    json_data = FrozenJSON(data)
    print(json_data.fields.address.tags[0])
    print(json_data.fields.roles[0].name)
    try:
        print(json_data.non_existing_field)
    except AttributeError as e:
        print(e)


def example_with_attr_set_validation():
    class LineItem:
        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.__quantity = quantity

        def subtotal(self):
            return self.price * self.quantity

        @property
        def quantity(self):
            return self.__quantity

        @quantity.setter
        def quantity(self, value):
            if value < 0:
                raise ValueError("Quantity cannot be a negative number.")
            self.__quantity = value

        def __str__(self):
            return "LineItem({}, {}, {})".format(self.name, self.price, self.quantity)

    order_line = LineItem("Coca Cola (1l)", 15, 2)
    print(f"{order_line} subtotal =", order_line.subtotal())
    order_line.quantity = 10
    print(f"{order_line} subtotal =", order_line.subtotal())
    try:
        order_line.quantity = -5
    except ValueError as e:
        print(e)


def example_with_property_factory():
    def property_factory(storage):
        def qty_getter(instance):
            return instance.__dict__[storage]

        def qty_setter(instance, value):
            if value < 0:
                raise ValueError(f"{storage} cannot be a negative number.")
            instance.__dict__[storage] = value
        return property(qty_getter, qty_setter)

    class LineItem:
        price = property_factory("price")
        quantity = property_factory("quantity")

        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        def subtotal(self):
            return self.price * self.quantity

        def __str__(self):
            return "LineItem({}, {}, {})".format(self.name, self.price, self.quantity)

    order_line = LineItem("Coca Cola (1l)", 10, 15)
    print(order_line.price)
    print(order_line.quantity)
    order_line.price = 100
    print(order_line.price)
    try:
        order_line.price = -10
    except ValueError as e:
        print(e)
    print(order_line.price)
    try:
        order_line.quantity = -2
    except ValueError as e:
        print(e)
    print(order_line.quantity)


def example_with_descriptors():
    class Quantity:
        def __init__(self, storage_name: str):
            self.storage_name = storage_name

        def __set__(self, instance, value):
            if value < 0:
                msg = "{} value must be non-negative."
                raise ValueError(msg.format(self.storage_name))
            else:
                instance.__dict__[self.storage_name] = value

    class LineItem:
        price = Quantity("price")
        quantity = Quantity("quantity")

        def __init__(self, name: str, price: float, quantity: int):
            self.name = name
            self.price = price
            self.quantity = quantity

        def subtotal(self):
            return self.price * self.quantity

        def __str__(self):
            repr_ = "{}({}, {}, {})"
            return repr_.format(self.__class__.__name__, self.name, self.price, self.quantity)

    order_line = LineItem("Fanta", 1000, 2)
    print(order_line)
    order_line.price = 1500
    print(order_line)
    try:
        order_line.price = -500
    except ValueError as e:
        print(e)
    print(order_line)
    try:
        order_line.quantity = -5
    except ValueError as e:
        print(e)
    print(order_line)


def example_descriptor_advanced():
    class Quantity:
        __counter = 0

        def __init__(self):
            cls = self.__class__
            prefix = cls.__name__
            index = cls.__counter
            self.storage_name = "_{}#{}".format(prefix, index)
            cls.__counter += 1

        def __get__(self, instance, owner):
            return getattr(instance, self.storage_name)

        def __set__(self, instance, value):
            if value < 0:
                raise ValueError("value must be > 0.")
            else:
                setattr(instance, self.storage_name, value)

    class LineItem:
        price = Quantity()
        quantity = Quantity()

        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        def subtotal(self):
            return self.price * self.quantity

        def __str__(self):
            repr_ = "{}({}, {}, {})"
            return repr_.format(self.__class__.__name__, self.name, self.price, self.quantity)

    order_line = LineItem("Fanta", 1000, 2)
    print(order_line)
    print(order_line.price)
    order_line.price = 1500
    print(order_line)
    print(getattr(order_line, "_Quantity#0"))
    try:
        order_line.price = -500
    except ValueError as e:
        print(e)
    print(order_line)
    print(LineItem.price)


def example_descriptor_advanced_2():
    import abc

    class AutoStorage:
        __counter = 0

        def __init__(self):
            cls = self.__class__
            index = cls.__counter
            self.storage_name = "_{}#{}".format(cls.__name__, index)
            cls.__counter += 1

        def __get__(self, instance, owner):
            if instance is None:
                return self
            else:
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

    class NonBlank(Validated):
        def validate(self, value: str):
            value = value.strip()
            if len(value) == 0:
                raise ValueError("value cannot be blank.")
            return value

    class LineItem:
        name = NonBlank()
        price = Quantity()
        quantity = Quantity()

        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity

        def subtotal(self):
            return self.price * self.quantity

        def __str__(self):
            repr_ = "{}({}, {}, {})"
            return repr_.format(self.__class__.__name__, self.name, self.price, self.quantity)

    order_line = LineItem("Fanta", 1500, 1)
    print(order_line)
    try:
        order_line.name = "   "
    except ValueError as e:
        print(e)
    print(order_line)
    try:
        order_line.price = -500
    except ValueError as e:
        print(e)
    print(order_line)


if __name__ == "__main__":
    example_descriptor_advanced_2()
