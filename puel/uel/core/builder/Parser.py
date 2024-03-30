from typing import Self
from typing import Any
from typing import Never
from uel.core.builder.ast.AbstractNode import AbstractNode
from uel.core.builder.ast.AddNode import AddNode
from uel.core.builder.ast.BinOpNode import BinOpNode
from uel.core.builder.ast.ContainerNode import ContainerNode
from uel.core.builder.ast.DivNode import DivNode
from uel.core.builder.ast.ExpressionNode import ExpressionNode
from uel.core.builder.ast.MinusNode import MinusNode
from uel.core.builder.ast.ModuleNode import ModuleNode
from uel.core.builder.ast.MultNode import MultNode
from uel.core.errors.ThrowException import ThrowException
from uel.core.errors.RaiseError import RaiseError
from uel.core.errors.UELSyntaxError import UELSyntaxError
from uel.core.builder.token.TokenNode import TokenNode
from uel.core.builder.token.TokenConstants import TT_TYPES
from uel.core.builder.token.TokenConstants import TT_EOF
from uel.core.builder.token.TokenConstants import TT_KEYWORDS
from uel.core.builder.token.TokenConstants import TT_ADD
from uel.core.builder.token.TokenConstants import TT_DIV
from uel.core.builder.token.TokenConstants import TT_MINUS
from uel.core.builder.token.TokenConstants import TT_MUL
from uel.core.builder.token.TokenConstants import TT_OP
from uel.core.builder.token.TokenConstants import TT_VALS

class Parser:
    def __init__(self, tokens: list[TokenNode]):
        self.tokens = tokens
        self.current_token = None
        self.idx = -1
        
        self.advance()

    def advance(self: Self) -> Any:
        """
        获取下一个Token
        """
        
        # 当前index加一
        self.idx += 1
        try:
            # 将当前token设置为index加一后的结果
            self.current_token = self.tokens[self.idx]
        except IndexError:
            # 因为有的时候可能是最后一个时执行了advance
            self.current_token = None
        return self.current_token

    def validate_expr(self,container=None) -> ExpressionNode:
        print(3)
        container = ExpressionNode(None)
        left_token = None
        op = None
        right_token = None
        
        val = None
        
        left_token = self.current_token
        if left_token.token_type == TT_EOF:
            error_object = UELSyntaxError('EOF error')
            ThrowException.throw(error_object)
        op: TokenNode = self.advance()
        if op.token_type not in TT_OP and op.token_type not in TT_VALS:
            container.val = left_token
            return container
        self.advance()
        self.right = self.validate_expr()
        
        ast_type: Any

        if op.token_type == TT_ADD:
            ast_type = AddNode
        elif op.token_type == TT_MINUS:
            ast_type = MinusNode
        elif op.token_type == TT_MUL:
            ast_type = MultNode
        elif op.token_type == TT_DIV:
            ast_type = DivNode
        else:
            op: Never
        
        node = ast_type(left_token,right_token)
        print(node)
        return node

    def stmt(self) -> AbstractNode:
        if self.current_token.token_type in TT_KEYWORDS:
            error_object = UELSyntaxError("Cannot parser keyword on now")
            ThrowException.throw(error_object)
        return self.validate_expr()

    def stmts(self, push_target: ContainerNode, eof_type: TT_TYPES) -> AbstractNode:
        if eof_type not in TT_TYPES:
            raise TypeError(f'Cannot parse {eof_type}: This is developer error')
        # while self.current_token.token_type != TT_EOF and self.current_token is not None:
        while self.current_token is not None and self.current_token.token_type != TT_EOF:
            push_target.push(self.stmt())
            self.advance()
        return push_target

    def parse(self) -> ModuleNode:
        """
        Tokens => AST
        """
        result = ModuleNode()
        self.stmts(result,TT_EOF)
        return result
