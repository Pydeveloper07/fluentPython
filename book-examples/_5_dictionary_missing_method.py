class StrDictKey0(dict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()


if __name__ == "__main__":
    my_dict = StrDictKey0()
    my_dict["10"] = "ten"
    print(my_dict[10])
