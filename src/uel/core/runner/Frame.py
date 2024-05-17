import typing as t

from uel.core.runner.Stack import Stack
from queue import Queue

class Frame:
    def __init__(self, stack: Stack,
                 idx: int,
                 bytecodes: t.List[t.Any],
                 prev_frame: t.Optional["Frame"]=None,
                 filename: str=None,
                 variables: t.Optional[dict]=None,
                 gqueue: t.Optional[Queue]=None):
        self.stack: Stack = stack
        self.idx = idx
        self.bytecodes = bytecodes
        self.filename = filename
        self.prev_frame = prev_frame
        self.variables = variables
        if self.variables is None:
            self.variables = {}
        self.gqueue = Queue()
        
