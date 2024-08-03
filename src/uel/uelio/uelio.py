from uel.exceptions import uel_set_error_string, UELIOError

import builtins


def file_open(file, mode, **kwrargs):
    try:
        fp = builtins.open(file, mode, **kwrargs)
    except Exception as e:
        uel_set_error_string(UELIOError, f"{type(e)} {e}")
    return fp
