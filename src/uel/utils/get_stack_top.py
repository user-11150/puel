__all__ = ["get_stack_top"]


def get_stack_top(frame):
    current_frame = frame
    while True:
        if not current_frame.stack.is_empty():
            return current_frame.stack.top
        current_frame = current_frame.prev_frame
        if current_frame is None:
            raise
            throw(UELRuntimeError, "Stack is empty")
            return
