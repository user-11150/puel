from uel.core.runner.task.AbstractTask import AbstractTask
from uel.core.builder.Lexer import Lexer
from uel.core.builder.token.TokenNode import TokenNode as Token
from uel.core.builder.ast.AbstractNode import AbstractNode
from uel.core.builder.Parser import Parser
from typing import List
from objprint import objprint
from uel.core.builder.bytecode.ASTToByteCodeCollectionCompiler import ASTToByteCodeCollectionCompiler
from uel.core.builder.bytecode.ByteCodeNodeInfoConstantsConfiguration.shared.functions.development.pretty.print.bytecode_object_print import bytecode_object_print as \
              builder_bytecode_bytecodenodeinfoconstantsconfiguration_shared_funtion_development_prettyprint_bytecodeprint

class BuildCode(AbstractTask):
    def __init__(self, fn, code):
        self.fn = fn
        self.code = code
        self.result = None

    def run(self):
        import warnings
        warnings.warn('It is still under development. Please do not use it.')
        lexer: Lexer = Lexer(self.fn, self.code)
        tokens: List[Token] = lexer.make_tokens()
        parser: Parser = Parser(tokens)
        ast = parser.parse()
        print('\nAST:')
        objprint(ast)
        print('\nByteCode:')
        uel_compiler = ASTToByteCodeCollectionCompiler(ast)
        result = uel_compiler.compiler()
        builder_bytecode_bytecodenodeinfoconstantsconfiguration_shared_funtion_development_prettyprint_bytecodeprint(
            result
        )