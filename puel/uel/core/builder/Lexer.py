from typing import List
from string import digits as DIGITS
from uel.core.builder.Position import Position
from uel.core.builder.token.TokenNode import TokenNode as Token
from uel.core.builder.token.TokenConstants import TT_EOF
from uel.core.builder.token.TokenConstants import TT_ADD
from uel.core.builder.token.TokenConstants import TT_FLOAT
from uel.core.builder.token.TokenConstants import TT_INT
from uel.core.builder.token.TokenConstants import TT_MINUS
from uel.core.builder.token.TokenConstants import TT_STRING
from uel.core.errors.UnknownSyntaxError import UnknownSyntaxError
from uel.core.errors.TooDotsError import TooDotsError
from uel.core.errors.ThrowException import ThrowException

class Lexer:
    """
    源代码 => Tokens
    """
    def __init__(self,fn: str, content: str):
        self.fn: str = fn
        self.content: str = content
        #                   I,  L  C   F   C
        self.pos = Position(-1, 0, -1, fn, content)
        self.current_char = None
        self.advance()

    def advance(self) -> None:
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
            if self.current_char == "#":
                self.skip_annotation()
                continue
            if self.current_char == " " or self.current_char == "\n":
                self.advance()
                continue
            # 匹配数字
            if self.current_char in DIGITS:
                tokens.append(self.make_number())
                continue
            if self.current_char == "+":
                tokens.append(Token(TT_ADD,pos=self.pos.copy()))
                self.advance()
                continue
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS,pos=self.pos.copy()))
                continue
            ThrowException.throw(UnknownSyntaxError('Unknown syntax',self.pos))
            
        tokens.append(Token(TT_EOF,pos=self.pos.copy()))
        return tokens

    def make_number(self) -> Token:
        string: str = self.current_char
        while self.advance():
            if (self.current_char not in DIGITS) and (self.current_char != "."):
                break
            string += self.current_char
        if string.count('.') > 1:
            ThrowException.throw(TooDotsError(f"At most one dot appears in a number, but more than one appear: '{string}'",self.pos))
        type_function = TT_FLOAT if "." in string else TT_INT
        return Token(type_function,string,pos=self.pos.copy())

    def skip_annotation(self):
        while True:
            self.advance()
            if self.current_char == "\n":
                self.advance()
                break
