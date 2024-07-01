from typing import Any

from uel.builder.ast.abstractnode import AbstractNode

__all__ = ["SequenceNode"]


class SequenceNode(AbstractNode):
    def __init__(self, values: list[Any]):
        self.values = values
        self.val = self
