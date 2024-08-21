from uel.settings import PACKAGE_DIRMAME, LIBARY_SEARCH_DIRECTORIES
from uel.virtual_machine.frames import Frame
from uel.opcodes import *
from uel.exceptions import uel_set_error_string, UELNameError
from uel.internal.uelcore_internal_exceptions import throw
from uel.tools import uel_exit
from uel.objects.object import UELObject
from uel.objects.fucntion import UELFunction
from uel.libary.manager import getmodules


class UELEval:
    frame: Frame

    def __init__(self, code):
        self.code = code

    def push_stack(self, value):
        self.frame.f_stack.push(value)

    def next(self):
        self.frame.f_lasti += 1

    def pop_stack(self) -> UELObject:
        return self.frame.f_stack.pop()

    def top_stack(self):
        return self.frame.f_stack.top()

    def const(self, index):
        return self.frame.f_code.co_consts[index]

    def variable(self, name):
        current_frame = self.frame
        while True:
            try:
                return current_frame.f_vars[name]
            except:
                if current_frame.f_back is not None:
                    current_frame = current_frame.f_back
                else:
                    break
        uel_set_error_string(
            UELNameError, f"Name '{name}' is not defined"
        )

    def run_until_complete(self):

        self.frame = Frame(None, self.code, 0, {})

        while True:
            if self.frame.f_lasti >= len(
                self.frame.f_code.co_instructions
            ):
                if self.frame.f_back is not None:
                    self.frame = self.frame.f_back
                else:
                    uel_exit()
            self.eval(
                self.frame.f_code.co_instructions[self.frame.f_lasti]
            )

    def eval(self, instruction):
        instr = instruction  # alias

        def target(*opcodes):
            return any(case == instruction.opcode for case in opcodes)

        if target(ADD, MINUS, MULT, DIV):
            self.next()
            name = f'tp_{opcode_to_opname(instruction.opcode).lower()}'
            right = self.pop_stack()
            left = self.pop_stack()
            self.push_stack(getattr(left, name)(right))
        elif target(LOAD_ATTR):
            self.next()
            self.push_stack(
                self.pop_stack().tp_getattr(
                    self.const(instruction.value)
                )
            )
        elif target(UNARY_NEGATIVE):
            self.next()
            self.push_stack(self.pop_stack().tp_negative())
        elif target(POP_TOP):
            self.pop_stack()
            self.next()
        elif target(LOAD_CONST):
            self.push_stack(self.const(instruction.value))
            self.next()
        elif target(LOAD_NAME):
            self.push_stack(self.variable(self.const(instruction.value)))
            self.next()
        elif target(STORE_NAME):
            self.frame.f_vars[self.const(instruction.value)
                             ] = self.pop_stack()
            self.next()
        elif target(EXEC_CODE):
            self.next()
            self.frame = Frame(self.frame, self.pop_stack(), 0, {})
        elif target(IMPORT_NAME):
            self.next()
            name = self.const(instr.value)
            self.push_stack(getmodules().get(name))
        elif target(RETURN_VALUE):
            retval = self.pop_stack()
            if self.frame.f_back is not None:
                self.frame = self.frame.f_back
                self.push_stack(retval)
            else:
                uel_exit()
        elif target(CALL):
            self.next()
            func = self.pop_stack()
            argcount = self.pop_stack()
            args = []
            for _ in range(argcount):
                args.insert(0, self.pop_stack())
            func.tp_call(self, args)
        elif target(MAKE_FUNCTION):
            body = self.pop_stack()
            args = self.pop_stack()
            self.push_stack(UELFunction(args, body))
            self.next()
        else:
            throw(
                f"{opcode_to_opname(instruction.opcode)}({instruction.opcode}) is not implemented"
            )
