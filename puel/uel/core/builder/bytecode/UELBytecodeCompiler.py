from uel.core.builder.ast.ModuleNode import ModuleNode
from uel.core.builder.ast.ContainerNode import ContainerNode
from uel.core.builder.ast.ExpressionNode import ExpressionNode
from uel.core.builder.ast.VariableNode import VariableNode
from uel.core.builder.ast.Constant import Constant
from uel.core.builder.ast.PushStackValueNode import PushStackValueNode
from uel.core.builder.ast.PutNode import PutNode
from uel.core.builder.ast.BinOpNode import BinOpNode
from uel.core.builder.ast.AddNode import AddNode
from uel.core.builder.ast.MinusNode import MinusNode
from uel.core.builder.ast.MultNode import MultNode
from uel.core.builder.ast.DivNode import DivNode
from uel.core.builder.ast.IfNode import IfNode
from uel.core.builder.ast.IsEqual import IsEqual
from uel.core.builder.ast.RepeatNode import RepeatNode

from uel.core.errors.RaiseError import RaiseError
from uel.core.errors.UELException import UELException

from uel.pyexceptions.CustomError import CustomError

from uel.core.builder.bytecode import BytecodeInfo as bytecode
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode.BytecodeInfo import BT

from uel.tools.func.share.runtime_type_check import runtime_type_check


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
            if type_ is ExpressionNode:
                counter = self.expr(child)
                self.pop(counter)
            elif type_ is PushStackValueNode:
                self.expr(child.val)
                self.bytecode(bytecode.BT_QPUT)
            elif type_ is PutNode:
                self.expr(child.val)
                self.bytecode(bytecode.BT_PUT)
            
            elif type_ is IfNode:
                nod: IfNode
                body = child.body
                else_do = child.orelse
                condition = child.condition
                self.expr(condition)
                self.bytecode(bytecode.BT_IF_TRUE_JUMP, value=self.idx + 3)
                jump_to_else_bytecode = BytecodeInfo(bytecode.BT_IF_FALSE_JUMP,
                                                     None,
                                                     self.idx + 1)
                self.idx += 1
                self.bytecodes.append(jump_to_else_bytecode)
                self.alwaysExecute(body)
                jump_to_continue_bytecode = BytecodeInfo(bytecode.BT_JUMP,
                                                         None,
                                                         self.idx + 1)
                self.idx += 1
                self.bytecodes.append(jump_to_continue_bytecode)
                jump_to_else_bytecode.value = self.idx + 1
                self.alwaysExecute(else_do)
                jump_to_continue_bytecode.value = self.idx + 1
                
            elif type_ is RepeatNode:
                start_index = self.idx
                self.alwaysExecute(child)
                self.bytecode(bytecode.BT_JUMP, value=start_index + 1)
                
            else:
                raise CustomError("Developer not completed")

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

            nod = node.val if runtime_type_check(node, ExpressionNode) else node

            if type(nod) is VariableNode:
                self.store_name(val.left, val.right)
                raise ExitAndReturn
            elif type(nod) is Constant:
                self.load_const((nod.type, nod.val))
                counter += 1
                raise ExitAndReturn

            elif type(nod) in (AddNode, MinusNode, MultNode, DivNode, IsEqual):
                self.calculator(nod)
                raise ExitAndReturn

            else:
                raise NotSupportType
        
        except NotSupportType:
            raise TypeError(f"Not support type: {type(nod)}")
        
        except ExitAndReturn:
            pass
        
        return counter

    def equal(self):
        self.bytecode(bytecode.BT_IS)

    def calculator(self, node: Constant | BinOpNode) -> None:
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
            elif type_node is MultNode:
                self.mult()
            elif type_node is DivNode:
                self.div()
            elif type_node is IsEqual:
                self.equal()
        
        def deep(node: t.Any, root: bool=True) -> None:
            if runtime_type_check(node, Constant):
                self.calculator(node)
                yield
                return
            if root:
                self.calculator(node.left)
                g = deep(node.right, False)
                next(g)
                _symbol(node)
                yield from g
            else:
                self.calculator(node.left)
                yield
                g = deep(node.right, False)
                next(g)
                _symbol(node)
                yield from g
        
        if type(node) is Constant:
            self.expr(node)
            return
        elif type(node) is ExpressionNode and type(node.val) is Constant:
            self.expr(node.val)
            return 
        elif runtime_type_check(node.left, Constant) and runtime_type_check(node.right, Constant):
            self.calculator(node.left)
            self.calculator(node.right)
            _symbol(node)
        else:
            for _ in deep(node):
                pass

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
