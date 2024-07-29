import uel.io as uelio

from uel.compile import uel_tokenize, UELCode
from uel.internal.uelcore_internal_exceptions import throw
from uel.constants import *

from uel.binary import uel_uel_binary_as_uel_code, uel_uel_code_as_uel_binary

try:
    from objprint import objprint
except ImportError:
    objprint = print

class UELExecutor:
    
    def _run(self, code):
        raise NotImplementedError
    
    def _get_source(self, filename, encoding):
        with uelio.file_open(filename, "rt", encoding=encoding) as f:
            return f.read()
    
    def _get_file_content(self, filename) -> bytes:
        with uelio.file_open(filename, "rb") as f: return f.read()
    
    def _build(self, fn, source) -> UELCode:
        code = UELCode()
        
        code.co_name = fn
        code.co_source = source
        
        uel_tokenize(code)
        
        return code

    def run_binary(self, filename) -> None:
        self._run(uel_uel_binary_as_uel_code(self._get_file_content(filename)))

    def run_source_file(self, filename, encoding) -> None:
        self._run(self._build(filename, self._get_source(filename, encoding)))
        
