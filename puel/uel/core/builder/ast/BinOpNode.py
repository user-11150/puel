from uel.core.builder.ast.AbstractNode import AbstractNode

class BinOpNode(AbstractNode):
    left: AbstractNode
    right: AbstractNode
    
    def __init__(self,left,right):
        self.left = left
        self.right = right
