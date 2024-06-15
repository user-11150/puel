from uel.ueargparse import _UERunTaskDesc

import unittest
import unittest.mock
import contextlib
import math
import io
import os

class TestRun(unittest.TestCase):
    def do_uel_test(self, code, rr, fn="<test-case>"):
        stdout = io.StringIO()
        
        with contextlib.redirect_stdout(stdout):
            _UERunTaskDesc.run_uel(None, fn, code, False)
        self.assertEqual(rr, stdout.getvalue())
    
    def test_run(self):
        self.do_uel_test("put 5", "5")

    def test_import(self):
        self.do_uel_test("""import "math"
push 1
call sin
put TOP
""", str(math.sin(1)))

    def test_function(self):
        self.do_uel_test("""function a;
  put 5
end

call a
""", str(5))
        self.do_uel_test("""
function a b;
    function c;
        put b
    end
    call c
end
push 1
call a
""", str(1))

    def test_calculator(self):
        self.do_uel_test("""put 1 + 2 * 2""", str(6))
        self.do_uel_test("""a = 2\nb=3\nput a + b""", str(5))

    def test_import2(self):
        self.do_uel_test("""import "data/a.uel"
""", "1", __file__)
