from uel.objects.object import UELObject
from uel.objects.none import uel_none


class UELModule(UELObject):
    tp_name = "Module"

    def __init__(self):
        self.__mapping = {}

    def tp_getattr(self, attr):
        try:
            return self.__mapping[attr]
        except:
            return uel_none

    def add_attribute(self, attr, val):
        self.__mapping[attr] = val

    def method(self, name):
        def decorator(f):
            self.add_attribute(name, f)
            return f

        return decorator
