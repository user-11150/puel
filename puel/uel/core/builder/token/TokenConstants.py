TT_INT = "TT_INT"
TT_FLOAT = "TT_FLOAT"
TT_STRING = "TT_STRING"

TT_ADD = "TT_ADD"
TT_MINUS = "TT_MINUS"
TT_MUL = "TT_MUL"
TT_DIV = "TT_DIV"

TT_EOF = "TT_EOF"

TT_VALS = [
    TT_STRING,
    TT_INT,
    TT_FLOAT
]

TT_OP = [TT_ADD,
         TT_MINUS,
         TT_MUL,
         TT_DIV]

TT_KEYWORDS = []

TT_TYPES = [*TT_VALS,
            *TT_OP,
            *TT_KEYWORDS,
            
            TT_EOF]
