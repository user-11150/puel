from typing import (# A
                    Any,
                    # G
                    Generic,
                    # T
                    TypeVar,
                    TypeAlias,
                    )

ByteCodeType: TypeAlias = str

BYTECODE_TYPE_LOAD_CONST: ByteCodeType = "BYTECODE_TYPE_LOAD_CONST"

BYTECODE_TYPE_ADD:   ByteCodeType = "BYTECODE_TYPE_ADD"
BYTECODE_TYPE_MINUS: ByteCodeType = "BYTECODE_TYPE_MINUS"
BYTECODE_TYPE_MUL:   ByteCodeType = "BYTECODE_TYPE_MUL"
BYTECODE_TYPE_DIV:   ByteCodeType = "BYTECODE_TYPE_DIV"

BYTECODE_TYPE_POP: ByteCodeType = "BYTECODE_TYPE_POP"
BYTECODE_TYPE_TOP: ByteCodeType = "BYTECODE_TYPE_TOP"

# About the ByteCodeNodeInfo
T = TypeVar("T")

class ByteCodeNodeInfo(Generic[T]):
    bytecode_type: ByteCodeType
    value: Any
    
    def __init__(self, bytecode_type: ByteCodeType, value: Any):
        self.__bytecode_type: ByteCodeType = bytecode_type
        self.__value: Any = value


    def __repr__(self):
        bytecode_type = self.bytecode_type
        value = self.value
        return f"ByteCodeNodeInfo({bytecode_type=}, {value=})"

    @property
    def bytecode_type(self) -> ByteCodeType:
        return self.__bytecode_type

    @bytecode_type.setter
    def bytecode_type(self, nv: Any) -> None:
        raise TypeError("Readonly object is cannot change")

    @property
    def value(self) -> Any:
        return self.__value

    @value.setter
    def value(self, nv: Any) -> None:
        raise TypeError("Readonly object is cannot change")

from queue import Queue
