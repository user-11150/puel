import typing as t
from pprint import pprint
from typing import List

from objprint import objprint

from uel.builder.ast.abstractnode import AbstractNode
from uel.builder.bytecode.asttobytecodecollectioncompiler import \
    ASTToByteCodeCollectionCompiler
from uel.builder.bytecode.bytecodeinfo import BytecodeInfo
from uel.builder.lexer import Lexer
from uel.builder.parser import Parser
from uel.runner.task.abstracttask import AbstractTask
from uel.optimizer import ast_optimizer
from uel.optimizer import bytecode_optimizer

__all__ = ["BuildCode"]


class BuildCode(AbstractTask):
    def __init__(self, fn: str, code: str):
        self.fn = fn
        self.code = code
        self.result = None

    def run(self, debug: bool = True) -> tuple[list[BytecodeInfo], str]:
        lexer: Lexer = Lexer(self.fn, self.code)
        tokens = lexer.make_tokens()
        if debug:
            pprint(tokens)
        parser: Parser = Parser(tokens)
        ast = parser.parse()
        ast_optimizer(ast)
        if debug:
            print('\nAST:')
            objprint(ast)
        compiler = ASTToByteCodeCollectionCompiler()
        if debug:
            print('\nBytecode')

        with compiler.with_ast(ast, self.fn) as fp:
            bytecode_optimizer(fp[0])
            if debug:
                pprint(fp[0], indent=4)
            return fp
