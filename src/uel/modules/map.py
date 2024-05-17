from uel.modules import fib
from objprint import op
from uel.libary.helpers import make_exports
from uel.core.object.object_parse import parse
from uel.core.object.UENumberObject import UENumberObject

def fib_wrapper(module):
    f_fib = module.fib
    def _f_fib(f, n):
        inputval = int(parse(n, f).val)
        print(inputval, type(inputval))
        res = f_fib(inputval)
        
        return UENumberObject(res)
    module.bytecodes = make_exports({
        "fib": _f_fib
    })
    return module

MAP = {
    "fib": fib_wrapper(fib)
}
