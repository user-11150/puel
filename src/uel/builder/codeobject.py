from dataclasses import dataclass
from uel.instruction import Instruction
from typing import Optional, Any


@dataclass
class UELCode:
    co_instructions: list[Instruction]
    co_consts: list[Any]
    co_stacksize: int
