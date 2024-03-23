from uel.core.builder.ast.ModuleNode import ModuleNode
from uel.core.builder.ast.ContainerNode import ContainerNode
from uel.core.builder.ast.AbstractNode import AbstractNode
from uel.core.builder.token.TokenNode import TokenNode
from uel.core.builder.token.TokenConstants import * # pylint: disable=W

from typing import (Self,
                    Any)

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

    def stmts(self, push_target: ContainerNode, eof_type: TT_TYPES) -> AbstractNode:
        pass

    def parse(self) -> ModuleNode:
        """
        Tokens => AST
        """
        result = ModuleNode([])
        self.stmts(result,TT_EOF)
