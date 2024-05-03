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
TT_SEMI = "TT_SEMI"
TT_COMMA = "TT_COMMA"

TT_EOF = "TT_EOF"

TT_PUSH = "push"

# ≈ print
TT_PUT = "put"

TT_END = "end"
TT_IF = "if"
TT_ELSE = "else"

TT_IS = "is"
TT_REPEAT = "repeat"
TT_FUNCTION = "function"
TT_CALL = "call"
TT_RETURN = "return"

TT_VALS = [
    TT_STRING,
    TT_INT,
    TT_FLOAT
]

TT_OP = [TT_ADD,
         TT_MINUS,
         TT_MUL,
         TT_DIV,
         TT_EQUAL,
         TT_IS]
         
TT_KEYWORDS = [TT_PUSH,
               TT_PUT,
               TT_END,
               TT_IF,
               TT_ELSE,
               TT_IS,
               TT_REPEAT,
               TT_FUNCTION,
               TT_CALL,
               TT_RETURN]

TT_TYPES = [*TT_VALS,
            *TT_OP,
            *TT_KEYWORDS,
            TT_KEYWORD,
            TT_EOF]
