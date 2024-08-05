from uel import uelio

from uel.builder import uel_tokenize, UELCode
from uel.internal.uelcore_internal_exceptions import throw
from uel.constants import *
from uel.builder.pretty_print import print_tokens
from uel.binary import uel_uel_binary_as_uel_code, uel_uel_code_as_uel_binary


class UELExecutor:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def _run(self, code):
        raise NotImplementedError

    def _get_source(self, filename, encoding):
        with uelio.file_open(filename, "rt", encoding=encoding) as f:
            return f.read()

    def _get_file_content(self, filename) -> bytes:
        with uelio.file_open(filename, "rb") as f:
            return f.read()

    def _build(self, fn, source) -> UELCode:
        code = UELCode()

        code.co_filename = fn
        code.co_source = source

        uel_tokenize(code)

        if self.verbose:
            print_tokens(code.co_tokens)

        return code

    def run_binary(self, filename: str) -> None:
        self._run(
            uel_uel_binary_as_uel_code(self._get_file_content(filename))
        )

    def run_source_file(self, filename: str, encoding: str) -> None:
        self._run(
            self._build(filename, self._get_source(filename, encoding))
        )
