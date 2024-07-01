from functools import wraps
from typing import Any, Callable, Generic, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar('R')
E = TypeVar("E")

__all__ = ["Withable", "with_out"]


class Withable(Generic[E]):
    def __init__(self, value: E):
        self.value = value

    def __repr__(self) -> str:
        return f"Withable<{self.value.__class__.__name__}>({self.value})"

    def __enter__(self) -> E:
        return self.value

    def __exit__(self, a: None, b: None, c: None) -> None:
        pass


def with_out(func: Callable[P, R]) -> Callable[P, Withable[R]]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Withable[R]:
        return Withable(func(*args, **kwargs))

    return inner


if __name__ == "__main__":

    @with_out
    def fn(m: int) -> int:
        return m + 3

    with fn(3) as f:
        print(f)
