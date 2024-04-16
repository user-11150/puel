# 编译器（compiler）——UEL的编译阶段的介绍
## 1. 总体过程
1. Source => Tokens: 把源代码变成Token流，Token流是与源代码等价的，它方便了后续的判断。
2. Tokens => AST: 将Token流转化成AST，它与源代码是等价的，他是可以解决`如何准确的表示要执行的代码？`这个问题的解。
3. AST => Bytecodes: Bytecode它接近于汇编，虽然人不容易看懂，但是后续可以很方便的执行
> 它会经历两次转化，第一次它保留了部分AST第二次转化就不存在AST了
# 2. Source => Tokens
实现Source => Tokens的过程是由`uel.core.builder.Lexer.Lexer`这个类的make_tokens完成的，它转化之后得到`Sequence[TokenNode]`
## Token
源代码：`uel.core.builder.token.TokenNode`
### TokenType
```
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
               TT_PUT]

TT_TYPES = [*TT_VALS,
            *TT_OP,
            *TT_KEYWORDS,
            TT_KEYWORD,
            TT_EOF]
```
### TokenValue
tokenvalue由代码决定
# 3. Tokens => AST
源代码：`uel.core.builder.Parser.Parser`
# 4. AST => Bytecode
未完成