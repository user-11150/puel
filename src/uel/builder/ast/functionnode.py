from uel.builder.ast.abstractnode import AbstractNode
from uel.builder.ast.containernode import ContainerNode

__all__ = ["FunctionNode"]


class FunctionNode(ContainerNode):
    def __init__(
        self, children: list[AbstractNode], name: str, args: list[str]
    ) -> None:
        super().__init__(children)
        self.args = args
        self.name = name
