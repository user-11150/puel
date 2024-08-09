from uel.builder.codeobject import UELCode
import uel.builder.ast as uelast
from uel.objects.string import uel_string_from_python_str
from uel.objects.number import uel_number_from_python_number
from uel.opcodes import *
from uel.instruction import Instruction


class Compiler:
    """
    Compile AST into bytecode
    """
    def __init__(self, filename, source, ast):
        self.filename = filename
        self.source = source
        self.ast = ast

        self.co_consts: list[object] = []
        self.co_names: list[str] = []
        self.co_instructions = []
        self.stacksize = 0

    def const(self, value):
        if value in self.co_consts:
            return self.co_consts.index(value)
        self.co_consts.append(value)
        return len(self.co_consts) - 1

    def name(self, name):
        if name in self.co_names:
            return self.co_names.index(name)
        self.co_names.append(name)
        return len(self.co_names) - 1

    def make_literal(self, node: uelast.Literal):
        if node.kind == "StringLiteral":
            return uel_string_from_python_str(node.value)
        elif node.kind == "NumberLiteral":
            return uel_number_from_python_number(float(node.value))

    def _compile_literal(self, node):
        const = self.make_literal(node)
        self.addop(LOAD_CONST, self.const(const), node.start.line)

    def _compile_block(self, ast: uelast.Block):
        code = Compiler(self.filename, self.source,
                        ast.statements).compile()
        self.addop(LOAD_CONST, self.const(code), ast.start.line)
        self.addop(EXEC_CODE, None, ast.start.line)

    def _compile_expr(self, node):
        if isinstance(node, uelast.Literal):
            self._compile_literal(node)
        elif node.kind == "Name":
            index = self.name(node.name)
            self.addop(LOAD_NAME, index, node.start.line)
        elif node.kind == 'BinOp':
            operator_to_opcode = {
                "+": ADD,
                "-": MINUS,
                "*": MULT,
                "/": DIV
            }
            if node.op in operator_to_opcode:
                self._compile_expr(node.left)
                self._compile_expr(node.right)
                self.addop(
                    operator_to_opcode[node.op], None, node.start.lineno
                )
            elif node.op == "->":
                self._compile_expr(node.left)
                if node.right.kind != "Name":
                    raise ValueError("Invalid node")
                idx = self.name(node.right.name)
                self.addop(LOAD_ATTR, idx, node.start.line)
        else:
            raise ValueError(
                f"Invalid node {node.kind} (When you get this error. Please upload an issue for UEL)"
            )

    def _compile_assign(self, node: uelast.Assign):
        if node.left.kind == "Name":
            self._compile_expr(node.right)
            self.addop(
                STORE_NAME, self.name(node.left.name), node.start.line
            )

    def addop(self, opcode, value, lineno):
        self.co_instructions.append(Instruction(opcode, value, lineno))

    def _compile(self, ast):
        if isinstance(ast, uelast.Assign):
            self._compile_assign(ast)
        elif isinstance(ast, uelast.Module):
            self._compile_block(ast.body)
        elif isinstance(ast, uelast.Block):
            self._compile_block(ast)

        elif isinstance(ast, list):
            for ast_ in ast:
                self._compile(ast_)
        else:
            self._compile_expr(ast)

    def compile(self):
        self._compile(self.ast)

        return UELCode(
            co_filename=self.filename,
            co_consts=self.co_consts,
            co_instructions=self.co_instructions,
            co_source=self.source,
            co_stacksize=self.stacksize,
            co_names=self.co_names
        )


def uel_compiler(filename, source, ast) -> UELCode:
    compiler = Compiler(filename, source, ast)

    return compiler.compile()
