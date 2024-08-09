from uel.opcodes import opcode_to_opname


class Instruction:
    def __init__(self, opcode, value, lineno):
        self.opcode = opcode
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return f"{self.lineno} {opcode_to_opname(self.opcode)} {repr(self.value)}"
