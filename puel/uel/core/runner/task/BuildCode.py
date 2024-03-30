from uel.core.runner.task.AbstractTask import AbstractTask
from uel.core.builder.Lexer import Lexer
from uel.core.builder.token.TokenNode import TokenNode as Token
from uel.core.builder.ast.AbstractNode import AbstractNode
from uel.core.builder.Parser import Parser
from typing import List
from pprint import pprint

class BuildCode(AbstractTask):
    def __init__(self, fn, code):
        self.fn = fn
        self.code = code
        self.result = None

    def run(self):
        lexer: Lexer = Lexer(self.fn, self.code)
        tokens: List[Token] = lexer.make_tokens()
        parser: Parser = Parser(tokens)
        ast = parser.parse()
        pprint(ast)