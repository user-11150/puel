from uel.tools import uel_exit
import unittest


class TestExit(unittest.TestCase):
    def test_exit(self):
        try:
            uel_exit()
        except:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
