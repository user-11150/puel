import sys
import os

os.chdir(os.path.dirname(__file__))

assert sys.version_info >= (3,8),TypeError('Python版本过低')

from server.core import main
from server.version import getVersion

__version__: str = getVersion(__file__)

if __name__ == "__main__":
    main()
