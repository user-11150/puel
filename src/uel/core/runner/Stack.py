from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """
    First in last out
    """

    def __init__(self) -> None:
        self.__deque = deque[T]()

    @property
    def top(self) -> T:
        return self.__deque.pop()

    def push(self, value: T) -> None:
        self.__deque.append(value)
