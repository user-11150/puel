from typing import Callable
from typing import List
from typing import Sequence
from typing import Any

from queue import Empty

from uel.core.builder.ast.ModuleNode import ModuleNode
from uel.core.builder.ast.ExpressionNode import ExpressionNode
from uel.core.builder.ast.Constant import Constant

from uel.core.builder.bytecode.ByteCodeNodeInfo import ByteCodeNodeInfo

from uel.core.builder.bytecode.ByteCodeNodeInfo import Queue

from uel.core.builder.bytecode.ByteCodeNodeInfo import BYTECODE_TYPE_ADD
from uel.core.builder.bytecode.ByteCodeNodeInfo import BYTECODE_TYPE_DIV
from uel.core.builder.bytecode.ByteCodeNodeInfo import BYTECODE_TYPE_MINUS
from uel.core.builder.bytecode.ByteCodeNodeInfo import BYTECODE_TYPE_MUL

from uel.core.builder.bytecode.ByteCodeNodeInfo import BYTECODE_TYPE_POP
from uel.core.builder.bytecode.ByteCodeNodeInfo import BYTECODE_TYPE_TOP

from uel.core.builder.bytecode.ByteCodeNodeInfo import BYTECODE_TYPE_LOAD_CONST
from uel.tools.func.share.runtime_type_check import runtime_type_check

class ASTToByteCodeCollectionCompiler:
    def __init__(self, ast: ModuleNode):
        self.ast = ast
        if type(self.ast) is not ModuleNode:
            raise TypeError("arg 1 must be a ModuleNode")
        self.queue = Queue()
    
    def compiler(self) -> None:
        """
        AST => Bytecode
        """
        for stmt in self.ast.childrens:
            if runtime_type_check(stmt, type):
                raise TypeError("STMT must be a object, not type")
            elif runtime_type_check(stmt, ExpressionNode):
                self.expr(stmt)
        result = []
        try:
            while True:
                result.append(self.queue.get_nowait())
        except Empty:
            return result

    def expr(self, stmt: ExpressionNode) -> None:
        value = stmt.val
        if runtime_type_check(value, Constant):
            self.load_const(value)

    def load_const(self, val):
        self.queue.put(ByteCodeNodeInfo(
            BYTECODE_TYPE_LOAD_CONST,
            val
        ))