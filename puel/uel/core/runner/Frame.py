import typing as t

from uel.core.runner.Stack import Stack
from queue import Queue

class Frame:
    def __init__(self, stack: Stack,
                 prev_frame: t.Optional["Frame"]=None,
                 variables: t.Optional[dict]=None,
                 gqueue: t.Optional[Queue]=None):
        self.stack: Stack = stack
        self.prev_frame = prev_frame
        self.variables = variables
        if self.variables is None:
            self.variables = {}
        self.gqueue = Queue()
        
