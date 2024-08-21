from uel.builder.ast import AST


class NodeVisitor:
    def visit(self, node: AST):
        getattr(self, f"visit_{node.kind}", self.generic_visit)(node)

    def generic_visit(self, node: AST):
        if not isinstance(node, AST):
            return
        for field in node._fields:
            value = getattr(node, field)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)
