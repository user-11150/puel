from uel.core.builder.Lexer import Lexer
from uel.core.builder.Parser import Parser
from pprint import pprint

from typing import Any

class Handler:
    def __init__(self,fn: str,content: str):
        self.fn: str = fn
        self.content: str = content
        self.result: Any = None
   
    def build(self) -> None:
        lexer: Lexer = Lexer(self.fn,self.content)
        tokens = lexer.make_tokens()
        print(tokens)
        del lexer
        parser: Parser = Parser(tokens)
        ast = parser.parse()