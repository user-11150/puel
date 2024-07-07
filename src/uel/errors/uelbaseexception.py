__all__ = ["UELBaseException"]


class UELBaseException(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self) -> str:
        msg = self.error_message
        return f"{self.__class__.__module__}.{self.__class__.__name__}: {msg}"
