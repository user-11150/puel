"""
The AST node's base
"""

from typing import Any, TypeVar

T = TypeVar("T")

__all__ = ["AbstractNode"]


class AbstractNode:
    """
    The AbstractNode(AN) is a abstract classs.

    AN is the all AST(abstract syntax tree) important baseclass
    """
    def __init__(self) -> None:
        raise NotImplementedError  # pragma: no cover

    def tp(self, typ: type[T]) -> T:
        return self  # type: ignore
