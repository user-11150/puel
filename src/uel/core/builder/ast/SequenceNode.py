from typing import Any

from uel.core.builder.ast.AbstractNode import AbstractNode


class SequenceNode(AbstractNode):

    def __init__(self, values: list[Any]):
        self.values = values
