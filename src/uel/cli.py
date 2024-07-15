import argparse
import typing as t

from uel.uelimpl import SOURCE_MODE, uel_run

def uel_main() -> None:
    
    parser = argparse.ArgumentParser()

    subcommands = parser.add_subparsers(dest="subcommands")

    commands: dict[str, argparse.ArgumentParser] = {
        "run": subcommands.add_parser(
            "run",
            help="Run uel codes"
        )
    }

    commands["run"].add_argument("filename")
    commands["run"].add_argument("--mode", default=SOURCE_MODE, type=int)
    commands["run"].add_argument("--encoding", default="UTF-8")

    for command in commands.values():
        command.add_argument("--verbose", help="Show debug infos", action="store_true")

    context = parser.parse_args()

    dispatch: dict[str, t.Callable[[argparse.Namespace], None]] = {
        "run": uel_run,
        "": lambda x: None
    }

    dispatch[context.subcommands or ""](context)
