from uel.objects.object import UELObject
from uel.exceptions import uel_set_error_string, UELTypeError


class UELNumber(UELObject):
    tp_name = "Number"

    def __init__(self, value):
        self.value = value

    def tp_str(self):
        from uel.objects.string import uel_string_from_python_str
        try:
            strval = str(self.value)
        except:
            return 'Infinity or -Infinity'
        return uel_string_from_python_str(strval)

    def tp_negative(self):
        return uel_number_from_python_number(
            -uel_number_as_python_number(self)
        )

    def tp_add(self, other):
        if not isinstance(other, UELNumber):
            uel_set_error_string(
                UELTypeError, f"{other} is not a number"
            )
        return uel_number_from_python_number(
            uel_number_as_python_number(self) +
            uel_number_as_python_number(other)
        )

    def tp_minus(self, other):
        if not isinstance(other, UELNumber):
            uel_set_error_string(
                UELTypeError, f"{other} is not a number"
            )
        return uel_number_from_python_number(
            uel_number_as_python_number(self) -
            uel_number_as_python_number(other)
        )

    def tp_mult(self, other):
        if not isinstance(other, UELNumber):
            uel_set_error_string(
                UELTypeError, f"{other} is not a number"
            )
        return uel_number_from_python_number(
            uel_number_as_python_number(self) *
            uel_number_as_python_number(other)
        )

    def tp_div(self, other):
        if not isinstance(other, UELNumber):
            uel_set_error_string(
                UELTypeError, f"{other} is not a number"
            )
        return uel_number_from_python_number(
            uel_number_as_python_number(self) /
            uel_number_as_python_number(other)
        )


def uel_number_as_python_number(number):
    return number.value


def uel_number_from_python_number(number):
    return UELNumber(number)
