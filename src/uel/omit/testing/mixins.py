import contextlib
import io

from uel.ueargparse import _UERunTaskDesc

__all__ = ["UELRunMixin"]


class UELRunMixin:
    def do_uel_test(self, code, rr, fn="<test-case>"):
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            _UERunTaskDesc.run_uel(None, fn, code, False)
        self.assertEqual(str(rr), stdout.getvalue())
