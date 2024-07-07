import os
from uel.version import __version__

__all__ = ["ENCODING", "DEBUG", "DIRNAME"]

ENCODING = "UTF-8"
DEBUG = "dev" in __version__

DIRNAME = os.path.dirname(__file__)
