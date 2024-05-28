from uel.core.builder.ast.AbstractNode import AbstractNode


class IfNode(AbstractNode):

    def __init__(self, condition: AbstractNode, body: AbstractNode,
                 orelse: AbstractNode) -> None:
        self.condition = condition
        self.body = body
        self.orelse = orelse
