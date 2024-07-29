import abc
from abc import abstractproperty


class UELObject(abc.ABC):
    @abstractproperty
    def tp_name(self) -> str:
        pass
