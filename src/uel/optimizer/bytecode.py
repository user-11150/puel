from uel.objects import parse


def bytecode_optimizer(bytecodes):
    for bytecode in bytecodes:
        try:
            value = parse(bytecode.value, None)
        except:
            pass
        else:
            bytecode.value = value
