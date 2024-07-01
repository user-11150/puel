import typing as t
from queue import Queue

from uel.runner.stack import Stack

__all__ = ["Frame"]


class Frame:
    def __init__(
        self,
        stack: Stack[t.Any],
        idx: int,
        bytecodes: t.List[t.Any],
        prev_frame: t.Optional["Frame"] = None,
        filename: str = "<unknown>",
        variables: t.Optional[dict[str, t.Any]] = None,
        gqueue: t.Optional[Queue] = None
    ):
        self.stack: Stack = stack
        self.idx = idx
        self.bytecodes = bytecodes
        self.filename = filename
        self.prev_frame = prev_frame
        self.variables = variables
        if self.variables is None:
            self.variables = {}
        self.gqueue = Queue[t.Any]()
