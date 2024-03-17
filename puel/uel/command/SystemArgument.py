from typing import Sequence
from typing import List

from os import _exit as o_exit

class SystemArgument:
    argv: Sequence[str]
    source: str
    dist: str
      
    def __init__(self,argv: Sequence[str]):
        self.argv = argv[1:]
        self.source = None
        self.dist = None
        self.build_config: List[str] = []

    def parserCommand(self) -> None:
        if len(self.argv) >= 2:
            *self.build_config, self.source, self.dist = self.argv
            print('Source',self.source)
            print('Dist',self.dist)
            print()
            return
        print(f'Unknown argument: "{" ".join([*self.argv])}"')
        o_exit(1)
