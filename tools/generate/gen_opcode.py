from generate import task, python
import os, textwrap, ast, itertools

SCRIPT_NAME = "tools/generate/gen_opcode.py"
OPCODE_FILE = "src/uel/opcodes"
OUTPUT_FILE = "src/uel/opcodes.py"

BASE_BIT = 8

def mybin(v, bit=BASE_BIT):
    if v < 2 ** bit:
        result = "0b"
        for offset in range(bit - 1, -1, -1):
            result += str(v >> offset & 1)
        assert int(v) == int(result, 2)
        return result
    else:
        try:
            return mybin(v, bit + BASE_BIT)
        except:
            return str(v)

def dict_repr(v):
    result = ""
    for k in sorted(v.keys()):
        result += f"{k}:{repr(v[k])},"
    return f"{{{result}}}"

def fn(x):
    return x

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
        result += f"{opcode}: int = {mybin(v)}\n"
    f += f"    return {dict_repr(mapping)}[opcode]\n"
    result += f
    return result
