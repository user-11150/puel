from typing import Any, Self, Union

from objprint import objprint

from uel.builder.ast.abstractnode import AbstractNode
from uel.builder.ast.addnode import AddNode
from uel.builder.ast.binopnode import BinOpNode
from uel.builder.ast.callfunctionnode import CallFunctionNode
from uel.builder.ast.constant import Constant
from uel.builder.ast.containernode import ContainerNode
from uel.builder.ast.divnode import DivNode
from uel.builder.ast.expressionnode import ExpressionNode
from uel.builder.ast.functionnode import FunctionNode
from uel.builder.ast.ifnode import IfNode
from uel.builder.ast.importnode import ImportNode
from uel.builder.ast.isequal import IsEqual
from uel.builder.ast.minusnode import MinusNode
from uel.builder.ast.modulenode import ModuleNode
from uel.builder.ast.multnode import MultNode
from uel.builder.ast.pushstackvaluenode import PushStackValueNode
from uel.builder.ast.putnode import PutNode
from uel.builder.ast.repeatnode import RepeatNode
from uel.builder.ast.returnnode import ReturnNode
from uel.builder.ast.sequencenode import SequenceNode
from uel.builder.ast.singlenode import SingleNode
from uel.builder.ast.variablenode import VariableNode
from uel.builder.ast.simplefunctioncall import SimpleFunctionCall
from uel.builder.token.tokenconstants import (
    TT_ADD, TT_CALL, TT_COMMA, TT_DIV, TT_ELSE, TT_END, TT_EOF, TT_EQUAL,
    TT_FLOAT, TT_FUNCTION, TT_IDENTIFER, TT_IF, TT_IMPORT, TT_INT, TT_IS,
    TT_KEYWORD, TT_KEYWORDS, TT_MINUS, TT_MUL, TT_OP, TT_PUSH, TT_PUT,
    TT_REPEAT, TT_RETURN, TT_SEMI, TT_STRING, TT_LSQB, TT_RSQB, TT_LPAR,
    TT_RPAR
)
from uel.builder.token.tokennode import TokenNode
from uel.errors.raiseerror import RaiseError
from uel.errors.throwexception import ThrowException
from uel.errors.uelsyntaxerror import UELSyntaxError
from uel.pyexceptions.nerver import Nerver
from uel.tools.func.wrapper.single_call import single_call

__all__ = ["Parser"]


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
            if tok.token_type == TT_LSQB:
                return self.validate_sequence_node(self.current_token)

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

        def isvalue(token):
            if token is None:
                return False
            return token.token_type in [
                TT_INT, TT_FLOAT, TT_STRING, TT_IDENTIFER, TT_LSQB
            ]

        def isop(token):
            if token is None:
                return False
            return token.token_type in [
                TT_ADD, TT_MINUS, TT_MUL, TT_DIV, TT_IS, TT_EQUAL
            ]

        def get_op_constructor(token):
            return (
                {
                    TT_ADD: AddNode,
                    TT_MINUS: MinusNode,
                    TT_MUL: MultNode,
                    TT_DIV: DivNode,
                    TT_IS: IsEqual,
                    TT_EQUAL: VariableNode
                }
            )[token.token_type]

        left = self.current_token
        if isvalue(left):
            leftval = wrap_single(left)
            self.advance()
        elif left.token_type == TT_LPAR:
            self.advance()
            leftval = self.validate_expr()
            self.advance()
            if self.current_token.token_type != TT_RPAR:
                raise UELSyntaxError(
                    f"Bad expr: {self.current_token}",
                    self.current_token.pos
                )
            self.advance()
        else:
            raise UELSyntaxError(
                f"Bad expr: {self.current_token}", self.current_token.pos
            )
        while True:
            op = self.current_token
            if isop(op):
                constructor = get_op_constructor(op)
            elif op is not None and op.token_type == TT_LPAR:
                args = self.validate_sequence_node(
                    self.current_token, TT_RPAR
                )
                leftval = SimpleFunctionCall(leftval, args)
                self.advance()
                continue
            else:
                self.rollback()
                return ExpressionNode(leftval)
            self.advance()
            right = self.current_token
            if isvalue(right):
                leftval = constructor(leftval, self.validate_expr())
                self.advance()
            elif right.token_type == TT_LPAR:
                self.advance()
                right = self.validate_expr()
                self.advance()
                if self.current_token.token_type != TT_RPAR:
                    raise UELSyntaxError(
                        f"Bad expr: {self.current_token}",
                        self.current_token.pos
                    )
                leftval = constructor(leftval, right)
                self.advance()
            else:
                raise UELSyntaxError("Need a op", self.current_token.pos)

    def validate_if(self) -> IfNode:
        last_token = self.current_token
        self.advance()
        if self.current_token is None:
            RaiseError(
                UELSyntaxError, "[Unknown Syntax] Syntax Error",
                last_token.pos
            )
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
            if not (
                self.current_token.token_type == TT_KEYWORD and
                self.current_token.token_val == TT_ELSE
            ):
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

    def validate_repeat_loop(self) -> RepeatNode:
        self.advance()

        # body
        result_node = RepeatNode()
        self.stmts(result_node)
        self.rollback()

        return result_node

    def validate_sequence(self, last_token) -> SequenceNode:
        if self.current_token is None or (
            self.current_token.token_type != TT_IDENTIFER and
            self.current_token.token_type != TT_SEMI
        ):
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

            RaiseError(
                UELSyntaxError, "SyntaxError", self.current_token.pos
            )
        return SequenceNode(sequence)

    def validate_sequence_node(
        self, last_token, eof=TT_RSQB
    ) -> SequenceNode:
        if self.current_token is None:
            RaiseError(
                UELSyntaxError,
                "SyntaxError: sequence need a LSQB, but get a EOF",
                last_token.pos
            )
        sequence = []
        self.advance()
        try:
            while True:
                if self.current_token.token_type == eof:
                    break
                sequence.append(self.validate_expr())
                self.advance()
                if self.current_token.token_type == TT_COMMA:
                    self.advance()
                    continue
        except Exception as e:
            raise e
            RaiseError(
                UELSyntaxError, "SyntaxError", self.current_token.pos
            )
        return SequenceNode(sequence)

    def validate_function(self) -> FunctionNode:
        last_token = self.current_token
        assert last_token is not None and last_token.pos is not None
        self.advance()
        if self.current_token is None:
            RaiseError(UELSyntaxError, "SyntaxError", last_token.pos)
        del last_token
        if self.current_token is None:
            raise

        if self.current_token.token_type != TT_IDENTIFER:
            RaiseError(
                UELSyntaxError, "SyntaxError", self.current_token.pos
            )
            raise SystemExit
        function_name = self.current_token.token_val
        last_token = self.current_token
        self.advance()
        args = self.validate_sequence(last_token)
        self.advance()
        fn = FunctionNode([], str(function_name), args.values)
        self.stmts(fn)
        self.rollback()
        return fn

    def validate_import(self) -> ImportNode:
        last_token = self.current_token
        if last_token is None:
            raise SystemExit
        self.advance()
        current = self.current_token
        if current is None or current.token_type != TT_STRING:
            if current is None:
                RaiseError(
                    UELSyntaxError, "Unknown Syntax", last_token.pos
                )
                raise SystemExit
            if current.token_type != TT_STRING:
                emsg = f'Libary name must be string literal, did you mean \n\'import "{current.token_val}"\'' if current.token_type == TT_IDENTIFER \
                    else "Libary name must be string literal"
                RaiseError(UELSyntaxError, emsg, current.pos)
            raise SystemExit
        assert type(current.token_val) is str
        return ImportNode(current.token_val)

    def stmt(self) -> Any:
        """
        stmt
        """
        if self.current_token is None:
            raise TypeError
        if self.current_token.token_type == TT_KEYWORD:
            if self.current_token.token_val == TT_PUSH:
                self.advance()
                node: ExpressionNode = self.validate_expr()
                return PushStackValueNode(node)
            elif self.current_token.token_val == TT_PUT:
                self.advance()
                node: ExpressionNode = self.validate_expr()  # type: ignore
                return PutNode(node)
            elif self.current_token.token_val == TT_CALL:
                self.advance()
                node: ExpressionNode = self.validate_expr()  # type: ignore
                return CallFunctionNode(node)
            elif self.current_token.token_val == TT_RETURN:
                self.advance()
                node: ExpressionNode = self.validate_expr()  # type: ignore
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
                RaiseError(
                    UELSyntaxError, "[Unknown Syntax] Syntax Error",
                    self.current_token.pos
                )
                raise SystemExit
        return self.validate_expr()

    def stmts(
        self, push_target: ContainerNode, eof_type: str = TT_EOF
    ) -> Any:
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
        self.stmts(result, TT_EOF)
        return result
