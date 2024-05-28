from uel.core.builder.ast.AbstractNode import AbstractNode


class ImportNode(AbstractNode):

    def __init__(self, libname: str) -> None:
        self.libname = libname
