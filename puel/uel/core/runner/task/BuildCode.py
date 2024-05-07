from uel.core.runner.task.AbstractTask import AbstractTask
from uel.core.builder.Lexer import Lexer
from uel.core.builder.token.TokenNode import TokenNode as Token
from uel.core.builder.ast.AbstractNode import AbstractNode
from uel.core.builder.Parser import Parser
from typing import List
from objprint import objprint # type: ignore
from pprint import pprint
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode.ASTToByteCodeCollectionCompiler import ASTToByteCodeCollectionCompiler

import typing as t

class BuildCode(AbstractTask):
    def __init__(self, fn: str, code: str):
        self.fn = fn
        self.code = code
        self.result = None

    def run(self, debug=True) -> List[BytecodeInfo]:
        lexer: Lexer = Lexer(self.fn, self.code)
        tokens: List[Token] = lexer.make_tokens()
        if debug:
            pprint(tokens)
        parser: Parser = Parser(tokens)
        ast = parser.parse()
        if debug:
            print('\nAST:')
            objprint(ast)
        compiler = ASTToByteCodeCollectionCompiler()
        if debug:
            print('\nBytecode')
        
        with compiler.with_ast(ast, self.fn) as fp:
            if debug:
               pprint(fp[0])
            return fp