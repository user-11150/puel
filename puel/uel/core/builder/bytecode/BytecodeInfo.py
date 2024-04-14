from copy import deepcopy
from typing import TypeAlias
from uel.core.builder.Position import Position
from uel.tools.func.share.runtime_type_check import runtime_type_check

# Bytecode types
BT: TypeAlias = int

# BT filter
BTF = TypeAlias = int

BT_ADD:   BT = 0b00000001
BT_MINUS: BT = 0b00000010
BT_MUL:   BT = 0b00000011
BT_DIV:   BT = 0b00000100
BT_VAR:   BT = 0b00000101

BT_OP: BTF =   0b00000111

class BytecodeInfo:
    def __init__(self, bytecode_type: BT,
                 value: str,
                 pos: int):
        # 只有bytecode运行到哪的位置，token的位置被我搞丢了
        assert pos > 0, "the arg 1 must be great 0"
        
        self.bytecode_type = bytecode_type
        self.value = value
        self.pos = pos

    def copy(self):
        return deepcopy(self)

    def where(self, start, end):
        if(abs(start) == start
          and abs(end) == end):
            return self.pos >= start and self.pos <= end
        raise ValueError("The arg 1 and arg 2 must be great 0")

    @staticmethod
    def pretty_with_bytecode_type(bt: BT):
        mapping = {
            BT_ADD: "add",
            BT_MINUS: "minus",
            BT_MUL: "multiply",
            BT_DIV: "division",
            BT_VAR: "variable"
        }
        mapping.setdefault("unknown")
        return mapping[bt], bt

    def __repr__(self) -> str:
        bt = self.pretty_with_bytecode_type(self.bytecode_type)[0]
        return f"Info({bt} => {self.value}, index={self.pos})"

#if __name__ == "__main__":
#    code = BytecodeInfo(BT_ADD, (2, 3), 1, Position(1,1,1,1,1))
#    print(code)
#    is_where_range = code.where(0,1)
#    print(is_where_range)
