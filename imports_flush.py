#pylint:disable=C0103
#pylint:disable=C0123

import os
import ast
import re
import sys
import functools
import tqdm
import multiprocessing

INIT = sys.argv[1]
DIR = sys.argv[2]

def import_translate(string):
    """
    import_translate
    """
    if match := re.fullmatch("from (.+?) import (.*)", string=string):
        imports = []
        module_name = match.group(1)
        for attr in match.group(2).split(","):
            if module_name.strip() == os.path.split(DIR)[1]:
                continue
            imports.append(f"from {module_name} import {attr.strip()}")
        return imports
    return [string]

def sort_by_length(i: str):
    """
    sort by length and reverse
    """
    res = -1 * len(i)
    return res

def cmp(x: str, y: str):
    if x.startswith("from") and y.startswith("import"):
        return -1
    elif x.startswith("import") and y.startswith("from"):
        return 1
    
    elif sort_by_length(x) > sort_by_length(y):
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
def get_imports(where):
    """
    get imports
    """
    result = []
    with multiprocessing.Pool() as pool:
        results = pool.map(
            get_imports_by_files,
            [*os.walk(where)],
            chunksize=50
        )
        for i in results:
            result.extend(i)
    sort_ed = sorted(set(result), key=functools.cmp_to_key(cmp))
    return "\n".join([*sort_ed])

def main():
    """
    main
    """
    f = open(INIT, "wt")
    f.write(get_imports(DIR))
    f.write("\n")
    f.close()

if __name__ == "__main__":
    main()
