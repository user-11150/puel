"""
语法解释器
"""

#pylint:disable=C0103

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
from uel.core.builder.ast.SingleNode import SingleNode
from uel.core.builder.ast.VariableNode import VariableNode
from uel.core.builder.ast.Constant import Constant
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
from uel.core.builder.token.TokenConstants import TT_INT
from uel.core.builder.token.TokenConstants import TT_FLOAT
from uel.core.builder.token.TokenConstants import TT_EQUAL

class Parser:
    """
    语法解析器
    """
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

    def rollback(self) -> Any:
        """
        回滚至上一个Token
        """
        self.idx -= 1
        try:
            self.current_token = self.tokens[self.idx]
        except IndexError:
            self.current_token = None
        return self.current_token

    def validate_expr(self) -> ExpressionNode:
        """
        expr:
            ->: <left> <op> <right>
            ->: <val>
            ->: <left> = <right>
        """
        def wrap_single(tok: TokenNode) -> Constant:
            """
            实现一个值token => AST
            """
            val = tok.token_val
            def mapping(typ):
                if typ in (TT_INT, TT_FLOAT):
                    return "number"
                return typ
            typ = mapping(tok.token_type)
            
            return Constant(val, typ)

        left_token = None
        op = None
        right_token = None # pylint: disable=W
        
        val = None # pylint: disable=W
        
        left_token = self.current_token
        if left_token.token_type == TT_EOF:
            error_object = UELSyntaxError('EOF error')
            ThrowException.throw(error_object)
        op: TokenNode = self.advance()
        if op.token_type not in TT_OP:
            container = ExpressionNode(None)
            left_val = wrap_single(left_token)
            container.val = left_val
            self.rollback()
            return container
        self.advance()
        right_val = self.validate_expr().val
        
        ast_type: Any

        if op.token_type == TT_ADD:
            ast_type = AddNode
        elif op.token_type == TT_MINUS:
            ast_type = MinusNode
        elif op.token_type == TT_MUL:
            ast_type = MultNode
        elif op.token_type == TT_DIV:
            ast_type = DivNode
        elif op.token_type == TT_EQUAL:
            ast_type = VariableNode
        else:
            op: Never
        
        left_val = wrap_single(left_token)
        
        node = ast_type(left_val,right_val)
        # print(node)
        return ExpressionNode(node)

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
