from .basetmpl import TestTmpl
from uel.tools import uel_exit
from uel.tools.pyclassestools import Singletonmode

class TestTools(TestTmpl):
    def test_exit(self):
        with self.assertRaises(SystemExit):
            uel_exit()

    def test_singletonmode(self):
        class Player(Singletonmode):
            def __init__(self, name, age):
                self.name = name
                self.age = age
        self.assertIs(Player('Andy', 20), Player('Amy', 20))
