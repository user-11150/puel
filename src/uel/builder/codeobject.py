from dataclasses import dataclass
from uel.instruction import Instruction
from typing import Optional, Any


@dataclass
class UELCode:
    co_filename: str
    co_source: str
    co_instructions: list[Instruction]
    co_names: list[str]
    co_consts: list[Any]
    co_stacksize: int
