from uel.ueargparse import UEBuildBytecodesTask
from uel.ueargparse import UERunBytecodesTask

import unittest
import os

class TestBytecodeFile(unittest.TestCase,
                       ):
    def test_bytecodefile(self):
        
        UEBuildBytecodesTask([
            os.path.join(os.path.dirname(__file__), "data/test_bytecodes/main.uel"),
            os.path.join(os.path.dirname(__file__), "data/test_bytecodes/main")]).run()
        UERunBytecodesTask([
            os.path.join(os.path.dirname(__file__), "data/test_bytecodes/main")
        ]).run()
