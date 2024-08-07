# -*- coding: utf-8 -*-
# Auto-generated by tools/generate/gen_tokenize.py from grammer/tokens
"""
UEL's tokenizer
"""

from uel.internal.uelcore_internal_exceptions import throw
from uel.exceptions import UELSyntaxError, uel_set_error_string
from uel.builder.codeobject import UELCode
from uel.builder.token import UELToken
from uel.builder.position import Position
import typing as t

numbers = '0123456789'
ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
TT_IDENTIFIER = 'TT_IDENTIFIER'
TT_STRING = 'TT_STRING'
TT_NUMBER = 'TT_NUMBER'
TT_ASSIGN = 'TT_ASSIGN'
TT_EQEQUAL = 'TT_EQEQUAL'
TT_LPAR = 'TT_LPAR'
TT_RPAR = 'TT_RPAR'
TT_PLUS = 'TT_PLUS'
TT_MINUS = 'TT_MINUS'
TT_STAR = 'TT_STAR'
TT_SLASH = 'TT_SLASH'
TT_EQUAL = 'TT_EQUAL'
TT_SEMI = 'TT_SEMI'
TT_KEYWORDS = [];TT_KEYWORD = 'TT_KEYWORD';TT_EOF = 'TT_EOF'
class Token:
    TT_IDENTIFIER = 'TT_IDENTIFIER'
    TT_STRING = 'TT_STRING'
    TT_NUMBER = 'TT_NUMBER'
    TT_ASSIGN = 'TT_ASSIGN'
    TT_EQEQUAL = 'TT_EQEQUAL'
    TT_LPAR = 'TT_LPAR'
    TT_RPAR = 'TT_RPAR'
    TT_PLUS = 'TT_PLUS'
    TT_MINUS = 'TT_MINUS'
    TT_STAR = 'TT_STAR'
    TT_SLASH = 'TT_SLASH'
    TT_EQUAL = 'TT_EQUAL'
    TT_SEMI = 'TT_SEMI'
    TT_KEYWORDS = [];TT_KEYWORD = 'TT_KEYWORD';TT_EOF = 'TT_EOF'
class UELTokenize:
    def __init__(self, source: t.Any) -> None:
        self.source = source
        self.current_idx = 0

    @property
    def current_char(self) -> str:
        return self.peek(0)

    def peek(self, relative):
        try:
            return self.source[self.current_idx + relative]
        except IndexError:
            return None

    def advance(self) -> str:
        self.current_idx += 1
        return self.current_char

    def rollback(self) -> str:
        self.current_idx -= 1
        return self.current_char

    def idx_as_position(self, idx):
        return UELToken.idx_as_position(self.source, idx)

    @property
    def current_position(self):
        return self.idx_as_position(self.current_idx)

    def make_tokens(self) -> list[UELToken]:
        tokens = []
        while self.current_char is not None:

            start_position = self.current_position


            if self.current_char == " " or self.current_char == "\n":
                self.advance()
                continue
            elif self.current_char == "#":
                while self.advance() not in [None, "\n"]:
                    pass


            elif self.current_char == ':' and self.peek(1) == '=':
                self.advance()
                self.advance()

                tokens.append(
                    UELToken(
                        TT_ASSIGN, ':=', start_position, self.current_position
                    )
                )

            elif self.current_char == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()

                tokens.append(
                    UELToken(
                        TT_EQEQUAL, '==', start_position, self.current_position
                    )
                )

            elif self.current_char == '(':
                self.advance()

                tokens.append(
                    UELToken(
                        TT_LPAR, '(', start_position, self.current_position
                    )
                )

            elif self.current_char == ')':
                self.advance()

                tokens.append(
                    UELToken(
                        TT_RPAR, ')', start_position, self.current_position
                    )
                )

            elif self.current_char == '+':
                self.advance()

                tokens.append(
                    UELToken(
                        TT_PLUS, '+', start_position, self.current_position
                    )
                )

            elif self.current_char == '-':
                self.advance()

                tokens.append(
                    UELToken(
                        TT_MINUS, '-', start_position, self.current_position
                    )
                )

            elif self.current_char == '*':
                self.advance()

                tokens.append(
                    UELToken(
                        TT_STAR, '*', start_position, self.current_position
                    )
                )

            elif self.current_char == '/':
                self.advance()

                tokens.append(
                    UELToken(
                        TT_SLASH, '/', start_position, self.current_position
                    )
                )

            elif self.current_char == '=':
                self.advance()

                tokens.append(
                    UELToken(
                        TT_EQUAL, '=', start_position, self.current_position
                    )
                )

            elif self.current_char == ';':
                self.advance()

                tokens.append(
                    UELToken(
                        TT_SEMI, ';', start_position, self.current_position
                    )
                )

            elif self.is_identifier_start(self.current_char):

                identifier = self.make_identifier()
                token_type = TT_KEYWORD if identifier in TT_KEYWORDS else TT_IDENTIFIER
                tokens.append(
                    UELToken(
                        token_type, identifier, start_position, self.current_position
                    )
                )
                self.advance()

            elif self.current_char in ['"', '\'']:

                start = self.current_char
                res = ""
                while True:
                    self.advance()
                    if self.current_char == "\\":
                        self.advance()
                        if self.current_char == start:
                            res += start

                        else:
                            uel_set_error_string(UELSyntaxError, "Anomalous backlash in string", self.source, self.current_position)
                        continue
                    if self.current_char == start:
                        self.advance()
                        break
                    if self.current_char is None:
                        uel_set_error_string(UELSyntaxError, "unterminated string literal", self.source, self.current_position)
                    res += self.current_char
                tokens.append(
                    UELToken(
                        TT_STRING, res, start_position, self.current_position
                    )
                )
                self.advance()

            elif self.current_char in '0123456789':

                result = ""
                while self.current_char in '0123456789.':
                    if "." in result and self.current_char == ".":
                        uel_set_error_string(UELSyntaxError, "Too many dots", self.source, self.current_position)
                    result += self.current_char
                    self.advance()
                tokens.append(
                    UELToken(
                        TT_NUMBER, result, start_position, self.current_position
                    )
                )


            else:
                uel_set_error_string(UELSyntaxError, "Invalid character", self.source, self.current_position)

            if self.current_char is None:
                break
        tokens.append(UELToken(Token.TT_EOF, None, None, None))

        return tokens

    @staticmethod
    def is_identifier_start(char_):
        if char_ in ascii_letters:
            return True
        if '一' <= char_ <= '鿿':
            return True
        if char_ in ["_", "$"]:
            return True
        return False

    @classmethod
    def is_identifier(cls, char_):
        return cls.is_identifier_start(char_) or char_ in numbers

    def make_identifier(self):
        result = ""

        while True:
            if self.current_char is None:
                break
            if self.is_identifier(self.current_char):
                result += self.current_char
                self.advance()
            else:
                break

        self.rollback()
        return result

def uel_generate_tokens(source: str) -> list[UELToken]:
    return UELTokenize(source).make_tokens()
def uel_tokenize(code: UELCode):
    assert code.co_source is not None
    code.co_tokens = uel_generate_tokens(code.co_source)
