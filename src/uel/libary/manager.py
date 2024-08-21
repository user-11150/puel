from uel.libary.builtins import std

_mapping = {}


def register(name, module):
    _mapping[name] = module


register('std', std.mod)


def getmodules():
    return _mapping
