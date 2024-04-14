from uel.core.builder.ast.ModuleNode import ModuleNode
from uel.core.builder.ast.ContainerNode import ContainerNode
from uel.core.builder.ast.ExpressionNode import ExpressionNode
from uel.core.builder.ast.VariableNode import VariableNode

from uel.core.builder.bytecode import BytecodeInfo as bytecode
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode.BytecodeInfo import BT

import threading

class UELBytecodeCompiler:
    def __init__(self):
        self.ast = None
        self.mutex = threading.Lock()
        self.idx = 0
        self.bytecodes = []
        self.__read = 0

    def __iter__(self):
        return iter([self.ast])

    def read(self, abstract_syntax_tree: ModuleNode):
        with self.mutex:
            self.__read += 1
            if self.__read != 1:
                if type(self.__read) is not int:
                    raise TypeError(f"Expected int, result is {self.__read.__class__.__name__}")
                if self.__read > 1:
                    raise RuntimeError("Multiple calls to read")
            self.ast = abstract_syntax_tree

    def toBytecodes(self):
        [ast] = self
        # print(ast)
        self.module(ast)
        return self.bytecodes

    def module(self, module_node: ModuleNode):
        self.alwaysExecute(module_node)

    def alwaysExecute(self, node: ContainerNode):
        for child in node.childrens:
            type_ = type(child)
            if type_ == ExpressionNode:
                self.expr(child)

    def expr(self, node: ExpressionNode):
        value = node.val
        vt = type(value)
        if vt is VariableNode:
            self.var(value)

    def var(self, varnode: VariableNode):
        self.bytecode(bytecode.BT_VAR, value=(varnode.left.val, varnode.right))

    def bytecode(self, bytecode_type: BT,
                 value: str):
        self.idx += 1
        self.bytecodes.append(BytecodeInfo(
            bytecode_type=bytecode_type,
            value=value,
            pos=self.idx
        ))
