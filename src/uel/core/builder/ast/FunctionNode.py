from uel.core.builder.ast.AbstractNode import AbstractNode
from uel.core.builder.ast.ContainerNode import ContainerNode


class FunctionNode(ContainerNode):

    def __init__(self, children: list[AbstractNode], name: str,
                 args: list[str]) -> None:
        super().__init__(children)
        self.args = args
        self.name = name
