class TokenNode:
    def __init__(self,token_type: str,token_val: str = None,pos=None):
        self.token_type: str = token_type
        self.pos = pos
        if self.pos is None:
            raise Exception('Cannot get token position')
        self.token_val: str = token_val
    def __repr__(self):
        if self.token_val is not None:
            return f"TokenNode(token_type={repr(self.token_type)}, token_val={repr(self.token_val)})"
        return f"TokenNode(token_type={self.token_type})"
