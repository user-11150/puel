from uel.core.builder.bytecode.BytecodeInfo import BytecodeInfo
from uel.core.builder.bytecode.BytecodeInfo import BT_LOAD_CONST
from uel.core.builder.bytecode.BytecodeInfo import BT_STORE_NAME

def make_exports(exports):
    i = range(1, len(exports) << 1 + 1).__iter__()
    return [
            x for key, val in exports.items()
              for x in (BytecodeInfo(BT_LOAD_CONST, val, pos=next(i)),
                        BytecodeInfo(BT_STORE_NAME, key, pos=next(i)))
           ]

