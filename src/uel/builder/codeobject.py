from dataclasses import dataclass
from typing import Optional, Any
from uel.builder.token import UELToken
from uel.builder.ast import AST


@dataclass
class UELCode:
    co_filename: Optional[str] = None
    co_source: Optional[str] = None
    co_tokens: Optional[list[UELToken]] = None
    co_ast: Optional[AST] = None
    co_bytecodes: Any = None
    co_names: Optional[list[str]] = None
    co_consts: Optional[list[Any]] = None
    co_stacksize: Optional[int] = None
