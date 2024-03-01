import sys

assert sys.version_info >= (3,8),TypeError('Python版本过低')

from server.core import main

__version__ = "0.2.3"

if __name__ == "__main__":
    main()
