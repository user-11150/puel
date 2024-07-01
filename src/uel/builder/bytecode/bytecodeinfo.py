import typing as t
from copy import deepcopy
from typing import TypeAlias

from uel.builder.position import Position
from uel.tools.func.share.runtime_type_check import runtime_type_check

# Bytecode types
BT: TypeAlias = int

BT_ADD: BT = 1
BT_MINUS: BT = 2
BT_MUL: BT = 3
BT_DIV: BT = 4
BT_STORE_NAME: BT = 5
BT_POP: BT = 6
BT_LOAD_CONST: BT = 7
BT_QPUT: BT = 8
BT_QTOP: BT = 9
BT_PUT: BT = 10
BT_JUMP: BT = 11
BT_IS: BT = 12
BT_CALL: BT = 13
BT_RETURN: BT = 14
BT_POP_JUMP_IF_FALSE = 15
BT_MAKE_SEQUENCE = 16
BT_SEQUENCE_APPEND = 17

__all__ = [
    *filter(lambda x: x.startswith("BT"),
            locals().keys()), "BytecodeInfo"
]


class BytecodeInfo:
    def __init__(
        self, bytecode_type: BT, value: t.Optional[t.Any], pos: int
    ):
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
            BT_POP_JUMP_IF_FALSE: "pop jump if false",
            BT_MAKE_SEQUENCE: "make sequence",
            BT_SEQUENCE_APPEND: "sequence append"
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
