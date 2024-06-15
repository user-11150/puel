import unittest
import contextlib
import io

from uel.cli import main

class TestCLI(unittest.TestCase):
    def test_cli(self):
        with contextlib.redirect_stdout(io.StringIO()):
            main()
