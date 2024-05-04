import sys

def throw(e):
    sys.stderr.write(str(e))
    raise SystemExit