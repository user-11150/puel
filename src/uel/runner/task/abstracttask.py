import typing as t

__all__ = ["AbstractTask"]


class AbstractTask:
    def run(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        raise NotImplementedError
