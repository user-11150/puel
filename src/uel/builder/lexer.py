from string import digits as DIGITS
from typing import List, Optional

from uel.builder.position import Position
from uel.builder.token.tokenconstants import (
    TT_ADD, TT_COMMA, TT_DIV, TT_EOF, TT_EQUAL, TT_FLOAT, TT_IDENTIFER,
    TT_INT, TT_KEYWORD, TT_KEYWORDS, TT_MINUS, TT_MUL, TT_SEMI, TT_STRING,
    TT_RPAR, TT_LPAR
)
from uel.builder.token.tools.identifier import (
    is_identifier_center_char_or_end_char, is_start
)
from uel.errors.raiseerror import RaiseError
from uel.errors.throwexception import ThrowException
from uel.errors.toodotserror import TooDotsError
from uel.errors.unknownsyntaxerror import UnknownSyntaxError
from uel.pyexceptions.nerver import Nerver

from .token.tokennode import TokenNode as Token

__all__ = ["Lexer"]


class Lexer:
    """
    源代码 => Tokens
    """
    def __init__(self, fn: str, content: str):
        self.fn: str = fn
        self.content: str = content
        #                   I,  L  C   F   C
        self.pos = Position(0, 1, 1, fn, content)
        self.current_char: Optional[str] = None
        self.advance()

    def advance(self) -> bool:
        """
        预读
        """

        self.pos.advance(self.current_char)

        if self.pos.idx < len(self.content):
            self.current_char = self.content[self.pos.idx]
            return True
        else:
            self.current_char = None
            return False

    def make_tokens(self) -> List[Token]:
        """
        产生Token
        """
        tokens: List[Token] = []

        while self.current_char is not None:
            if self.current_char is None:
                raise RuntimeError
            # 匹配注释
            elif self.current_char == "#":
                self.skip_annotation()
                continue

            # 空白
            elif (
                self.current_char == " " or self.current_char == "\n" or
                self.current_char == "\t"
            ):
                self.advance()
                continue

            # 匹配数字
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
                continue
            # 匹配符号
            elif self.current_char == "+":
                tokens.append(Token(TT_ADD, pos=self.pos.copy()))
                self.advance()
                continue
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS, pos=self.pos.copy()))
                self.advance()
                continue
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL, pos=self.pos.copy()))
                self.advance()
                continue
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV, pos=self.pos.copy()))
                self.advance()
                continue
            elif self.current_char == "=":
                tokens.append(Token(TT_EQUAL, pos=self.pos.copy()))
                self.advance()
                continue

            # 字符串
            elif self.current_char == "\"":
                tokens.append(self.make_string())
                continue
            elif self.current_char == ";":
                tokens.append(Token(TT_SEMI, pos=self.pos.copy()))
                self.advance()
                continue
            elif self.current_char == ",":
                tokens.append(Token(TT_COMMA, pos=self.pos.copy()))
                self.advance()
                continue

            elif is_start(self.current_char):
                tokens.append(self.make_identifier())
                continue

            # 序列
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAR, pos=self.pos.copy()))
                self.advance()
                continue
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAR, pos=self.pos.copy()))
                self.advance()
                continue

            else:
                ThrowException.throw(
                    UnknownSyntaxError('Unknown syntax', self.pos)
                )

        tokens.append(Token(TT_EOF, pos=self.pos.copy()))
        return tokens

    def make_string(self) -> Token:
        pos = self.pos.copy()
        string = ""
        while True:
            self.advance()
            if self.current_char is None:
                break
            else:
                if self.current_char == "\"":
                    self.advance()
                    break
            string += self.current_char
        return Token(TT_STRING, string, pos=pos)

    def make_identifier(self) -> Token:
        if self.current_char is None:
            raise RuntimeError
        identifer = self.current_char
        while self.current_char is not None:
            self.advance()
            if self.current_char is None:
                break
            if not is_identifier_center_char_or_end_char(
                self.current_char
            ):
                break
            identifer += self.current_char
        token_val: str = identifer.strip()
        token_type: str = TT_IDENTIFER if token_val not in TT_KEYWORDS else TT_KEYWORD
        return Token(token_type, token_val, self.pos.copy())

    def make_number(self) -> Token:
        if self.current_char is None:
            raise Nerver
        string: str = self.current_char
        while self.advance():
            if (self.current_char
                not in DIGITS) and (self.current_char != "."):
                break
            if self.current_char is None:
                raise SystemExit
            string += self.current_char
        if string.count('.') > 1:
            ThrowException.throw(
                TooDotsError(
                    f"At most one dot appears in a number, but more than one appear: '{string}'",
                    self.pos
                )
            )
        type_function = TT_FLOAT if "." in string else TT_INT
        return Token(type_function, string, pos=self.pos.copy())

    def skip_annotation(self) -> None:
        while True:
            self.advance()
            if self.current_char == "\n":
                self.advance()
                break
