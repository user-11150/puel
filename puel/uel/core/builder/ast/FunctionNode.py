from uel.core.builder.ast.ContainerNode import ContainerNode

class FunctionNode(ContainerNode):
    def __init__(self, children, name, args):
        super().__init__(children)
        self.args = args
        self.name = name
