from dataclasses import dataclass


@dataclass
class UELCode:
    co_filename = None
    co_source = None
    co_tokens = None
    co_ast = None
    co_bytecodes = None
    co_names = None
    co_consts = None
    co_stacksize = None
