import typing as t


class AbstractTask:

    def run(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        raise NotImplementedError
