from typing import TypeAlias

from uel.constants import FILE_ENCODING as ENCODING
from uel.executor import UELExecutor
from uel.internal.uelcore_internal_exceptions import throw

import argparse
import sys

Status: TypeAlias = int


def dispatch(fn):
    dispatch.dict[fn.__name__] = fn
    return fn


dispatch.dict = {"": lambda context: None}


@dispatch
def run(context):
    
    encoding = context.encoding
    filename = context.filename
    
    
    if context.b:
        UELExecutor().run_binary(filename)
        return
    
    UELExecutor().run_source_file(filename, encoding)


def make_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    subcommands = parser.add_subparsers(dest="subcommands")

    run = subcommands.add_parser("run", help="Running UEL")

    run.add_argument("filename", help="filename")
    run.add_argument("-b", help="Run UEL-Binary file", action="store_true")
    
    run.add_argument("--encoding", help="Set encoding", default=ENCODING)

    commands = {"run": run}

    for command in commands.values():
        command.add_argument(
            "--verbose", help="Show debug infos", action="store_true"
        )

    return parser


def main(args: list[str]) -> Status:
    parser = make_argparser()

    context = parser.parse_args(args[1:])

    dispatch.dict[context.subcommands or ""](context)

    return 0


def console_main():
    raise SystemExit(main(sys.argv))
