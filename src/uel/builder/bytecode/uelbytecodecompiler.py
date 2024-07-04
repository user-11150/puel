import threading
import typing as t
from uel.builder.bytecode.bytecodeinfo import (
    BT_ADD, BT_CALL, BT_DIV, BT_IS, BT_JUMP, BT_LOAD_CONST,
    BT_MAKE_SEQUENCE, BT_MINUS, BT_MUL, BT_POP, BT_POP_JUMP_IF_FALSE,
    BT_PUT, BT_QPUT, BT_QTOP, BT_RETURN, BT_SEQUENCE_APPEND, BT_STORE_NAME
)
from uel.builder.ast.abstractnode import AbstractNode
from uel.builder.ast.addnode import AddNode
from uel.builder.ast.binopnode import BinOpNode
from uel.builder.ast.callfunctionnode import CallFunctionNode
from uel.builder.ast.constant import Constant
from uel.builder.ast.containernode import ContainerNode
from uel.builder.ast.divnode import DivNode
from uel.builder.ast.expressionnode import ExpressionNode
from uel.builder.ast.functionnode import FunctionNode
from uel.builder.ast.ifnode import IfNode
from uel.builder.ast.importnode import ImportNode
from uel.builder.ast.isequal import IsEqual
from uel.builder.ast.minusnode import MinusNode
from uel.builder.ast.modulenode import ModuleNode
from uel.builder.ast.multnode import MultNode
from uel.builder.ast.pushstackvaluenode import PushStackValueNode
from uel.builder.ast.putnode import PutNode
from uel.builder.ast.repeatnode import RepeatNode
from uel.builder.ast.returnnode import ReturnNode
from uel.builder.ast.variablenode import VariableNode
from uel.builder.ast.sequencenode import SequenceNode
from uel.builder.bytecode import bytecodeinfo as bytecode
from uel.builder.bytecode.bytecodeinfo import BT, BytecodeInfo
from uel.errors.raiseerror import RaiseError
from uel.errors.uelexception import UELException
from uel.objects import IS_CAN_MAKE_OBJECT, uel_new_object
from uel.objects import UEFunctionObject
from uel.objects import UEObject
from uel.pyexceptions.customerror import CustomError
from uel.tools.func.share.runtime_type_check import runtime_type_check

__all__ = ["UELBytecodeCompiler"]


class UELBytecodeCompiler:
    """
    Bytecode compiler
    """
    def __init__(self, filename: str) -> None:
        self.ast: t.Optional[ModuleNode] = None
        self.mutex = threading.Lock()
        self.idx = 0
        self.bytecodes: t.List[BytecodeInfo] = []
        self.__read = 0
        self.filename = filename

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
                    raise TypeError(
                        f"Expected int, result is {self.__read.__class__.__name__}"
                    )
                if self.__read > 1:
                    raise RuntimeError("Multiple calls to read")
            self.ast = abstract_syntax_tree

    def toBytecodes(self) -> t.List[BytecodeInfo]:
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

    def alwaysExecute(self, node: AbstractNode) -> None:
        """
        Must be exceute
        """
        node = node.tp(ContainerNode)
        for child in node.childrens:
            type_ = type(child)
            if type_ is ExpressionNode:
                child_ = child.tp(ExpressionNode)
                counter = self.expr(child_)
                self.pop(counter)
            elif type_ is PushStackValueNode:
                child_ = child.tp(PushStackValueNode)
                self.expr(child_.val)
                self.bytecode(BT_QPUT)
            elif type_ is PutNode:
                child_ = child.tp(PutNode)
                self.expr(child_.val)
                self.bytecode(BT_PUT)

            elif type_ is IfNode:
                child = child.tp(IfNode)
                body = child.body
                else_do = child.orelse
                condition = child.condition
                self.expr(condition)
                start_index = self.idx
                else_to = BytecodeInfo(
                    BT_POP_JUMP_IF_FALSE, 0, start_index + 1
                )
                self.bytecodes.append(else_to)
                self.idx += 1
                self.alwaysExecute(body)
                self.idx += 1
                jump_exit = BytecodeInfo(BT_JUMP, 0, self.idx)
                self.bytecodes.append(jump_exit)
                else_to.value = self.idx + 1
                self.alwaysExecute(else_do)
                jump_exit.value = self.idx + 1

            elif type_ is FunctionNode:
                child = child.tp(FunctionNode)
                interpreter_compiler = UELBytecodeCompiler(self.filename)
                interpreter_compiler.read(child.tp(ModuleNode))
                bytecodes = interpreter_compiler.toBytecodes()
                function_object = uel_new_object(
                    "function", (child.args, bytecodes)
                )
                self.load_const(("object", function_object))
                self._store_name(child.name)
            elif type_ is RepeatNode:
                child = child.tp(RepeatNode)
                start_index = self.idx
                self.alwaysExecute(child)
                self.bytecode(BT_JUMP, value=start_index + 1)
            elif type_ is CallFunctionNode:
                child = child.tp(CallFunctionNode)
                self.expr(child.val)
                self.bytecode(BT_CALL)
            elif type_ is ReturnNode:
                child = child.tp(ReturnNode)
                self.expr(child.val)
                self.bytecode(BT_RETURN)
            elif type_ is ImportNode:
                child = child.tp(ImportNode)
                """
                def module_def(compiler: t.Any, node: ImportNode) -> None:
                    for bytecode in module_import(node.libname, compiler.filename):
                        compiler.bytecode(bytecode.bytecode_type, bytecode.value)
                """
                from uel.runner.importlib import module_import
                for bytecode in module_import(child.libname, self.filename):
                    self.bytecode(bytecode.bytecode_type, bytecode.value)
            elif type_ is SequenceNode:
                self.sequence(child)
            else:
                raise CustomError("Developer not completed")

    def sequence(self, child: SequenceNode) -> None:
        self.bytecode(BT_MAKE_SEQUENCE)
        for val in child.values:
            self.expr(val)
            self.bytecode(BT_SEQUENCE_APPEND)

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

            nod = node.val if runtime_type_check(
                node, ExpressionNode
            ) else node

            if type(nod) is VariableNode:
                self.store_name(val.left, val.right)
                raise ExitAndReturn
            elif type(nod) is Constant:
                self.load_const((nod.type, nod.val))
                counter += 1
                raise ExitAndReturn
            elif type(nod) in (
                AddNode, MinusNode, MultNode, DivNode, IsEqual
            ):
                self.calculator(nod)
                raise ExitAndReturn
            elif type(nod) is SequenceNode:
                self.sequence(nod)
                counter += 1

            else:
                raise NotSupportType

        except NotSupportType:
            raise TypeError(f"Not support type: {type(nod)}")

        except ExitAndReturn:
            pass

        return counter

    def equal(self) -> None:
        self.bytecode(BT_IS)

    def calculator(
        self, node: t.Union[Constant, BinOpNode, t.Any]
    ) -> None:
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

        def deep(node: t.Any, root: bool = True) -> t.Any:
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

        if type(node) is Constant or type(node) is SequenceNode:
            self.expr(node)
            return
        elif type(node) is ExpressionNode and (
            type(node.val) is Constant or type(node.val) is SequenceNode
        ):
            self.expr(node.val)
            return
        elif type(node) is BinOpNode and runtime_type_check(
            node.left, Constant, SequenceNode
        ) and runtime_type_check(node.right, Constant, SequenceNode):
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
            self.bytecode(BT_POP)

    def load_const(self, val: t.Any) -> None:
        """
        Push a value to stack
        """
        if not issubclass(type(val), UEObject) and IS_CAN_MAKE_OBJECT(
            val[0]
        ):
            val = ("object", uel_new_object(*val))
        self.bytecode(BT_LOAD_CONST, val)

    def store_name(self, name: Constant, value: t.Any) -> None:
        """
        Variable
        """
        self.expr(value)
        self._store_name(name.val)

    def _store_name(self, value: t.Any) -> None:
        self.bytecode(BT_STORE_NAME, value)

    def bytecode(
        self, bytecode_type: BT, value: t.Optional[t.Any] = None
    ) -> None:
        """
        Push a bytecode
        """
        self.idx += 1
        self.bytecodes.append(
            BytecodeInfo(
                bytecode_type=bytecode_type, value=value, pos=self.idx
            )
        )

    def add(self) -> None:
        self.bytecode(BT_ADD)

    def minus(self) -> None:
        self.bytecode(BT_MINUS)

    def mult(self) -> None:
        self.bytecode(BT_MUL)

    def div(self) -> None:
        self.bytecode(BT_DIV)
