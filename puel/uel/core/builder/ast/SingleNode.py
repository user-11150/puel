from uel.core.builder.ast.AbstractNode import AbstractNode

class SingleNode:
    def __init__(self, val, type = None):
        self.val = val
        self.type = type

    def __repr__(self):
        return """%s<%s>(val=%s)""" % (self.__class__.__name__,
                                        self.type,
                                        repr(self.val))
