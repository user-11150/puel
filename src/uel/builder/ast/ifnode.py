from uel.builder.ast.abstractnode import AbstractNode

__all__ = ["IfNode"]


class IfNode(AbstractNode):
    def __init__(
        self, condition: AbstractNode, body: AbstractNode,
        orelse: AbstractNode
    ) -> None:
        self.condition = condition
        self.body = body
        self.orelse = orelse
