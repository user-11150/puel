class AttributeOnlyError(Exception):
    pass

class AttributeOnly:
    def __init__(self, obj, names):
        self.__obj = obj
        self.__names = names

    def __getattr__(self, name):
        if not (name in self.__names):
            raise AttributeOnlyError(str(self.__names))
        return self.__obj.__getattribute__(name)

if __name__ == "__main__":
    from dataclasses import dataclass
    @dataclass
    class A:
        a: int
    s = AttributeOnly(A(1), ["a"])
    print(s.a)
