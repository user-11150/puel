from typing import Sequence
from typing import List
from os import _exit as o_exit

import typing as t

#class SystemArgument:
#    argv: Sequence[str]
#    source: str
#    dist: str
#      
#    def __init__(self,argv: Sequence[str]):
#        self.argv = argv[1:]
#        self.source = None
#        self.dist = None
#        self.build_config: List[str] = []

#    def parserCommand(self) -> None:
#        if len(self.argv) >= 2:
#            *self.build_config, self.source, self.dist = self.argv
#            print('Source',self.source)
#            print('Dist',self.dist)
#            print()
#            return
#        print(f'Unknown argument: "{" ".join([*self.argv])}"')
#        o_exit(1)

class SystemArgument:
    def __init__(self, argv: List[str]):
        self.argv = argv[1:]

        self.source_file:  t.Optional[str] = None
        self.rest: t.Optional[t.List[str]] = None

    def parserCommand(self) -> None:
        if len(self.argv) < 1:
            print("Usage:\n"
                  "\tpython -m main <source-file>"
                  "")
        elif len(self.argv) >= 1:
            [self.source_file, *self.rest] = self.argv
        
#        # 测试
#        print("Source file:",self.source_file)
