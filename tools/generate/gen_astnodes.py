from generate import task, python
import textwrap
import ast
import os.path
import re

ASDL = "grammer/astnodes"

DESCRIPTION = """
AST nodes
"""

class GenerateASTNodes:
    declare = re.compile("(\w+?):\s*(.*)")
    
    def __init__(self, asdl):
        self.asdl = asdl
        self.result = ""
    
    def add_node_class(self, declaration):
        class_ = ""
        tmp = self.declare.findall(declaration)
        
        if not tmp:
            return
        
        kind, body = tmp.pop()
        
        class_ += f"class {kind}(AST):\n"
        
        fields = []
        attributes = []
        
        arguments = [*map(str.strip, body.split(","))] + ["start", "end"]
        
        for argument in arguments:
            if argument.isspace() or not argument:
                continue
            if not argument.startswith("_"):
                attributes.append(argument)
                fields.append(argument)
            else:
                attributes.append(argument)
        
        tmp = textwrap.dedent(
        f"""
        kind = {repr(kind)}
        _fields: list[str] = {repr(fields)}
        """)
        
        tmp += textwrap.dedent(
            f"""
            def __init__(self, {",".join(attributes)}):
                {";".join(map(lambda s: f"self.{s} = {s}", attributes))}
            """
            )
        
        class_ += textwrap.indent(tmp, "    ")
        
        self.result += class_
    
    def generate(self):
        
        self.result += textwrap.dedent(
            r"""
            from typing import Protocol, runtime_checkable
            
            @runtime_checkable
            class BaseAST(Protocol):
                kind: str
                _fields: list[str]
                
            
            class AST:

                kind = 'AST'
                _fields: list[str] = []
            
            """
        )
        declarations = self.asdl.split(";")
        declarations.sort()
        
        for declaration in declarations:
            self.add_node_class(declaration)
        
        self.result += textwrap.dedent(
        r"""
        def dump(node: BaseAST, indent=None):
            def _format(node, level=0):
                if indent is not None:
                    level += 1
                    prefix = "\n" + indent * level
                    sep = ",\n" + indent * level
                else:
                    prefix = ""
                    sep = ", "
                if isinstance(node, AST):
                    args = []
                    for name in node._fields:
                        value = _format(getattr(node, name), level)
                        args.append(f"{name}={value}")
                    return f"{node.kind}({prefix}{sep.join(args)})"
                elif isinstance(node, list):
                    if not node:
                        return '[]'
                    return f'[{prefix}{sep.join(_format(x, level) for x in node)}]'
                return repr(node)
            return _format(node)
            
        """
        )
        
        return ast.unparse(ast.parse(self.result))

@task("src/uel/builder/ast.py")
@python("tools/generate/gen_astnodes.py", ASDL, DESCRIPTION)
def generate_astnodes(dirname):
    asdl_path = os.path.join(dirname, ASDL)
    result = ""
    with open(asdl_path) as f:
        result += GenerateASTNodes(f.read()).generate()
    return result
