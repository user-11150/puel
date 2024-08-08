import sys
import types
import os
import textwrap
import ast
import executing

__all__ = ["install"]


def excepthook(exc_type, value, trace: types.TracebackType | None):
    def getastnode(tb):
        return executing.Source.executing(tb).node

    trace_lines: list[str] = []

    sys.stderr.write("Untracked error:\n")

    def add_trace(trace: types.TracebackType, lines):
        try:
            cofilename = trace.tb_frame.f_code.co_filename
            path = os.path.relpath(cofilename, os.path.dirname(__file__))
            if path.startswith("."):
                path = cofilename
        except Exception:
            path = cofilename

        astnode = getastnode(trace)
        if astnode is not None:
            extra = ast.unparse(astnode)
            extra = "\n" + textwrap.indent(extra, "  ")
        else:
            extra = trace.tb_frame.f_code.co_name

        lines.insert(0, f"In \"{path}\", {trace.tb_lineno}: {extra}")
        if trace.tb_next is not None:
            add_trace(trace.tb_next, lines)

    sys.stderr.write(exc_type.__name__)
    value = str(value)
    if value:
        sys.stderr.write(":")
        sys.stderr.write(value)
    sys.stderr.write("\n")
    if trace is not None:
        add_trace(trace, trace_lines)

        for idx, line in enumerate(trace_lines, start=1):
            prefix = "  "
            if idx > 10:
                overflow = len(trace_lines) - idx + 1
                sys.stderr.write(f"{prefix}... {overflow} more\n")
                break
            sys.stderr.write(textwrap.indent(str(line), prefix))
            sys.stderr.write("\n")

    sys.stderr.flush()


def install():
    sys.excepthook = excepthook
