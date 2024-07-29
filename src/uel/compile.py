import typing as t
from string import ascii_letters
# from uel.exceptions import uel_set_error_string
# from uel.exceptions import UELSyntaxError
from uel.constants import (
    TT_EOF, TT_IDENTIFIER, TT_KEYWORD, TT_KEYWORDS, TT_NEWLINE,
)
from dataclasses import dataclass
from uel.internal.uelcore_internal_exceptions import throw

numbers = "".join(map(str, range(10)))


@dataclass
class UELCode:
    co_name = None
    co_source = None
    co_tokens = None
    co_ast = None
    co_bytecodes = None
    co_names = None
    co_consts = None
    co_stacksize = None


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
        pos = f"start_col={self.start_col}, end_line={self.end_line}, end_col={self.end_col}"
        return f"UELToken(token_type={self.token_type}, token_value={repr(self.token_value)}, start_line={self.start_line}, {pos})"

    def __str__(self) -> str:
        return f"{self.token_type} {repr(self.token_value)} {(self.start_line, self.start_col)} -> {(self.end_line, self.end_col)}"

    @staticmethod
    def _slice(source, idx):

        result = ""

        for current_index, current_char in enumerate(source):
            result += current_char
            if current_index == idx:
                break

        print(repr(result))
        return result

    @staticmethod
    def idx_as_line_and_col(
        source: str, idx: int
    ) -> tuple[t.Union[int, None], t.Union[int, None]]:
        line = 1
        col = 0

        if len(source) <= idx:
            return None, None

        for current in UELToken._slice(source, idx):
            col += 1
            if current == "\n":
                col = 0
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

    def rollback(self) -> str:
        self.current_idx -= 1
        return self.current_char

    def make_tokens(self) -> list[UELToken]:
        tokens = []
        while self.current_char is not None:

            start_position = self.current_idx
            if start_position <= len(self.source):
                start_line, start_col = UELToken.idx_as_line_and_col(
                    self.source, start_position
                )
            if self.current_char == " ":
                self.advance()  # Skipped
            elif self.current_char == "\n":
                self.advance()

                tokens.append(
                    UELToken(
                        TT_NEWLINE, "\n", start_line, start_col,
                        *UELToken.idx_as_line_and_col(
                            self.source, self.current_idx
                        )
                    )
                )
            elif self.is_identifier_start(self.current_char):
                identifier = self.make_identifier()
                token_type = TT_KEYWORD if identifier in TT_KEYWORDS else TT_IDENTIFIER
                end_line, end_col = UELToken.idx_as_line_and_col(
                    self.source, self.current_idx
                )
                tokens.append(
                    UELToken(
                        token_type, identifier, start_line, start_col,
                        end_line, end_col
                    )
                )
                self.advance()

        tokens.append(UELToken(TT_EOF, None, None, None, None, None))

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

        while True:
            if self.is_identifier(self.current_char):
                result += self.current_char
                self.advance()
            else:
                break

        self.rollback()
        return result


class UELAST:
    pass


class UELBytecode:
    pass


CompileResult = t.Union[list[UELToken], UELAST, list[UELBytecode]]

Source = t.Union[str, CompileResult]


def uel_generate_tokens(source: str) -> list[UELToken]:
    return UELTokenize(source).make_tokens()

def uel_tokenize(code: UELCode):
    code.co_tokens = uel_generate_tokens(code.co_source)
