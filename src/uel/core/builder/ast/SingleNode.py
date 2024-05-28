import typing as t

from uel.core.builder.ast.AbstractNode import AbstractNode


class SingleNode:

    def __init__(self, val: t.Any, type: t.Optional[str] = None):
        self.val = val
        self.type = type

    def __repr__(self) -> str:
        return """%s<%s>(val=%s)""" % (self.__class__.__name__, self.type,
                                       repr(self.val))
