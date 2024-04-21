from uel.core.builder.ast.AbstractNode import AbstractNode

class IfNode(AbstractNode):
    def __init__(self, condition, body, orelse):
        self.condition = condition
        self.body = body
        self.orelse = orelse
