from uel.core.runner.Frame import Frame
from uel.core.runner.Stack import Stack
from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode import BytecodeInfo as bytecode

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
        if bytecode_info.bytecode_type is bytecode.BT_LOAD_CONST:
            self.stack_push(bytecode_info.value)
        elif bytecode_info.bytecode_type is bytecode.BT_ADD:
            x = self.stack_top
            y = self.stack_top
            self.stack_push(1)
        elif bytecode_info.bytecode_type is bytecode.BT_MINUS:
            x = self.stack_top
            y = self.stack_top
            print(x,y)
        elif bytecode_info.bytecode_type is bytecode.BT_STORE_NAME:
            value = bytecode_info.value
            print("store ",value)
        else:
            raise ValueError(f"Not support type: {bytecode_info.bytecode_type}")
