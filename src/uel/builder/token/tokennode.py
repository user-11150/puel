from typing import *

from uel.builder.position import Position

__all__ = ["TokenNode"]


class TokenNode:
    def __init__(
        self,
        token_type: str,
        token_val: Optional[str] = None,
        pos: Position = Position()
    ) -> None:
        assert pos

        self.token_type: str = token_type
        self.pos = pos
        self.token_val: Optional[str] = token_val

    def __repr__(self) -> str:
        if self.token_val is not None:
            return f"TokenNode(token_type={repr(self.token_type)}, token_val={repr(self.token_val)})"
        return f"TokenNode(token_type={self.token_type})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenNode):
            # raise TypeError(f'Try to compare Token with {type(other)} for equality') from None
            raise NotImplementedError
        return self.token_type == other.token_type and self.token_val == other.token_val
