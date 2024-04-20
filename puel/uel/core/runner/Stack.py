from collections import deque
from typing import TypeVar
from typing import Generic

T = TypeVar("T")

class Stack(Generic[T]):
    """
    First in last out
    """
    def __init__(self):
        self.__deque = deque[T]()

    @property
    def top(self) -> T:
        return self.__deque.pop()

    def push(self, value: T) -> None:
        self.__deque.append(value)

if __name__ == "__main__":
    stack = Stack[bool]()
    stack.push(True)
    stack.push(False)
    print(stack.top)
    print(stack.top)
