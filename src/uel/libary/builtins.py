from typing import Callable
import os

from uel.libary.pymodule import UEModuleNew, pymodule_get

__all__ = ["BUILTIN_MODULES"]

generate_module_new_func = lambda name: (lambda: pymodule_get(name))


def filter_by_module(names, root):
    for name in names:
        f = os.path.join(root, name)
        if not os.path.isdir(f):
            continue
        if any(map(lambda i: "module" in i, os.listdir(f))):
            yield name


def generate_builtin_modules():
    root = os.path.dirname(__file__)
    result = {}

    for name in filter_by_module(os.listdir(root), root):
        if name == "__pycache__":
            continue
        result[name.strip("_")] = generate_module_new_func(name)
    return result


BUILTIN_MODULES: dict[str, Callable[[], UEModuleNew]] = {}

builtins = BUILTIN_MODULES
builtins |= generate_builtin_modules()
