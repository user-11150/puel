from uel.objects.object import UELObject


class UELNumber(UELObject):
    tp_name = "Number"

    def __init__(self, value):
        self.value = value


def uel_number_as_python_number(number):
    return number.value


def uel_number_from_python_number(number):
    return UELNumber(number)
