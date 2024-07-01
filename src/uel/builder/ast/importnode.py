from uel.builder.ast.abstractnode import AbstractNode

__all__ = ["ImportNode"]


class ImportNode(AbstractNode):
    def __init__(self, libname: str) -> None:
        self.libname = libname
