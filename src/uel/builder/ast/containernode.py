from typing import Any, List

from uel.builder.ast.abstractnode import AbstractNode

__all__ = ["ContainerNode"]


class ContainerNode(AbstractNode):
    def __init__(self, childrens: List[AbstractNode] | None = None):
        self.childrens: List[AbstractNode] = childrens or []

    def push(self, node: AbstractNode) -> None:
        self.childrens.append(node)
