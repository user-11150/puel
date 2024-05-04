# coding: utf-8

from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.tools.func.wrapper.with_out import with_out
from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.core.builder.ast.ModuleNode import ModuleNode
from uel.core.builder.bytecode.UELBytecodeCompiler import UELBytecodeCompiler

class ASTToByteCodeCollectionCompiler:
    @with_out
    def with_ast(self, ast: ModuleNode) -> list[BytecodeInfo]:
        compiler = self.createCompiler()
        compiler.read(ast)
        return compiler.toBytecodes()

    def createCompiler(self) -> UELBytecodeCompiler:
        return UELBytecodeCompiler()
