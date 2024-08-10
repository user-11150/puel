from uel.objects.object import UELObject
from uel.typing import Position, Optional, Never
from uel.tools import uel_exit
from uel.internal.uelcore_internal_exceptions import throw
import sys


class UELError(UELObject):
    tp_name = "Error"

    def __init__(self, message=None):
        self.message = message


class UELSyntaxError(UELError):
    tp_name = "UELSyntaxError"


class UELIOError(UELError):
    tp_name = "IOError"


def _getline(source, target_lineno):
    return source.splitlines()[target_lineno - 1]


def uel_set_error(
    exception: UELError,
    source: Optional[str] = None,
    start: Optional[Position] = None,
    end: Optional[Position] = None
) -> Never:
    """
    Using "uel_set_error"

      1. No positions
          uel_set_error(<exc>[, <source>])
      2. Only start
          uel_set_error(<exc>, <source>, <start>)
      3. Full
          uel_set_error(<exc>, <source>, <start>, <end>)
    """

    string = ""

    string += exception.tp_name
    if exception.message is not None:
        string += ":"
        string += exception.message

    try:
        if source is not None and start is not None:

            trace = _getline(source, start[0])

            if end is None and start is not None:
                end = start
            if start is None and end is not None:
                throw(uel_set_error.__doc__)
            if start is not None and end is not None:
                if start[0] == end[0] and end[1] > start[1]:
                    trace = f"{trace}\n{' '*(start[1]-1)}{'^'*len(trace[start[1]:end[1]+1])}"
                else:
                    trace = f"{trace}\n{' '*(start[1]-1)}^"
            if not trace.isspace():
                string = f"{trace}\n{string}"
    except:
        pass
    sys.stderr.write(string)
    sys.stderr.write("\n")
    sys.stderr.flush()
    uel_exit()


def uel_set_error_string(exception, message, *args, **kwargs) -> Never:
    uel_set_error(exception(message), *args, **kwargs)
