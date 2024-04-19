from uel.core.builder.ast.ModuleNode import ModuleNode
from uel.core.builder.ast.ContainerNode import ContainerNode
from uel.core.builder.ast.ExpressionNode import ExpressionNode
from uel.core.builder.ast.VariableNode import VariableNode
from uel.core.builder.ast.Constant import Constant

from uel.core.builder.ast.BinOpNode import BinOpNode

# Four Arithmetic
from uel.core.builder.ast.AddNode import AddNode
from uel.core.builder.ast.MinusNode import MinusNode
from uel.core.builder.ast.MultNode import MultNode
from uel.core.builder.ast.DivNode import DivNode

from uel.core.builder.bytecode import BytecodeInfo as bytecode
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode.BytecodeInfo import BT

import threading
import typing as t

__all__ = ["UELBytecodeCompiler"]

class FourArithmethicMixinWithUELBytcodeCompilerI:
    def bytecode(self, bytecode_type: BT,
                 value: str | None=None) -> None:
        pass
    

class FourArithmethicMixin(
        FourArithmethicMixinWithUELBytcodeCompilerI
    ):
    def add(self) -> None:
        self.bytecode(bytecode.BT_ADD)

    def minus(self) -> None:
        self.bytecode(bytecode.BT_MINUS)

    def mult(self) -> None:
        self.bytecode(bytecode.BT_MUL)

    def div(self) -> None:
        self.bytecode(bytecode.BT_DIV)


class UELBytecodeCompiler(FourArithmethicMixin):
    """
    Bytecode compiler
    """
    def __init__(self) -> None:
        self.ast: t.Optional[ModuleNode] = None
        self.mutex = threading.Lock()
        self.idx = 0
        self.bytecodes: t.List[BytecodeInfo] = []
        self.__read = 0

    def __iter__(self) -> t.Any:
        yield self.ast

    def read(self, abstract_syntax_tree: ModuleNode) -> None:
        """
        Save the AST for compiler
        """
        with self.mutex:
            self.__read += 1
            if self.__read != 1:
                if type(self.__read) is not int:
                    raise TypeError(f"Expected int, result is {self.__read.__class__.__name__}")
                if self.__read > 1:
                    raise RuntimeError("Multiple calls to read")
            self.ast = abstract_syntax_tree

    def toBytecodes(self) -> t.List[bytecode.BytecodeInfo]:
        """
        Return the saved AST compile to bytecodes
        """
        [ast] = self
        # print(ast)
        self.module(ast)
        return self.bytecodes

    def module(self, module_node: ModuleNode) -> None:
        """
        Its will arg 1 to save bytecodes with Compiler.bytecodes
        """
        self.alwaysExecute(module_node)

    def alwaysExecute(self, node: ContainerNode) -> None:
        """
        Must be exceute
        """
        for child in node.childrens:
            type_ = type(child)
            if type_ == ExpressionNode:
                counter = self.expr(child)
            self.pop(counter)

    def expr(self, node: t.Any) -> int:
        """
        Parse the expression
        """
        counter = 0
        
        class ExitAndReturn(Exception):
            pass
        class NotSupportType(Exception):
            pass
        
        try:
            if hasattr(node, "val"):
                val = node.val
                value_type = type(val)

            if type(node) is ExpressionNode:
                if value_type is VariableNode:
                    self.store_name(val.left, val.right)
                    raise ExitAndReturn

                elif type(val) is Constant:
                    self.load_const((val.type, val.val))
                    counter += 1

                else:
                    raise NotSupportType

            elif type(node) is Constant:
                self.load_const((node.type, node.val))
                counter += 1

            elif type(node) in (AddNode, MinusNode):
                self.calculator(node)

            else:
                raise NotSupportType
        except ExitAndReturn:
            pass
        except NotSupportType as e:
            # If the metaclass __str__ is overload
            objstr = object.__str__
            with_types = f" ~ {objstr(type(node.val))}" if hasattr(node, "val") else ""
            raise TypeError(f"Not support type: {objstr(type(node))}{with_types}") from e
        
        return counter

    def calculator(self, node: t.Any, root: bool=True) -> None:
        """
        Four arithmetic
        """
        def _symbol(node: t.Any) -> None:
            type_node = type(node)
            if type_node is AddNode:
                self.add()
                return
            elif type_node is MinusNode:
                self.minus()
                return
            # Test
        if type(node) is Constant:
            self.expr(node)
            return
        if root:
            self.calculator(node.left, False)
            self.calculator(node.right, False)
            _symbol(node)
        else:
            self.calculator(node.left, False)
            _symbol(node)
            self.calculator(node.right, False)

    def pop(self, each_number: int) -> None:
        """
        Pop stack value
        """
        for _ in range(each_number or 0):
            self.bytecode(bytecode.BT_POP)

    def load_const(self, val: t.Any) -> None:
        """
        Push a value to stack
        """
        self.bytecode(bytecode.BT_LOAD_CONST, val)

    def store_name(self, name: Constant, value: t.Any) -> None:
        """
        Variable
        """
        self.expr(value)
        self.bytecode(bytecode.BT_STORE_NAME, value=name.val)

    def bytecode(self, bytecode_type: BT,
                 value: t.Optional[str]=None) -> None:
        """
        Push a bytecode
        """
        self.idx += 1
        self.bytecodes.append(BytecodeInfo(
            bytecode_type=bytecode_type,
            value=value,
            pos=self.idx
        ))
