TT_INT = "TT_INT"
TT_FLOAT = "TT_FLOAT"
TT_STRING = "TT_STRING"

TT_ADD = "TT_ADD"
TT_MINUS = "TT_MINUS"
TT_MUL = "TT_MUL"
TT_DIV = "TT_DIV"
TT_EQUAL = "TT_EQUAL"

TT_IDENTIFER = "TT_IDENTIFER"
TT_KEYWORD = "TT_KEYWORD"

TT_EOF = "TT_EOF"

TT_PUSH = "PUSH"

# ≈ print
TT_PUT = "PUT"

TT_END = "END"
TT_IF = "IF"
TT_ELSE = "ELSE"

TT_VALS = [
    TT_STRING,
    TT_INT,
    TT_FLOAT
]

TT_OP = [TT_ADD,
         TT_MINUS,
         TT_MUL,
         TT_DIV,
         TT_EQUAL]
         
TT_KEYWORDS = [TT_PUSH,
               TT_PUT,
               TT_END,
               TT_IF,
               TT_ELSE,]

TT_TYPES = [*TT_VALS,
            *TT_OP,
            *TT_KEYWORDS,
            TT_KEYWORD,
            TT_EOF]
