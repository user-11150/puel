import sys

error_name = sys.argv[1]
code_string = f"""class {error_name}():
    pass
"""

f = open(f"{error_name}.py", "wt")
f.write(code_string)
f.close()
