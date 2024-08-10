"""
Priority
"""

LOWEST = 0
EQUALS = 1
LESSGREATER = 2
SUM = 3
PRODUCT = 4
PREFIX = 5
CALL = 6
INDEX = 7
MAX = 8


class Precedence:
    def __getattr__(self, name):
        return 0

    TT_ASSIGN: int = EQUALS
    TT_IDENTIFIER: int = LOWEST
    TT_STRING: int = LOWEST
    TT_NUMBER: int = LOWEST
    TT_LPAR: int = CALL
    TT_RPAR: int = CALL
    TT_EQEQUAL: int = EQUALS
    TT_PLUS: int = SUM
    TT_MINUS: int = SUM
    TT_STAR: int = PRODUCT
    TT_SLASH: int = PRODUCT
    TT_ATTR: int = INDEX
