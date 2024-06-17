import contextlib
import math
import unittest

from uel.omit.testing.mixins import UELRunMixin

class TestRun(unittest.TestCase, UELRunMixin):
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
        self.do_uel_test("""import "data/test_module/a.uel"
""", "1", __file__)

    def test_if_statement(self):
        self.do_uel_test("if 1 put 5 end", 5)
