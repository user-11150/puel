import typing as t
import warnings
from uel.tools import uel_exit
from pprint import pprint
from string import ascii_letters
from uel.exceptions import uel_set_error_string
from uel.exceptions import UELSyntaxError

numbers = "".join(map(str, range(10)))

# Flags
UEL_TOKENIZE = 0
UEL_AST = 1
UEL_OPTIMIZED_AST = 2
UEL_BYTECODE = 3
UEL_RUNUE = 6

# Combination flags
UEL_SIMPLE_RUN_FLAGS = [
    UEL_TOKENIZE, UEL_AST, UEL_OPTIMIZED_AST, UEL_BYTECODE, UEL_RUNUE
]

# Token types
TT_NEWLINE = "NEWLINE"
TT_EOF = "EOF"

TT_KEYWORD = "KEYWORD"
TT_IDENTIFIER = "IDENTIFIER"

KEYWORDS = [
    "put"
]

class UELCode:
    def __init__(
            self,
            co_source: t.Any=None,
            co_filename: t.Optional[str]=None,
            co_consts: t.Optional[list[str]]=None,
            co_names: t.Optional[list[str]]=None):
        self.co_source = co_source
        self.co_filename = co_filename
        self.co_consts = co_consts
        self.co_names = co_names


class UELToken:
    def __init__(
        self,
        token_type: str,  # Token's Type
        token_value: t.Any,  # Token's value
        start_line: int,  # Token's start line
        start_col: int,  # Token's start col
        end_line: int,  # Token's end line
        end_col: int  # Token's end col
    ):
        self.token_type = token_type
        self.token_value = token_value
        self.start_line = start_line
        self.start_col = start_col
        self.end_line = end_line
        self.end_col = end_col

    def __repr__(self) -> str:
        return f"UELToken(token_type={self.token_type}, token_value={repr(self.token_value)}, start_line={self.start_line}, start_col={self.start_col}, end_line={self.end_line}, end_col={self.end_col})"

    def __str__(self) -> str:
        return f"{self.token_type} {repr(self.token_value)} {(self.start_line, self.start_col)} -> {(self.end_line, self.end_col)}"

    @staticmethod
    def _slice(source, idx):
        if len(source) <= idx:
            uel_set_error_string()

    @staticmethod
    def idx_as_line_and_col(source: str, idx: int) -> tuple[int, int]:
        line = 1
        col = 1
        
        for current in UELToken._slice(source, idx):
            col += 1
            if current == "\n":
                col = 1
                line += 1
        return line, col

class UELTokenize:
    def __init__(self, source: t.Any) -> None:
        self.source = source
        self.current_idx = 0
    
    @property
    def current_char(self) -> str:
        try:
            return self.source[self.current_idx]
        except IndexError:
            return None
    
    def advance(self) -> str:
        self.current_idx += 1
        return self.current_char
    
    def make_tokens(self) -> list[UELToken]:
        tokens = []
        while True:
            start_position = self.current_idx
            if start_position <= len(self.source):
                start_line, start_col = UELToken.idx_as_line_and_col(self.source, start_position)
            if self.current_char is None:
                start_line = None
                start_col = None
                
                tokens.append(
                    UELToken(
                        TT_EOF,
                        None,
                        start_line,
                        start_col,
                        None,
                        None
                    )
                )
                break
            if self.current_char == " ":
                self.advance() # Skipped
            elif self.current_char == "\n":
                self.advance()
                tokens.append(
                    UELToken(
                        TT_NEWLINE,
                        "\n",
                         start_line,
                         start_col,
                         *UELToken.idx_as_line_and_col(self.source, self.current_idx)
                    )
                )
            elif self.is_identifier_start(self.current_char):
                identifier = self.make_identifier()
                token_type = TT_KEYWORD if identifier in KEYWORDS else TT_IDENTIFIER
                end_line, end_col = UELToken.idx_as_line_and_col(self.source, self.current_idx)
                tokens.append(
                    UELToken(
                        token_type,
                        identifier,
                        start_line,
                        start_col,
                        end_line,
                        end_col
                    )
                )
            
        return tokens

    @staticmethod
    def is_identifier_start(char):
        if char in ascii_letters:
            return True
        if '\u4e00' <= char <= '\u9fff':
            return True
        if char in ["_", "$"]:
            return True

        return False

    @classmethod
    def is_identifier(cls, char):
        return cls.is_identifier_start(char) or char in numbers

    def make_identifier(self):
        result = ""
        
        while self.is_identifier(self.current_char):
            result += self.current_char
            self.advance()
        
        return result

class UELAST:
    pass


class UELBytecode:
    pass


CompileResult = t.Union[list[UELToken], UELAST, list[UELBytecode]]

Source = t.Union[str, CompileResult]


def uel_tokenize(source: str) -> list[UELToken]:
    return UELTokenize(source).make_tokens()

def _uel_compile(source, code, flag) -> Source:
    if flag == UEL_TOKENIZE:
        code.co_source = source
        return uel_tokenize(source)
    else:
        warnings.warn("Accept a error flag, exit")
        uel_exit()
def print_compiled(compiled):
     if type(compiled) is list:
         if len(compiled):
             if type(compiled[0]) is UELToken:
                 print("\n".join(map(str, compiled)))

def uel_compile(source: Source, code: UELCode, verbose: bool,flags: t.Optional[list[int]] = None) -> t.Any:
    if flags is None:
        flags = UEL_SIMPLE_RUN_FLAGS

    for flag in flags:
        source = _uel_compile(source, code, flag)
        if verbose:
            print_compiled(source)
