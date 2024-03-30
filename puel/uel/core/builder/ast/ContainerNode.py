from uel.core.builder.ast.AbstractNode import AbstractNode

from typing import (Any,
                    List)

class ContainerNode(AbstractNode):
    def __init__(self, childrens: List[AbstractNode] | None = None):
        self.childrens: List[AbstractNode] = childrens or []

    def push(self,node: AbstractNode) -> None:
        self.childrens.append(node)
