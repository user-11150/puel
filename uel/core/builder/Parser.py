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
from uel.core.builder.ast.PushStackValueNode import PushStackValueNode
from uel.core.builder.ast.PutNode import PutNode
from uel.core.builder.ast.IfNode import IfNode
from uel.core.builder.ast.IsEqual import IsEqual
from uel.core.builder.ast.RepeatNode import RepeatNode
from uel.core.builder.ast.FunctionNode import FunctionNode
from uel.core.builder.ast.SequenceNode import SequenceNode
from uel.core.builder.ast.ReturnNode import ReturnNode
from uel.core.builder.ast.CallFunctionNode import CallFunctionNode
from uel.core.builder.ast.ImportNode import ImportNode
from uel.core.errors.ThrowException import ThrowException
from uel.core.errors.RaiseError import RaiseError
from uel.core.errors.UELSyntaxError import UELSyntaxError
from uel.pyexceptions.Nerver import Nerver
from uel.core.builder.token.TokenNode import TokenNode
from uel.core.builder.token.TokenConstants import TT_TYPES
from uel.core.builder.token.TokenConstants import TT_EOF
from uel.core.builder.token.TokenConstants import TT_KEYWORDS
from uel.core.builder.token.TokenConstants import TT_KEYWORD
from uel.core.builder.token.TokenConstants import TT_ADD
from uel.core.builder.token.TokenConstants import TT_DIV
from uel.core.builder.token.TokenConstants import TT_MINUS
from uel.core.builder.token.TokenConstants import TT_MUL
from uel.core.builder.token.TokenConstants import TT_OP
from uel.core.builder.token.TokenConstants import TT_INT
from uel.core.builder.token.TokenConstants import TT_FLOAT
from uel.core.builder.token.TokenConstants import TT_EQUAL
from uel.core.builder.token.TokenConstants import TT_IDENTIFER
from uel.core.builder.token.TokenConstants import TT_STRING
from uel.core.builder.token.TokenConstants import TT_PUT
from uel.core.builder.token.TokenConstants import TT_PUSH
from uel.core.builder.token.TokenConstants import TT_IF
from uel.core.builder.token.TokenConstants import TT_ELSE
from uel.core.builder.token.TokenConstants import TT_END
from uel.core.builder.token.TokenConstants import TT_IS
from uel.core.builder.token.TokenConstants import TT_REPEAT
from uel.core.builder.token.TokenConstants import TT_COMMA
from uel.core.builder.token.TokenConstants import TT_FUNCTION
from uel.core.builder.token.TokenConstants import TT_SEMI
from uel.core.builder.token.TokenConstants import TT_CALL
from uel.core.builder.token.TokenConstants import TT_RETURN
from uel.core.builder.token.TokenConstants import TT_IMPORT
from uel.tools.func.wrapper.single_call import single_call
from typing import (Self,
                    Any)
from objprint import objprint

class Parser:
    """
    语法解析器
    """
    def __init__(self, tokens: list[TokenNode]):
        self.tokens = tokens
        self.current_token: TokenNode | None
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
#            def mapping(typ: str) -> str:
#                if typ in (TT_INT, TT_FLOAT):
#                    return "number"
#                elif typ == TT_IDENTIFER:
#                    return "name"
#                else:
#                    RaiseError(UELSyntaxError, f"Incorrect use of keyword: {typ}", tok.pos)

            typ = None
            if tok.token_val == "TOP":
                typ = "stack_top"
            if tok.token_val == "true" or tok.token_val == "false":
                typ = "boolean"
            
            mapping = {
                TT_INT: "number",
                TT_FLOAT: "number",
                TT_IDENTIFER: "name",
                TT_STRING: "string"
            }
            token_type: str = tok.token_type
            if typ is None:
                typ = mapping[token_type]
            return Constant(val, typ)
        

        left_token = self.current_token
        if left_token is None or left_token.token_type == TT_EOF:
            if left_token is None:
                raise Nerver
            error_object = UELSyntaxError('EOF error', left_token.pos)
            ThrowException.throw(error_object)
        op: TokenNode = self.advance()
        if op is None or op.token_type not in TT_OP and not (op.token_type == TT_KEYWORD and op.token_val == TT_IS):
            container = ExpressionNode(None)
            left_val = wrap_single(left_token)
            container.val = left_val
            self.rollback()
            return container
        self.advance()
        right_val = self.validate_expr().val
        left_val = wrap_single(left_token)
        
        ast_type: Any
        if op.token_type == TT_ADD:
            ast_type = AddNode
        elif op.token_type == TT_MINUS:
            ast_type = MinusNode
        elif op.token_type == TT_MUL:
            ast_type = MultNode
        elif op.token_type == TT_DIV:
            ast_type = DivNode
        elif op.token_type == TT_KEYWORD and op.token_val == TT_IS:
            ast_type = IsEqual
        elif op.token_type == TT_EQUAL:
            ast_type = VariableNode
        else:
            raise ValueError("op.token_type is not support")
        
        node: AbstractNode = ast_type(left_val,right_val) # type: ignore
        # print(node)
        return ExpressionNode(node) # type: ignore

    def validate_if(self):
        last_token = self.current_token
        self.advance()
        if self.current_token is None:
            RaiseError(UELSyntaxError, "[Unknown Syntax] Syntax Error", last_token.pos)
            raise SystemExit
        del last_token
        condition = self.validate_expr()
        self.advance()
        body_result = ContainerNode()
        self.stmts(body_result, TT_EOF)
        
        
        class GotoNoElseCase(Exception):
            pass
        
        try:
            if self.current_token is None:
                raise GotoNoElseCase
            if not (self.current_token.token_type == TT_KEYWORD \
             and self.current_token.token_val == TT_ELSE):
                raise GotoNoElseCase
        except GotoNoElseCase:
            else_case = ContainerNode()
            self.rollback()
            return IfNode(condition, body_result, else_case)
        
        else_case = ContainerNode()
        self.advance()
        self.stmts(else_case, TT_EOF)
        self.rollback()
        return IfNode(condition, body_result, else_case)

    def validate_repeat_loop(self):
        self.advance()
        
        # body
        result_node = RepeatNode()
        self.stmts(result_node)
        self.rollback()
        
        return result_node

    def validate_sequence(self, last_token):
        if self.current_token is None or (self.current_token.token_type != TT_IDENTIFER and self.current_token.token_type != TT_SEMI):
            RaiseError(UELSyntaxError, "SyntaxError", last_token.pos)
        sequence = []
        try:
            while True:
                if self.current_token.token_type == TT_SEMI:
                    break
                assert self.current_token.token_type == TT_IDENTIFER
                sequence.append(self.current_token.token_val)
                self.advance()
                if self.current_token.token_type == TT_COMMA:
                    self.advance()
                    continue
        except Exception:
            
            RaiseError(UELSyntaxError, "SyntaxError", self.current_token.pos)
        return SequenceNode(sequence)

    def validate_function(self):
        last_token = self.current_token
        self.advance()
        if self.current_token is None:
            RaiseError(UELSyntaxError, "SyntaxError", last_token.pos)
        del last_token
        if self.current_token.token_type != TT_IDENTIFER:
            RaiseError(UELSyntaxError, "SyntaxError", self.current_token.pos)
        function_name = self.current_token.token_val
        last_token = self.current_token
        self.advance()
        args = self.validate_sequence(last_token)
        self.advance()
        fn = FunctionNode([], function_name, args.values)
        self.stmts(fn)
        self.rollback()
        return fn

    def validate_import(self):
        last_token = self.current_token
        self.advance()
        current = self.current_token
        if current is None or current.token_type != TT_STRING:
            if current is None:
                RaiseError(UELSyntaxError,"Unknown Syntax", last_token.pos)
            elif current.token_type != TT_STRING:
                emsg = f'Libary name must be string literal, did you mean \n\'import "{current.token_val}"\'' if current.token_type == TT_IDENTIFER \
                        else "Libary name must be string literal"
                RaiseError(UELSyntaxError, emsg, self.current_token.pos)
        return ImportNode(self.current_token.token_val)

    def stmt(self) -> AbstractNode:
        """
        stmt
        """
        if self.current_token is None:
            raise TypeError
        if self.current_token.token_type == TT_KEYWORD:
            if self.current_token.token_val == TT_PUSH:
                self.advance()
                node: ExpressionNode = self.validate_expr() # type: ignore
                return PushStackValueNode(node)
            elif self.current_token.token_val == TT_PUT:
                self.advance()
                node: ExpressionNode = self.validate_expr() # type: ignore
                return PutNode(node)
            elif self.current_token.token_val == TT_CALL:
                self.advance()
                node: ExpressionNode = self.validate_expr() # type: ignore
                return CallFunctionNode(node)
            elif self.current_token.token_val == TT_RETURN:
                self.advance()
                node: ExpressionNode = self.validate_expr() # type: ignore
                return ReturnNode(node)
            elif self.current_token.token_val == TT_END:
                return
            elif self.current_token.token_val == TT_IF:
                return self.validate_if()
            elif self.current_token.token_val == TT_REPEAT:
                return self.validate_repeat_loop()
            elif self.current_token.token_val == TT_FUNCTION:
                return self.validate_function()
            elif self.current_token.token_val == TT_IMPORT:
                return self.validate_import()
            else:
                RaiseError(UELSyntaxError, "[Unknown Syntax] Syntax Error", self.current_token.pos)
                raise SystemExit
        return self.validate_expr()

    def stmts(self, push_target: ContainerNode, eof_type: str=TT_EOF) -> Any:
        if eof_type not in TT_TYPES:
            raise TypeError(f'Cannot parse {eof_type}: This is developer error')
        # while self.current_token.token_type != TT_EOF and self.current_token is not None:
        while self.current_token is not None and self.current_token.token_type != TT_EOF:
            if self.current_token is None:
                break
            if self.current_token.token_type == TT_END:
                self.advance()
                break
            result_node = self.stmt()
            if result_node is not None:
                push_target.push(result_node)
                self.advance()
            else:
                self.advance()
                break
            
        return push_target

    def parse(self) -> ModuleNode:
        """
        Tokens => AST
        """
        result = ModuleNode()
        self.stmts(result,TT_EOF)
        return result
