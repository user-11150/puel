# coding: utf-8

from typing import Any

from uel.core.builder.ast.ModuleNode import ModuleNode
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode.UELBytecodeCompiler import UELBytecodeCompiler
from uel.tools.func.share.runtime_type_check import runtime_type_check
from uel.tools.func.wrapper.with_out import with_out


class ASTToByteCodeCollectionCompiler:

    @with_out
    def with_ast(self, ast: ModuleNode,
                 filename: str) -> tuple[list[BytecodeInfo], str]:
        compiler = self.createCompiler(filename)
        compiler.read(ast)
        return compiler.toBytecodes(), compiler.filename

    def createCompiler(self, *args: Any, **kwargs: Any) -> UELBytecodeCompiler:
        return UELBytecodeCompiler(*args, **kwargs)
