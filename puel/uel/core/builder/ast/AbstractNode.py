"""
The AST node's base
"""

from typing import Callable
from typing import Union
from typing import List

class AbstractNode:
    """
    The AbstractNode(AN) is a abstract classs.
    
    AN is the all AST(abstract syntax tree) important baseclass
    """
    def __init__(self):
        raise NotImplementedError
