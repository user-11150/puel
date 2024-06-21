import os
import re

def main():
    for root, _, files in [*os.walk("./src"), *os.walk("./tests/")]:
        for file in filter(lambda x: x.endswith(".py"), files):
            #with open(os.path.join(root, file), "rt") as f:
#                text = f.read()
#            with open(os.path.join(root, file), "wt") as f:
#                f.write(text.replace("core.", ""))
             with open(os.path.join(root, file)) as f:
                 text = f.read()
             os.remove(os.path.join(root, file))
             with open(os.path.join(root, file).lower(), "wt") as f:
                 f.write(
                     re.sub(
                         "from (.*?) import (.*?)",
                         lambda match: f"from {match.group(1).lower()} import {match.group(2)}",
                         text)
                 )

main()
