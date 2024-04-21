from uel.core.runner.Frame import Frame
from uel.core.runner.Stack import Stack
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode import BytecodeInfo as bytecode
from uel.core.object.object_parse import parse
from uel.core.errors.runtime.throw import throw
from uel.core.errors.runtime.UELRuntimeError import UELRuntimeError

from uel.core.object.UEObject import UEObject
from queue import Queue

from typing import Any
from typing import List

class Ueval:
    def __init__(self, bytecodes: List[BytecodeInfo]):
        self.bytecodes = bytecodes
        self.frame = Frame(
            # Stack
            Stack[Any](),
            # Prev_frame
            None,
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
        for _bytecode in self.bytecodes:
            self.eval(_bytecode)

    def eval(self, bytecode_info: BytecodeInfo) -> None:
        if bytecode_info.bytecode_type == bytecode.BT_LOAD_CONST:
            self.stack_push(bytecode_info.value)

        elif bytecode_info.bytecode_type == bytecode.BT_ADD:
            self.binary_op(self.frame, bytecode_info)

        elif bytecode_info.bytecode_type == bytecode.BT_MINUS:
            self.binary_op(self.frame, bytecode_info)

        elif bytecode_info.bytecode_type == bytecode.BT_STORE_NAME:
            name = bytecode_info.value
            val = parse(self.stack_top, self.frame)
            self.frame.variables[name] = val

        elif bytecode_info.bytecode_type == bytecode.BT_QPUT:
            self.frame.gqueue.put(self.stack_top)

        elif bytecode_info.bytecode_type == bytecode.BT_POP:
            self.stack_top # pylint: disable=W

        elif bytecode_info.bytecode_type == bytecode.BT_PUT:
            self.print(self.stack_top)

        else:
            raise ValueError(f"Not support type: {bytecode_info.pretty_with_bytecode_type(bytecode_info.bytecode_type)[0]}")

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
