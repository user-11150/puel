#pylint:disable=C0103
#pylint:disable=C0123

import os
import ast
import re
import sys
import functools
import importlib
import multiprocessing
import keyword
import io
import pprint

INIT = sys.argv[1]
DIR = sys.argv[2]

def import_translate(string):
    """
    import_translate
    """
    def getall(m):
        if m.__name__ not in ".":
            return []
        if hasattr(m, "__all__"):
            return m.__all__
        return []
    def from_imports():
        module_name = match.group(1)
        for attr in match.group(2).split(","):
            if module_name.strip() == os.path.split(DIR)[1]:
                continue
            yield f"from {module_name} import {attr.strip()}"
    def imports(match):
        name = match.group(1)
        try:
            module = importlib.import_module(name.strip())
            return [f"from {name} import {x}" for x in getall(module)]
        except:
            return [f"from {name} import *"]
    if match := re.fullmatch(r"from (.+?) import (.+)", string=string):
        return [*from_imports()]
    elif match := re.fullmatch(r"import ([^\s]+)\s*$", string):
        return [*imports(match), string]
    else:
        return [string]

def sort_by_length(i: str):
    """
    sort by length and reverse
    """
    res = -1 * len(i)
    return res

def cmp(x: str, y: str):
    if sort_by_length(x) > sort_by_length(y):
        return 1
    elif sort_by_length(x) < sort_by_length(y):
        return -1
    
    return 1 if x > y else -1

#def group_by(items):
#    """
#    group by
#    """
#    standard = []
#    custom = []
#    for i in items:
#        module = re.fullmatch("^from (.+?) import (.*)$", i)
#        if module is None:
#            module = re.fullmatch("^import (.*?)", i).group(1)
#        else:
#            module = module.group(1)
#        if module.startswith(os.path.split(DIR)[1]):
#            custom.append(i)
#        else:
#            standard.append(i)
#    return standard, custom
def get_imports_by_files(args):
    root, _, files = args
    result = []
    for file in filter(lambda x: x.endswith(".py") or x.endswith(".pyi"), files):
        current = os.path.join(root, file)
        with open(current, "rt") as fd:
            text_content = fd.read()
        nodes = [*filter(lambda child: type(child) is ast.Import
                                           or type(child) is ast.ImportFrom,
                         ast.parse(text_content).body)]
        for child in nodes:
            s = ast.unparse(child)
            result.extend(import_translate(s))
    return result

def weight_removal(imports):
    dic = {}
    def get_name(_import):
        def parse_alias(alias):
            if alias.asname is not None:
                return alias.asname
            return alias.name
        for node in ast.parse(_import).body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    alias = node.names[0]
                    return parse_alias(alias)
                elif isinstance(node, ast.ImportFrom):
                    return parse_alias(node.names[0])
    names = [*filter(lambda x: "." not in x, map(get_name, imports))]
    for _import in imports:
        name = get_name(_import)
        dic[name] = _import
    return dic

def flat(f):
    result = []
    for n in f:
        if type(n) is list:
            result.extend(flat(n))
        else:
            result.append(n)
    return result

def get_imports(where):
    """
    get imports
    """
    with multiprocessing.Pool() as pool:
        global results
        results = pool.map(
            get_imports_by_files,
            [*os.walk(where)],
            chunksize=50
        )
        results = flat(results)
    x = weight_removal(results)
    sort_ed = sorted(x.values(), key=functools.cmp_to_key(cmp))
    return f"__all__ = {repr(sorted([y for y in x.keys() if y != '*'], key=len, reverse=True))}\n", "\n".join([*sort_ed])

def main():
    """
    main
    """
     
    with open(INIT, "wt") as fp:
        
        f = io.StringIO()
        header, data = get_imports(DIR)
        f.write(header)
        f.write(data)
        f.write("\n")
        result = f.getvalue()
        result = ast.unparse(ast.parse(result))
        result = f"# yapf: disable\n{result}"
        fp.write(result)

if __name__ == "__main__":
    main()
