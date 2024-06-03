def get_stack_top(frame):
    current_frame = frame
    while True:
        if current_frame.stack._queue != []:
            return current_frame.stack.top
        current_frame = current_frame.prev_frame
        if current_frame is None:
            raise
            throw(UELRuntimeError, "Stack is empty")
            return
