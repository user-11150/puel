__all__ = ["UELBaseException"]


class UELBaseException:
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:{self.error_message}"
