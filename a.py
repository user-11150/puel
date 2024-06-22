from uel.libary.helpers import make_exports

import sys

bytecodes = make_exports({
    "a": lambda x, y: print("Da Sa bi")
})
