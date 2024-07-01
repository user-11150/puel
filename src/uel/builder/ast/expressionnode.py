import typing

from uel.builder.ast.abstractnode import AbstractNode
from uel.builder.ast.constant import Constant
from uel.builder.ast.singlenode import SingleNode

__all__ = ["ExpressionNode"]


class ExpressionNode(AbstractNode):
    def __init__(self, val: typing.Any) -> None:
        self.val = val
