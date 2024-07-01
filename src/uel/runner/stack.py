from queue import LifoQueue
from typing import Generic, TypeVar, Iterator

T = TypeVar("T")

__all__ = ["Stack"]


class Stack(Generic[T]):
    """
    First in last out
    """
    def __init__(self) -> None:
        self._queue: list[T] = []

    @property
    def top(self) -> T:
        return self._queue.pop()

    def push(self, value: T) -> None:
        self._queue.append(value)

    def is_empty(self):
        return not self._queue
