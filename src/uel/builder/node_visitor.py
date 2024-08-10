from uel.builder.ast import AST


class NodeVisitor:
    def visit(self, node: AST):
        getattr(self, f"visit_{node.kind}", self.generic_visit)(node)

    def generic_visit(self, node: AST):
        for field in node._fields:
            value = getattr(node, field)
            if isinstance(value, list):
                for item in value:
                    self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)
