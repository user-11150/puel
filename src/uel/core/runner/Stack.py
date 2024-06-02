from queue import LifoQueue
from typing import Generic, TypeVar

T = TypeVar("T")


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
