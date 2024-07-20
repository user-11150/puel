from uel.objects import UELTypeObject, UELObject, uel_internal_class_definition_head, UELObject_New
from uel.internal.uelcore_internal_exceptions import throw

UELException = UELTypeObject(
    tp_name="Exception",
    tp_doc="Exception",
    tp_attrs={},
    nb_add=None,
    nb_minus=None,
    nb_mult=None,
    nb_div=None,
    tp_call=None,
    tp_new=UELObject_New
)

if not UELType_Ready(UELException):
    throw("A error in initial")


def uel_set_error_string(exception: UELBaseException):
    pass
