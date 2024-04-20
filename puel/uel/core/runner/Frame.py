import typing as t

from queue import Queue

class Frame:
    def __init__(self, stack: t.Any,
                 prev_frame: t.Optional["Frame"]=None,
                 variables: t.Optional[dict]=None,
                 gqueue: t.Optional[Queue]=None,):
        self.stack: t.Any = stack
        self.prev_frame = prev_frame
        self.variables = variables
        if self.variables is None:
            self.variables = {}
        self.gqueue = Queue()
        
