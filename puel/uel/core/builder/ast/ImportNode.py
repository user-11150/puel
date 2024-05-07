from uel.core.builder.ast.AbstractNode import AbstractNode

class ImportNode(AbstractNode):
    def __init__(self, libname):
        self.libname = libname
