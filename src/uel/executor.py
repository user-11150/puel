from uel import uelio

from uel.builder import uel_tokenize, UELCode
from uel.builder.pretty_print import print_tokens, print_ast
from uel.binary import uel_uel_binary_as_uel_code
from uel.builder.parser import uel_ast_parser


class UELExecutor:
    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def _run(self, code: UELCode) -> None:
        raise NotImplementedError

    def _get_source(self, filename: str, encoding: str) -> str:
        with uelio.file_open(
            filename, "rt", encoding=encoding
        ) as f:
            return f.read()

    def _get_file_content(self, filename: str) -> bytes:
        with uelio.file_open(filename, "rb") as f:
            return f.read()

    def _build(self, fn: str, source: str) -> UELCode:
        code = UELCode()

        code.co_filename = fn
        code.co_source = source

        uel_tokenize(code)

        if self.verbose:
            assert code.co_tokens is not None
            print_tokens(code.co_tokens)

        uel_ast_parser(code)

        if self.verbose:
            assert code.co_ast is not None
            print_ast(code.co_ast)
        exit()

        return code

    def run_binary(self, filename: str) -> None:
        self._run(
            uel_uel_binary_as_uel_code(
                self._get_file_content(filename)
            )
        )

    def run_source_file(
        self, filename: str, encoding: str
    ) -> None:
        self._run(
            self._build(
                filename, self._get_source(filename, encoding)
            )
        )
