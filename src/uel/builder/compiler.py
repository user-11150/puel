from uel.builder.codeobject import UELCode
from uel.builder.ast import *
from uel.objects.string import uel_string_from_python_str
from uel.objects.number import uel_number_from_python_number
from uel.opcodes import *
from uel.instruction import Instruction
from uel.constants import File
from os.path import dirname, join
from uel.objects.none import uel_none


class Compiler:
    """
    Compile AST into bytecode
    """
    def __init__(self, filename, ast):
        self.ast = ast
        self.filename = filename

        self.co_consts: list[object] = []
        self.co_instructions = []

    def const(self, value):
        if value in self.co_consts:
            return self.co_consts.index(value)
        self.co_consts.append(value)
        return len(self.co_consts) - 1

    def make_literal(self, node: Literal):
        if node.kind == "StringLiteral":
            return uel_string_from_python_str(node.value)
        elif node.kind == "NumberLiteral":
            return uel_number_from_python_number(float(node.value))

    def _compile_literal(self, node):
        const = self.make_literal(node)
        self.addop(LOAD_CONST, self.const(const))

    def _compile_block(self, ast: Block):
        code = Compiler(self.filename, ast.statements).compile()
        self.addop(LOAD_CONST, self.const(code))
        self.addop(EXEC_CODE, None)

    def _compile_expr(self, node):
        if isinstance(node, Literal):
            self._compile_literal(node)
        elif node.kind == "Name":
            index = self.const(node.name)
            self.addop(LOAD_NAME, index)
        elif node.kind == "FunctionCall":
            node: FunctionCall
            for child in node.arguments:
                self._compile_expr(child)
            self.addop(LOAD_CONST, self.const(len(node.arguments)))

            self._compile_expr(node.function)
            self.addop(CALL, None)
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
                self.addop(operator_to_opcode[node.op], None)
            elif node.op == "->":
                self._compile_expr(node.left)
                if node.right.kind != "Name":
                    raise ValueError("Invalid node")
                idx = self.const(node.right.name)
                self.addop(LOAD_ATTR, idx)
        else:
            raise ValueError(
                f"Invalid node {node.kind} (When you get this error. Please upload an issue for UEL)"
            )

    def _compile_assign(self, node: Assign):
        if node.left.kind == "Name":
            self._compile_expr(node.right)
            self.addop(STORE_NAME, self.const(node.left.name))

    def addop(self, opcode, value):
        self.co_instructions.append(Instruction(opcode, value))

    def _compile(self, ast):
        if isinstance(ast, Assign):
            self._compile_assign(ast)
        elif isinstance(ast, Module):
            self._compile_block(ast.body)
        elif isinstance(ast, Block):
            self._compile_block(ast)
        elif isinstance(ast, IncludeFile):
            from uel.executor import UELExecutor

            exe = UELExecutor()
            self._compile(
                exe._build_ast_only(
                    exe._get_source(
                        join(dirname(self.filename), ast.filename),
                        File.FILE_ENCODING
                    )
                )
            )
        elif isinstance(ast, ImportName):
            self.addop(IMPORT_NAME, self.const(ast.name))
            self.addop(STORE_NAME, self.const(ast.name))
        elif isinstance(ast, FunctionDef):
            f = self.const(ast.name)
            args = self.const(ast.arguments)
            body = self.const(
                Compiler(self.filename, ast.body).compile()
            )
            self.addop(LOAD_CONST, args)
            self.addop(LOAD_CONST, body)
            self.addop(MAKE_FUNCTION, None)
            self.addop(STORE_NAME, f)
        elif isinstance(ast, list):
            for ast_ in ast:
                self._compile(ast_)
        else:
            self._compile_expr(ast)
            self.addop(POP_TOP, None)

    def compile(self):
        self._compile(self.ast)
        none = self.const(uel_none)
        self.addop(LOAD_CONST, none)
        self.addop(RETURN_VALUE, None)

        return UELCode(
            co_consts=self.co_consts,
            co_instructions=self.co_instructions,
        )


def uel_compiler(filename, _, ast) -> UELCode:
    compiler = Compiler(filename, ast)

    return compiler.compile()
