from uel.exceptions import uel_set_error_string, UELIOError
from typing import Any

import builtins


def file_open(file: str, mode: str, **kwrargs: Any) -> Any:
    try:
        fp = builtins.open(file, mode, **kwrargs)
    except Exception as e:
        uel_set_error_string(UELIOError, f"{type(e)} {e}")
    return fp
