#pylint:disable=C0103
#pylint:disable=C0411
#pylint:disable=C0116
from uel.core.runner.Frame import Frame
from uel.core.runner.Stack import Stack

from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode import BytecodeInfo as bytecode

from uel.tools.func.share.runtime_type_check import runtime_type_check

from uel.core.object.object_parse import parse

from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError

from uel.core.object.UEObject import UEObject
from uel.core.object.UEBooleanObject import UEBooleanObject
from uel.core.object.UECallableObject import UECallableObject
from uel.core.object.UEFunctionObject import UEFunctionObject

from queue import Queue, Empty

from typing import *
from types import *

class Ueval:
    """
    Runner
    """
    def __init__(self, bytecodes: List[BytecodeInfo], frame: Optional[Frame]=None, filename=None):
        self.bytecodes = bytecodes
        self.frame =  frame or Frame(
            # Stack
            Stack[Any](),
            # index
            0,
            # bytecodes
            self.bytecodes,
            # Prev_frame
            None,
            filename if filename is not None else exec("raise"),
            # Variables
            {},
            # Gqueue
            Queue()
        )

    @property
    def stack_top(self) -> Any:
        return self.frame.stack.top

    def stack_push(self, value: Any) -> None:
        self.frame.stack.push(value)

    def uelEval_EvalBytecodeDefault(self) -> None:
        while self.frame.idx < len(self.bytecodes):
            self.eval(self.bytecodes[self.frame.idx])
            self.frame.idx += 1

    def equal(self, x: UEObject, y: UEObject) -> bool:
        if hasattr(x, "val") and hasattr(y, "val"):
            return x.val == y.val
        
        return x == y

    def eval(self, bytecode_info: BytecodeInfo) -> None:
        if bytecode_info.bytecode_type == bytecode.BT_LOAD_CONST:
            self.stack_push(bytecode_info.value)

        elif bytecode_info.bytecode_type == bytecode.BT_ADD:
            self.binary_op(self.frame, bytecode_info)

        elif bytecode_info.bytecode_type == bytecode.BT_MINUS:
            self.binary_op(self.frame, bytecode_info)
        elif bytecode_info.bytecode_type == bytecode.BT_MUL:
            self.binary_op(self.frame, bytecode_info)
        elif bytecode_info.bytecode_type == bytecode.BT_DIV:
            self.binary_op(self.frame, bytecode_info)
        elif bytecode_info.bytecode_type == bytecode.BT_IS:
            left_value = parse(self.stack_top, self.frame)
            right_val = parse(self.stack_top, self.frame)
            
            if hasattr(left_value, "tp_equal"):
                self.stack_push(left_value.tp_equal(right_val).tp_bytecode())
            elif hasattr(right_val, "tp_equal"):
                self.stack_push(right_val.tp_equal(left_value).tp_bytecode())
            else:
                result = UEBooleanObject(str(self.equal(left_value, right_val)))
                self.stack_push(result.tp_bytecode())
        elif bytecode_info.bytecode_type == bytecode.BT_STORE_NAME:
            name = bytecode_info.value
            val = parse(self.stack_top, self.frame)
            self.frame.variables[name] = val

        elif bytecode_info.bytecode_type == bytecode.BT_QPUT:
            self.frame.gqueue.put(self.stack_top)

        elif bytecode_info.bytecode_type == bytecode.BT_POP:
            try:
                self.stack_top # pylint: disable=W
            except Empty:
                pass

        elif bytecode_info.bytecode_type == bytecode.BT_PUT:
            self.print(self.stack_top)

        elif bytecode_info.bytecode_type == bytecode.BT_JUMP:
            self.jump(bytecode_info.value)
        elif bytecode_info.bytecode_type == bytecode.BT_IF_TRUE_JUMP:
            val = parse(self.stack_top, self.frame)
            if self.tp_bool(val):
                self.jump(bytecode_info.value)
                return
            self.stack_push(val.tp_bytecode())
        elif bytecode_info.bytecode_type == bytecode.BT_IF_FALSE_JUMP:
            value = parse(self.stack_top, self.frame)
            if not self.tp_bool(value):
                self.jump(bytecode_info.value)
                return
            self.stack_push(value.tp_bytecode())
        elif bytecode_info.bytecode_type == bytecode.BT_CALL:
            self.call_function()
        elif bytecode_info.bytecode_type == bytecode.BT_RETURN:
            if self.frame.prev_frame is None:
                throw(UELRuntimeError, "'return' outside function")
            self.frame.prev_frame.gqueue.put_nowait(self.frame.stack.top)
            
        else:
            prettyd = bytecode_info.pretty_with_bytecode_type(bytecode_info.bytecode_type)[0]
            raise ValueError("Not support type:" +
                             f"{prettyd}"
                            )

    def call_function(self):
        def getFunctionArgumentLength(fn: Union[UEFunctionObject, UECallableObject, FunctionType]):
            if runtime_type_check(fn, FunctionType):
                return fn.__code__.co_argcount - 1
            elif issubclass(type(fn), UECallableObject):
                if runtime_type_check(fn, UEFunctionObject):
                    return len(fn.args)
                else:
                    throw(UELRuntimeError, f"{fn.tp_str()} is not callable")
        function: Union[UEFunctionObject, UECallableObject, FunctionType] = parse(self.stack_top, self.frame)
        arguments = []
        for _ in range(0, getFunctionArgumentLength(function)):
            arguments.insert(0, self.frame.gqueue.get_nowait())
        if runtime_type_check(function, UEFunctionObject):
            function.tp_call(args=arguments,
                             frame=self.frame)
            # print(self.frame)
        elif isinstance(function, FunctionType):
            result: UEObject = function(self.frame, *arguments)
            if result is not None:
                self.frame.gqueue.put_nowait(result)
        else:
            print(function)

    def jump(self, idx):
        self.frame.idx = idx - 2

    def tp_bool(self, val) -> bool:
        if hasattr(val, "val"):
            return bool(val.val)
        return True

    @staticmethod
    def binary_op(frame: Frame, bytecode_info: BytecodeInfo):
        right_value = parse(frame.stack.top, frame)
        left_value = parse(frame.stack.top, frame)
        
        fn_name: str
        
        if bytecode_info.bytecode_type == bytecode.BT_ADD:
            fn_name = "tp_add"
        elif bytecode_info.bytecode_type == bytecode.BT_MINUS:
            fn_name = "tp_minus"
        elif bytecode_info.bytecode_type == bytecode.BT_MUL:
            fn_name = "tp_mult"
        elif bytecode_info.bytecode_type == bytecode.BT_DIV:
            fn_name = "tp_div"
        else:
            raise ValueError
        if (
            (hasattr(left_value, fn_name) and hasattr(right_value, fn_name))
           ):
            result = getattr(left_value, fn_name)(right_value)
        else:
            throw(UELRuntimeError("[TypeError] Unable add"))
        frame.stack.push(result.tp_bytecode())

    def print(self, uelobject: UEObject) -> None:
        print(parse(uelobject, self.frame).tp_str(), end="")
