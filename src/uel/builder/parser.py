from uel.builder.codeobject import UELCode
from uel.builder.token import UELToken
from uel.constants import Token as TokenConstants
from uel.builder.ast import *  # noqa
from uel.builder.precedence import Precedence, PREFIX
from uel.exceptions import uel_set_error_string, UELSyntaxError


class Parser:
    def __init__(self, source, tokens: list[UELToken]):
        self.source = source
        self.tokens = tokens
        self.current_index = 0

        self.prefix_expression = {}
        self.infix_expression = {}
        self.postfix_expression = {}

        self.register_prefix_expression(
            TokenConstants.TT_NUMBER, self.parse_number
        )
        self.register_prefix_expression(
            TokenConstants.TT_STRING, self.parse_string
        )
        self.register_prefix_expression(
            TokenConstants.TT_IDENTIFIER, self.parse_name
        )

        self.register_prefix_expression(
            TokenConstants.TT_LPAR,
            self.parse_grouped_expression
        )
        self.register_prefix_expression(
            TokenConstants.TT_MINUS,
            self.parse_prefix_expression
        )
        self.register_prefix_expression(
            TokenConstants.TT_PLUS,
            self.parse_prefix_expression
        )
        self.register_infix_expression(
            TokenConstants.TT_EQEQUAL,
            self.parse_infix_expression
        )
        self.register_infix_expression(
            TokenConstants.TT_PLUS, self.parse_infix_expression
        )
        self.register_infix_expression(
            TokenConstants.TT_MINUS,
            self.parse_infix_expression
        )
        self.register_infix_expression(
            TokenConstants.TT_STAR, self.parse_infix_expression
        )
        self.register_infix_expression(
            TokenConstants.TT_SLASH,
            self.parse_infix_expression
        )

    def register(self, dictionary, key, value):
        dictionary[key] = value

    def register_prefix_expression(self, key, value):
        self.register(self.prefix_expression, key, value)

    def register_infix_expression(self, key, value):
        self.register(self.infix_expression, key, value)

    def peek_token(self, relative) -> UELToken | None:
        try:
            return self.tokens[self.current_index + relative]
        except IndexError:
            return None

    @property
    def next_token(self) -> UELToken | None:
        return self.peek_token(1)

    @property
    def current_token(self) -> UELToken | None:
        return self.peek_token(0)

    @property
    def token(self) -> UELToken | None:
        """
        alias to "current_token"
        """

        return self.current_token

    @property
    def last_token(self) -> UELToken | None:
        return self.peek_token(-1)

    def advance(self) -> None:
        self.current_index += 1

    def rollback(self) -> None:
        self.current_index -= 1

    def parse(self) -> AST:
        return self.parse_module()

    def parse_module(self) -> AST:
        statements = []

        start = self.token.start

        while self.token is not None and self.token.token_type != TokenConstants.TT_EOF:
            statements.append(self.parse_statement())
            self.advance()

        end = self.last_token.end

        return Module(statements, start, end)

    def parse_statement(self) -> AST:
        return self.parse_expression()

    def parse_number(self):
        return NumberLiteral(
            self.token.token_value, self.token.start,
            self.token.end
        )

    def parse_name(self):
        return Name(
            self.token.token_value, self.token.start,
            self.token.end
        )

    def parse_string(self):
        return StringLiteral(
            self.token.token_value, self.token.start,
            self.token.end
        )

    def parse_expression(self, precedence=0) -> AST:
        token = self.token
        try:
            node = self.prefix_expression[token.token_type]()
        except KeyError:
            uel_set_error_string(
                UELSyntaxError,
                f"Invalid token type: {token.token_type}",
                self.source, self.token.start, self.token.end
            )
        while self.next_token.token_type not in [
            TokenConstants.TT_SEMI, TokenConstants.TT_EOF
        ] and precedence < get_precedence(self.next_token):
            infix = self.infix_expression.get(
                self.next_token.token_type
            )
            if infix is None:
                # print("What the fuck", self.next_token.token_type)
                return node
            self.advance()

            node = infix(node)
        return node

    def parse_prefix_expression(self):
        op = self.current_token
        self.advance()
        res = self.parse_expression(PREFIX)
        return UnaryOp(res, op.token_value, op.start, res.end)

    def parse_grouped_expression(self):
        self.advance()
        res = self.parse_expression()
        if self.next_token.token_type == TokenConstants.TT_RPAR:
            self.advance()
        return res

    def parse_infix_expression(self, leftexp: AST):
        start = leftexp.start
        op = self.current_token
        self.advance()
        right = self.parse_expression(get_precedence(op))
        end = self.current_token.end
        return BinOp(
            left=leftexp,
            op=op.token_value,
            right=right,
            start=start,
            end=end
        )


def get_precedence(token: UELToken) -> int:
    return getattr(Precedence(), token.token_type)


def uel_generate_ast(source, tokens):
    return Parser(source, tokens).parse()


def uel_ast_parser(code: UELCode) -> None:
    code.co_ast = uel_generate_ast(
        code.co_source, code.co_tokens
    )
