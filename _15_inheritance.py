def example_with_subclassing_builtin_type():
    class DoppelDict(dict):
        def __setitem__(self, key, value):
            super().__setitem__(key, [value] * 2)

        def __getitem__(self, item):
            return super().__getitem__(item) * 2

    # __setitem__ special method is ignored when __init__ and __update__methods are invoked
    my_dict = DoppelDict(one=1)
    assert my_dict.get("one") == 1
    assert my_dict["one"] == 2
    my_dict['two'] = 2
    assert my_dict.get("two") == [2, 2]
    my_dict.update(three=3)
    assert my_dict.get("three") == 3

    class AnswerDict(dict):
        def __getitem__(self, item):
            return 42

    ad = AnswerDict(a="foo")
    assert ad["a"] == 42
    d = {}
    d.update(ad)
    assert d["a"] == 'foo'


def example_with_subclassing_from_collections():
    from collections import UserDict

    class DoppelDict(UserDict):
        def __setitem__(self, key, value):
            super().__setitem__(key, [value] * 2)

    # __setitem__ special method is not ignored when __init__ and __update__methods are invoked
    my_dict = DoppelDict(one=1)
    assert my_dict.get("one") == [1, 1]
    assert my_dict["one"] == [1, 1]
    my_dict['two'] = 2
    assert my_dict.get("two") == [2, 2]
    my_dict.update(three=3)
    assert my_dict.get("three") == [3, 3]

    class AnswerDict(UserDict):
        def __getitem__(self, item):
            return 42

    ad = AnswerDict(a="foo")
    assert ad["a"] == 42
    d = {}
    d.update(ad)
    assert d["a"] == 42


def example_with_multiple_inheritance():
    class A:
        def ping(self):
            print('ping:', self)

    class B(A):
        def pong(self):
            print('pong:', self)

    class C(A):
        def pong(self):
            print("PONG:", self)

    class D(B, C):
        def ping(self):
            super().ping()
            print('post-ping:', self)

        def pingpong(self):
            self.ping()
            super().ping()
            self.pong()
            super().pong()
            C.pong(self)

    print(D.__mro__)
    d = D()
    d.ping()
    d.pingpong()


if __name__ == "__main__":
    example_with_multiple_inheritance()
