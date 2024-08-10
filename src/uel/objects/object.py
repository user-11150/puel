from abc import abstractproperty, ABC


class UELObject(ABC):
    tp_name = "Object"

    def __repr__(self):
        if hasattr(self, "value"):
            return f"{self.tp_name}({self.value})"
        raise NotImplementedError
