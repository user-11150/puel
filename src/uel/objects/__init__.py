from uel.internal.uelcore_internal_exceptions import throw
from typing import Optional

import inspect as insp
import objprint

class UELTypeObject:
    def __init__(self,
        tp_name: str, tp_doc: str, tp_attrs: dict[str, "UELObject"],
        
        nb_add,
        nb_minus, nb_mult, nb_div,
        
        tp_call):
        if type(tp_name) is not str:
            throw("Invalid tp_name")
        
        self.tp_name = tp_name
        self.tp_doc = tp_doc
        self.tp_attrs = tp_attrs
        
        self.nb_add = nb_add
        self.nb_minus = nb_minus
        self.nb_mult = nb_mult
        self.nb_div = nb_div
        
        self.tp_call = tp_call

class UELObject:
    type: UELTypeObject
