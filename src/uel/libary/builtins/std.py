from uel.objects.module import UELModule
from uel.objects.number import uel_number_from_python_number
from uel.objects.fucntion import uel_func_from_pyfunc
from uel.objects.object import UELObject
from uel.objects.string import uel_string_as_python_str, uel_string_from_python_str
from sys import stdout

mod = UELModule()

PI = 3.141592


@mod.method('print')
@uel_func_from_pyfunc
def std_print(executor, *targets):
    sep = ""
    for target in targets:
        stdout.write(uel_string_as_python_str(target.tp_str()))


@mod.method('typeof')
@uel_func_from_pyfunc
def typeof(executor, *targets):
    return uel_string_from_python_str(
        ",".join(map(lambda x: x.tp_name, targets))
    )


class UELReference(UELObject):
    tp_name = "Reference"

    def __init__(self, value):
        self.value = value

    def tp_getattr(self, name):
        if name == "value":
            return self.value
        super().tp_getattr(name)

    def tp_str(self):
        return uel_string_from_python_str(f'__tmp_ref_{id(self.value)}')


@mod.method('ref')
@uel_func_from_pyfunc
def ref(executor, x, y=None):
    if y is None:
        return UELReference(x)
    x.value = y
    return x


mod.add_attribute('PI', uel_number_from_python_number(PI))
