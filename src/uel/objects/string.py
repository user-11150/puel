from uel.objects.object import UELObject


class UELString(UELObject):
    tp_name = "String"

    def __init__(self, value):
        self.value = value


def uel_string_as_python_str(string):
    return string.value


def uel_string_from_python_str(string):
    return UELString(string)
