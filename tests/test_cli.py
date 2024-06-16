import unittest
import contextlib
import io

from uel.cli import main
from uel.ueargparse import UEBuildBytecodesTask

from uel.testing.mixins import UELRunMixin
import unittest

class TestCLI(unittest.TestCase, UELRunMixin):
    def test_cli(self):
        with contextlib.redirect_stdout(io.StringIO()):
            main()

    def test_bytecodefile(self):
        UEBuildBytecodesTask(["data/test_bytecode/"])
