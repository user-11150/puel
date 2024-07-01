# pylint:disable=W0221
"""
The argparse and exec for UEL
"""

import os
import sys
import importlib

from sys import path

from uel.runner.executecontext import ExecuteContext
from uel.runner.importlib import _read_string_from_file
from uel.ue_web import start as _ue_web_start

from uel.colors import GREEN, RED, RESET, YELLOW
from uel.constants import DEBUG
from uel.pyexceptions.customerror import CustomError

from uel.bytecodefile.compress import compress, decompress

HELP = ("help", "--help")
VERSION = ("version", "-V")
RUN = ("run", )
REPL = ("repl", )
WEB = ("web", )
BUILD_BYTECODE = ("binary", )
RUN_BYTECODE = ("run-binary", "run_binary")

try:
    TERCOL = os.get_terminal_size().columns
except OSError:
    TERCOL = 80


class UEArgParser:
    def __init__(self, args: list[str]):
        self.tsk: UETaskDesc | None = None
        self.args: list[str] = args
        self.current: str | None = None
        self.idx: int = -1
        self.advance()
        self.parser()

    def advance(self) -> None:
        try:
            self.idx += 1
            self.current = self.args[self.idx]
        except IndexError:
            self.current = None

    @property
    def rest(self) -> list[str]:
        return self.args[self.idx + 1:]

    def parser(self) -> None:  # pragma: no cover
        if self.current in HELP:
            self.tsk = UEHelpTaskDesc(self.rest)
        elif self.current in VERSION:
            self.tsk = UEVersionTaskDesc(self.rest)
        elif self.current in RUN:
            self.tsk = UERun(self.rest)
        elif self.current in REPL:
            self.tsk = UERepl(self.rest)
        elif self.current in WEB:
            self.tsk = UEWebTask(self.rest)
        elif self.current in BUILD_BYTECODE:
            self.tsk = UEBuildBytecodesTask(self.rest)
        elif self.current in RUN_BYTECODE:
            self.tsk = UERunBytecodesTask(self.rest)
        else:
            print(
                f"{YELLOW}[WARNNING] Unknown argument, print help{RESET}"
            )

class UETaskDesc:
    def __init__(self, rest: list[str] | None = None) -> None:
        if rest is None:
            rest = []
        self.rest: list[str] = rest


class UEHelpTaskDesc(UETaskDesc):
    ONLY_COMMAND_HELP = {
        RUN:
            "Run UEL code",
        HELP:
            "Show help. use of 'python -m uel help' or show help of given command eg: 'python -m help run'",
        VERSION:
            "Show python version",
        REPL:
            "Looks like python REPL",
        WEB:
            "The web for UEL, usage: 'python -m uel [<ip> [<port>]]'",
        BUILD_BYTECODE:
            "Build the bytecodes, (WARN: If you used Python extension, nerver use this)",
        RUN_BYTECODE:
            "Run the bytecodes, (WARN: If you used Python extension, nerver use this)"
    }
    EMPTY: list[str] = []
    s = ""
    col = max(
        *map(lambda x: len(", ".join(x[0])), ONLY_COMMAND_HELP.items())
    )
    for ks, v in sorted(
        ONLY_COMMAND_HELP.items(),
        key=lambda x: (
            y := bytes(",".join(x[0]), "utf-8"), int.from_bytes(y)
            if not y.count(b"-") else 0
        )[1]
    ):
        i = ", ".join(sorted(ks))
        s += i.ljust(col + 1)
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
        s += RESET
    s += "\n"
    DEFAULT_HELP = f"""This is UEL programming language help. by LiXingHao

Usage: python -m uel [arguments]
  {s}
"""
    del col, s

    def run(self) -> None:

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
    def run(self) -> None:
        assert len(self.rest) == 0
        print(sys.version)


class UEWebTask(UETaskDesc):
    def run(self) -> None:
        if not (0 <= len(self.rest) and len(self.rest) <= 2):
            print(
                f"Unkown argument: '{self.rest}'\n"
                "Usage: python -m uel [<ip> [<port>]]"
            )
            exit()
        default_address = ("0.0.0.0", 2521)
        address = default_address
        if len(self.rest) == 1:
            address = (self.rest[0], default_address[1])
        elif len(self.rest) == 2:
            address = self.rest  # type: ignore
        _ue_web_start(address)


class _Private:
    pass


class _UERunTaskDesc(_Private):
    def run_uel(self, fn: str, string: str, debug=DEBUG) -> None:
        ectx = ExecuteContext()
        ectx.run_code_from_basic(fn, string, debug)


class UEBuildBytecodesTask(UETaskDesc):
    def run(self):
        class BuildFail(Exception):
            pass

        assert len(self.rest) == 2

        filename = self.rest[0]
        save = self.rest[1]
        string = _read_string_from_file(filename)
        debug = DEBUG

        ectx = ExecuteContext()
        bytecodes = ectx.build_bytecodes(
            fn=filename, code=string, debug=debug
        )
        with open(save, "wb") as fp:
            try:
                compressd = compress(bytecodes)

                decompress(compressd)
            except Exception as e:
                raise BuildFail(
                    "Build Fail: (Maybe you used Python extension UEL.)"
                ) from e
            fp.write(compressd)


class UERunBytecodesTask(UETaskDesc):
    def run(self):
        assert len(self.rest) == 1

        filename = self.rest[0]

        ectx = ExecuteContext()

        ectx.run_bytecodes(decompress(open(filename, "rb").read()))


class UERepl(UETaskDesc, _UERunTaskDesc):
    def run(self) -> None:
        UEVersionTaskDesc().run()
        print("Use '.exit' quit")
        while True:
            try:
                print(">>>", end="", flush=True)
                string_of_code = sys.stdin.readline()[:-1]
                if string_of_code == ".exit":
                    print("EXIT")
                    break
                self.run_uel("<string>", string_of_code)
            except KeyboardInterrupt:
                print(f"{RED}KeyboardInterrupt{RESET}")


class UERun(UETaskDesc, _UERunTaskDesc):
    def run(self) -> None:
        if len(self.rest) != 1:
            print(
                f"{RED}ERROR!!!: Run takes only one argument, <filename>, but is given {len(self.rest)}{RESET}"
            )
            return
        filename = self.rest[0]

        string = _read_string_from_file(filename)
        self.run_uel(filename, string)


class UETask:
    def __init__(self, parser: UEArgParser) -> None:
        self.parser = parser
        self.tsk = parser.tsk

    def run(self) -> None:
        if hasattr(self.tsk, "run"):
            tsk = self.tsk
        else:
            tsk = UEHelpTaskDesc()
        if tsk is not None:
            tsk.run()
        else:
            print("NONE")
