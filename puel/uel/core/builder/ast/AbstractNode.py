"""
The AST node's base
"""

class AbstractNode:
    """
    The AbstractNode(AN) is a abstract classs.
    
    AN is the all AST(abstract syntax tree) important baseclass
    """

    # The methods is required.
    # It's always call
    def __repr__(self):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError
