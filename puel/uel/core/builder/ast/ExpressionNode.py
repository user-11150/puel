from uel.core.builder.ast.AbstractNode import AbstractNode

class ExpressionNode(AbstractNode):
    def __init__(self,val):
        self.val = val
