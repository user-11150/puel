import constextlib

from uel.ueargparse import _UERunTaskDesc

class UELRunMixin:
    def do_uel_test(self, code, rr, fn="<test-case>"):
        stdout = io.StringIO()
        
        with contextlib.redirect_stdout(stdout):
            _UERunTaskDesc.run_uel(None, fn, code, False)
        self.assertEqual(str(rr), stdout.getvalue())
    
