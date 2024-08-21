class UELObject:
    tp_name = "Object"

    def tp_call(self, _, args):
        from uel.exceptions import uel_set_error_string, UELNotImplementedError
        uel_set_error_string(
            UELNotImplementedError,
            f'{self.tp_name} object is not a callable'
        )

    def tp_negative(self):
        from uel.exceptions import uel_set_error_string, UELNotImplementedError
        uel_set_error_string(UELNotImplementedError, '')

    def tp_add(self, _):
        from uel.exceptions import uel_set_error_string, UELNotImplementedError
        uel_set_error_string(UELNotImplementedError, '')

    def tp_minus(self, _):
        from uel.exceptions import uel_set_error_string, UELNotImplementedError
        uel_set_error_string(UELNotImplementedError, '')

    def tp_mult(self, _):
        from uel.exceptions import uel_set_error_string, UELNotImplementedError
        uel_set_error_string(UELNotImplementedError, '')

    def tp_div(self, _):
        from uel.exceptions import uel_set_error_string, UELNotImplementedError
        uel_set_error_string(UELNotImplementedError, '')

    def tp_getattr(self, attr):
        from uel.exceptions import uel_set_error_string, UELAttributeError
        uel_set_error_string(
            UELAttributeError,
            f'{repr(self.tp_name)} object has no {repr(attr)} member'
        )

    def tp_str(self):
        from uel.objects.string import uel_string_from_python_str
        return uel_string_from_python_str(self.tp_name)
