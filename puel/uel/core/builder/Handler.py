from uel.core.builder.Lexer import Lexer
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
        del lexer
        pprint(tokens)
        # ...(剩下的正在开发中)