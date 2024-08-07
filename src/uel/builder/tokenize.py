# -*- coding: utf-8 -*-
# Generate in 08/03/24 by tools/generate/__init__.py
from uel.internal.uelcore_internal_exceptions import throw
from uel.exceptions import UELSyntaxError, uel_set_error_string
from uel.builder.codeobject import UELCode
from uel.builder.token import UELToken
import typing as t
numbers = '0123456789'
ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
TT_IDENTIFIER = 'TT_IDENTIFIER'
TT_STRING = 'TT_STRING'
TT_LPAR = 'TT_LPAR'
TT_RPAR = 'TT_RPAR'
TT_PLUS = 'TT_PLUS'
TT_MINUS = 'TT_MINUS'
TT_STAR = 'TT_STAR'
TT_SLASH = 'TT_SLASH'
TT_NEWLINE = 'TT_NEWLINE'
TT_KEYWORDS = []
TT_KEYWORD = 'TT_KEYWORD'
TT_EOF = 'TT_EOF'

class Token:
    TT_IDENTIFIER = 'TT_IDENTIFIER'
    TT_STRING = 'TT_STRING'
    TT_LPAR = 'TT_LPAR'
    TT_RPAR = 'TT_RPAR'
    TT_PLUS = 'TT_PLUS'
    TT_MINUS = 'TT_MINUS'
    TT_STAR = 'TT_STAR'
    TT_SLASH = 'TT_SLASH'
    TT_NEWLINE = 'TT_NEWLINE'
    TT_KEYWORDS = []
    TT_KEYWORD = 'TT_KEYWORD'
    TT_EOF = 'TT_EOF'

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

    def idx_as_line_and_col(self, idx):
        return UELToken.idx_as_line_and_col(self.source, idx)

    def make_tokens(self) -> list[UELToken]:
        tokens = []
        while self.current_char is not None:
            start_position = self.current_idx
            if start_position <= len(self.source):
                start_line, start_col = UELToken.idx_as_line_and_col(self.source, start_position)
            if self.current_char == ' ':
                self.advance()
                continue
            elif self.current_char == '#':
                while self.advance() != '\n':
                    pass
            elif self.current_char == '(':
                self.advance()
                tokens.append(UELToken(TT_LPAR, '(', start_line, start_col, *UELToken.idx_as_line_and_col(self.source, self.current_idx)))
            elif self.current_char == ')':
                self.advance()
                tokens.append(UELToken(TT_RPAR, ')', start_line, start_col, *UELToken.idx_as_line_and_col(self.source, self.current_idx)))
            elif self.current_char == '+':
                self.advance()
                tokens.append(UELToken(TT_PLUS, '+', start_line, start_col, *UELToken.idx_as_line_and_col(self.source, self.current_idx)))
            elif self.current_char == '-':
                self.advance()
                tokens.append(UELToken(TT_MINUS, '-', start_line, start_col, *UELToken.idx_as_line_and_col(self.source, self.current_idx)))
            elif self.current_char == '*':
                self.advance()
                tokens.append(UELToken(TT_STAR, '*', start_line, start_col, *UELToken.idx_as_line_and_col(self.source, self.current_idx)))
            elif self.current_char == '/':
                self.advance()
                tokens.append(UELToken(TT_SLASH, '/', start_line, start_col, *UELToken.idx_as_line_and_col(self.source, self.current_idx)))
            elif self.current_char == '\n':
                self.advance()
                tokens.append(UELToken(TT_NEWLINE, '\n', start_line, start_col, *UELToken.idx_as_line_and_col(self.source, self.current_idx)))
            elif self.is_identifier_start(self.current_char):
                identifier = self.make_identifier()
                token_type = TT_KEYWORD if identifier in TT_KEYWORDS else TT_IDENTIFIER
                end_line, end_col = UELToken.idx_as_line_and_col(self.source, self.current_idx)
                tokens.append(UELToken(token_type, identifier, start_line, start_col, end_line, end_col))
                self.advance()
            elif self.current_char in ['"', "'"]:
                start = self.current_char
                res = ''
                while True:
                    self.advance()
                    if self.current_char == '\\':
                        self.advance()
                        if self.current_char == start:
                            res += start
                        else:
                            uel_set_error_string(UELSyntaxError, 'Anomalous backlash in string', self.source, self.idx_as_line_and_col(self.current_idx))
                        continue
                    if self.current_char == start:
                        self.advance()
                        break
                    if self.current_char is None:
                        uel_set_error_string(UELSyntaxError, 'unterminated string literal', self.source, self.idx_as_line_and_col(start_position))
                    res += self.current_char
                end_line, end_col = UELToken.idx_as_line_and_col(self.source, self.current_idx)
                tokens.append(UELToken(TT_STRING, res, start_line, start_col, end_line, end_col))
                self.advance()
            else:
                uel_set_error_string(UELSyntaxError, 'Invalid character', self.source, self.idx_as_line_and_col(start_position))
        tokens.append(UELToken(Token.TT_EOF, None, None, None, None, None))
        return tokens

    @staticmethod
    def is_identifier_start(char):
        if char in ascii_letters:
            return True
        if '一' <= char <= '鿿':
            return True
        if char in ['_', '$']:
            return True
        return False

    @classmethod
    def is_identifier(cls, char):
        return cls.is_identifier_start(char) or char in numbers

    def make_identifier(self):
        result = ''
        while True:
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
    code.co_tokens = uel_generate_tokens(code.co_source)