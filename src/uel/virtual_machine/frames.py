from uel.virtual_machine.stack import Stack
from uel.builder.codeobject import UELCode
from uel.typing import Union


class Frame:
    def __init__(
        self, f_back: Union[None, "Frame"], f_code: UELCode,
        f_lasti: int, f_vars
    ):
        self.f_back = f_back
        self.f_code = f_code
        self.f_lasti = f_lasti
        self.f_vars = f_vars
        self.f_stack = Stack()
