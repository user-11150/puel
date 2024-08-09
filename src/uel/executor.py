from uel import uelio

from uel.builder import uel_generate_tokens, UELCode
from uel.builder.pretty_print import print_tokens, print_ast, print_code
from uel.binary import uel_uel_binary_as_uel_code
from uel.builder.parser import uel_ast_parser
from uel.builder.compiler import uel_compiler


class UELExecutor:
    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def _run(self, code: UELCode) -> None:
        raise NotImplementedError

    def _get_source(self, filename: str, encoding: str) -> str:
        with uelio.file_open(filename, "rt", encoding=encoding) as f:
            return f.read()

    def _get_file_content(self, filename: str) -> bytes:
        with uelio.file_open(filename, "rb") as f:
            return f.read()

    def _build(self, fn: str, source: str) -> UELCode:
        tokens = uel_generate_tokens(source)

        if self.verbose:
            print_tokens(tokens)

        ast = uel_ast_parser(source, tokens)

        if self.verbose:
            print_ast(ast)

        code = uel_compiler(fn, source, ast)

        print_code(code)

        return code

    def run_binary(self, filename: str) -> None:
        self._run(
            uel_uel_binary_as_uel_code(self._get_file_content(filename))
        )

    def run_source_file(self, filename: str, encoding: str) -> None:
        self._run(
            self._build(filename, self._get_source(filename, encoding))
        )
