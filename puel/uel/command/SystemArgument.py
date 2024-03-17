from typing import Sequence

class SystemArgument:
    argv: Sequence[str]
    source: str
    dist: str
      
    def __init__(self,argv: Sequence[str]):
        self.argv = argv[1:]
        self.source = None
        self.dist = None
        self.build_config = []

    def parserCommand(self) -> None:
        if len(self.argv) >= 2:
            *self.build_config, self.source, self.dist = self.argv
        print(f'Unknown argument: "{" ".join([*self.argv])}"')