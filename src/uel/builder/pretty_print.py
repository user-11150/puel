"""
Print compile results

This is a incomplete, but growing list for printable objects
  1. Tokens

"""

from uel.builder.token import UELToken
from uel.builder.ast import AST, dump


def print_tokens(tokens: list[UELToken]) -> None:
    print("\n".join(map(str, tokens)))


def print_ast(ast: AST) -> None:
    print(dump(ast, indent="    "))
