from uel.builder.ast.abstractnode import AbstractNode


class BinOpNode(AbstractNode):
    left: AbstractNode
    right: AbstractNode

    def __init__(self, left: AbstractNode, right: AbstractNode) -> None:
        self.left = left
        self.right = right
