from uel.builder.ast.abstractnode import AbstractNode


class SimpleFunctionCall(AbstractNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args
