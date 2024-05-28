import typing

from uel.core.builder.ast.AbstractNode import AbstractNode
from uel.core.builder.ast.Constant import Constant
from uel.core.builder.ast.SingleNode import SingleNode


class ExpressionNode(AbstractNode):

    def __init__(self, val: typing.Any) -> None:
        self.val = val
