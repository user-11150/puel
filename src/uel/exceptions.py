from uel.objects import UELObject


class UELException(UELObject):
    tp_name = "Exception"


class UELError(UELException):
    tp_name = "Error"


class UELSyntaxError(UELError):
    tp_name = "UELSyntaxError"


def uel_set_error_string(exception: UELException):
    pass
