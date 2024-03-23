from uel.core.builder.ast.AbstractNode import AbstractNode

from typing import Any

class ContainerNode(AbstractNode):
    def __init__(self, childrens: Any):
        self.childrens = childrens
