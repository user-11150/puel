#pylint:disable=W0221
"""
The argparse and exec for UEL
"""

import sys
import os

from .colors import RESET, YELLOW, GREEN, RED

from .pyexceptions.CustomError import CustomError
from uel.core.runner.ExecuteContext import ExecuteContext
from uel.core.runner.importlib import _read_string_from_file

HELP = ("help", "--help")
VERSION = ("version", "-V")
RUN = ("run",)
REPL = ("repl", )

try:
    TERCOL = os.get_terminal_size().columns
except OSError:
    TERCOL = 80

class UEArgParser:
    def __init__(self, args):
        self.tsk = None
        self.args = args
        self.current = None
        self.idx = -1
        self.advance()
        self.parser()

    def advance(self):
        try:
            self.idx += 1
            self.current = self.args[self.idx]
        except IndexError:
            self.current = None

    @property
    def rest(self):
        return self.args[self.idx + 1:]

    def parser(self):
        if self.current in HELP:
            self.tsk = UEHelpTaskDesc(self.rest)
        elif self.current in VERSION:
            self.tsk = UEVersionTaskDesc(self.rest)
        elif self.current in RUN:
            self.tsk = UERun(self.rest)
        else:
            print(f"{YELLOW}[WARNNING] Unknown argument, print help{RESET}")

class UETaskDesc:
    def __init__(self, rest=None):
        if rest is None:
            rest = []
        self.rest = rest

class UEHelpTaskDesc(UETaskDesc):
    ONLY_COMMAND_HELP = {
        RUN: "Run UEL code",
        HELP: "Show help. use of 'python -m uel help' or show help of given command eg: 'python -m help run'",
        VERSION: "Show python version",
        REPL: "Looks like python REPL(future feature)"
    }
    EMPTY = []
    s = ""
    col = max(*map(lambda x: len(", ".join(x[0])), ONLY_COMMAND_HELP.items()))
    for ks, v in sorted(ONLY_COMMAND_HELP.items(), key=lambda x: (y := bytes(",".join(x[0]), "utf-8"), int.from_bytes(y) if not y.count(b"-") else 0)[1]):
        i = ", ".join(sorted(ks))
        s += i.ljust(col)
        s += ":"
        if v.count("\n") > 1:
            s += "\n    "
            for n in v.splitlines():
                s += n
                s += "\n    "
        else:
            s += " "
            s += v
        s += "\n  "
    s += "\n"
    DEFAULT_HELP = f"""This is UEL programming language help. by LiXingHao

Usage: python -m uel [arguments]
  {s}

"""
    del col, s
    def run(self):
        
        if self.rest == self.EMPTY:
            text = self.DEFAULT_HELP
        elif len(self.rest) == 1:
            d = self.ONLY_COMMAND_HELP
            d2 = {}
            for ks, v in d.items():
                for k in ks:
                    d2[k] = v
            text = d2[self.rest[0]]
        print(text)

class UEVersionTaskDesc(UETaskDesc):
    def run(self):
        assert len(self.rest) == 0
        print(sys.version)

class _Private:
    """
    不对外直接公开的，但是可以间接使用的
    """

class _UERunTaskDesc(_Private):
    def run(self, fn, string):
        ectx = ExecuteContext()
        ectx.run_code_from_basic(fn, string)

class UERun(UETaskDesc, _UERunTaskDesc):
    def run(self):
        if len(self.rest) != 1:
            print(f"{RED}ERROR!!!: Run takes only one argument, <filename>, but is given {len(self.rest)}{RESET}")
            return
        filename = self.rest[0]
        
        string = _read_string_from_file(filename)
        super().run(filename, string)

class UETask:
    def __init__(self, parser):
        self.parser = parser
        self.tsk = parser.tsk

    def run(self):
        if hasattr(self.tsk, "run"):
            tsk = self.tsk
        else:
            tsk = UEHelpTaskDesc()
        tsk.run()