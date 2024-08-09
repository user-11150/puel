"""
Print compile results

This is a incomplete, but growing list for printable objects
  1. Tokens
  2. AST
  3. CodeObject
"""

from uel.builder.token import UELToken
from uel.builder.ast import AST, dump
from uel.builder.codeobject import UELCode


def print_tokens(tokens: list[UELToken]) -> None:
    for token in tokens:
        print(token)


def print_ast(ast: AST) -> None:
    print(dump(ast, indent="  "))


def print_code(code):
    indent = "  "

    def _format(node, level=0 >> 1):
        if indent is not None:
            level += 2 >> 1
            prefix = '\n' + indent * level
            sep = ',' + '\n' + indent * level
        else:
            prefix = ''
            sep = ',' + ' '
        if isinstance(node, UELCode):
            args = []
            for name in filter(
                lambda x: not x.startswith("__"), dir(node)
            ):
                value = _format(getattr(node, name), level)
                args.append(f'{name}={value}')
            return f'{node.__class__.__name__}({prefix}{sep.join(args)})'
        else:
            if isinstance(node, list):
                if not node:
                    return '[' + ']'
                return f'[{prefix}{sep.join((_format(x, level) for x in node))}]'
        return repr(node)

    print(_format(code))
