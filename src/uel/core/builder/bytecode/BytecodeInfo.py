import typing as t
from copy import deepcopy
from typing import TypeAlias

from uel.core.builder.Position import Position
from uel.tools.func.share.runtime_type_check import runtime_type_check

# Bytecode types
BT: TypeAlias = int

BT_ADD: BT = 0b00000000_00000000_00000001
BT_MINUS: BT = 0b00000000_00000000_00000010
BT_MUL: BT = 0b00000000_00000000_00000011
BT_DIV: BT = 0b00000000_00000000_00000100
BT_STORE_NAME: BT = 0b00000000_00000000_00000101
BT_POP: BT = 0b00000000_00000000_00000110
BT_LOAD_CONST: BT = 0b00000000_00000000_00000111
BT_QPUT: BT = 0b00000000_00000000_00001000
BT_QTOP: BT = 0b00000000_00000000_00001001
BT_PUT: BT = 0b00000000_00000000_00001010
BT_JUMP: BT = 0b00000000_00000000_00001011
BT_IS: BT = 0b00000000_00000000_00001100
BT_CALL: BT = 0b00000000_00000000_00001101
BT_RETURN: BT = 0b00000000_00000000_00001110
BT_POP_JUMP_IF_FALSE = 0b00000000_00000000_00001111


class BytecodeInfo:

    def __init__(self, bytecode_type: BT, value: t.Optional[t.Any], pos: int):
        # 只有bytecode运行到哪的位置，token的位置被我搞丢了
        assert pos > 0, "the arg 1 must be great 0"

        self.bytecode_type = bytecode_type
        self.value = value
        self.pos = pos

    def copy(self) -> "BytecodeInfo":
        return deepcopy(self)

    def where(self, start: int, end: int) -> bool | None:
        if (abs(start) == start and abs(end) == end):
            return self.pos >= start and self.pos <= end
        raise ValueError("The arg 1 and arg 2 must be great 0")

    @staticmethod
    def pretty_with_bytecode_type(bt: BT) -> t.Tuple[str, int]:
        mapping = {
            BT_ADD: "add",
            BT_MINUS: "minus",
            BT_MUL: "multiply",
            BT_DIV: "division",
            BT_STORE_NAME: "store name",
            BT_POP: "pop",
            BT_LOAD_CONST: "load const",
            BT_QPUT: "queue put",
            BT_QTOP: "queue top",
            BT_PUT: "put",
            BT_JUMP: "jump to",
            BT_IS: "is",
            BT_CALL: "call",
            BT_RETURN: "return",
            BT_POP_JUMP_IF_FALSE: "pop jump if false"
        }
        mapping.setdefault("unknown")  # type: ignore
        return mapping[bt].upper().replace(" ", "_"), bt

    def __repr__(self) -> str:
        bt = self.pretty_with_bytecode_type(self.bytecode_type)[0]
        if self.value is not None:
            return f"Info({bt}, {self.value}, index={self.pos})"
        else:
            return f"Info({bt}, index={self.pos})"


# if __name__ == "__main__":
#    code = BytecodeInfo(BT_ADD, (2, 3), 1, Position(1,1,1,1,1))
#    print(code)
#    is_where_range = code.where(0,1)
#    print(is_where_range)
