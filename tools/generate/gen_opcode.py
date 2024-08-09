from generate import task, python
import os, textwrap, ast, itertools

SCRIPT_NAME = "tools/generate/gen_opcode.py"
OPCODE_FILE = "src/uel/opcodes"
OUTPUT_FILE = "src/uel/opcodes.py"


@task(OUTPUT_FILE)
@python(SCRIPT_NAME, OPCODE_FILE, "opcodes")
def gen_opcode(dirname):
    result = ""
    with open(os.path.join(dirname, OPCODE_FILE)) as f:
        opcodes = f.read().splitlines()
    f = "def opcode_to_opname(opcode):\n"
    cases = ""
    count = itertools.count(0)
    mapping = {}
    for opcode in sorted(opcodes):
        if not opcode:
            continue
        v = next(count)
        mapping[v] = opcode
        result += f"{opcode} = {v}\n"
    f += textwrap.indent(f"return {mapping}[opcode]", "    ")
    result += f
    return result
