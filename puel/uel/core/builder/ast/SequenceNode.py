from uel.core.builder.ast.AbstractNode import AbstractNode

class SequenceNode(AbstractNode):
    def __init__(self, values):
        self.values = values