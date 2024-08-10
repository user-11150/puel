from uel.opcodes import opcode_to_opname


class Instruction:
    def __init__(self, opcode, value):
        self.opcode = opcode
        self.value = value

    def __repr__(self):
        return f"Instruction({self.opcode}({opcode_to_opname(self.opcode)}) {repr(self.value)})"
