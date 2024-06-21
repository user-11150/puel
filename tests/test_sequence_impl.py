import unittest

from uel.impl.sequence import *

class TestSequence(unittest.TestCase):
    def test_simple(self):
        a = Sequence()
        self.assertTrue(a.as_list() is a.as_list())
        