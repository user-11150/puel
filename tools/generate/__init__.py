import importlib
import os
import multiprocessing
import functools
import time

_tasks = []

class task:
    def __init__(self, output):
        self.output = output
    
    def __call__(self, fn):
        @functools.wraps(fn)
        def inner(dirname):
            print(f"Generate {self.output}")
            with open(os.path.join(dirname, self.output), "wb") as fp:
                fp.write(fn(dirname))
        _tasks.append(inner)

def run(fn):
    def wrapper(target):
        @functools.wraps(target)
        def inner(*args, **kwargs):
            return fn(target(*args, **kwargs), target)
        return inner
    return wrapper

python = run(lambda s, f: f"# -*- coding: utf-8 -*-\n# Generate in {time.strftime('%x')}\n" + s)
encode = run(lambda s, f: s.encode("utf-8"))


def main(dirname):
    
    for name in filter(lambda s: s.startswith("gen") and s.endswith(".py"), os.listdir(os.path.dirname(__file__))):
        importlib.import_module("generate." + name.split(".")[0])
    
    [*map(lambda f: f(dirname), _tasks)]
