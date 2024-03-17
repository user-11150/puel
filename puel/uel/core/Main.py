# Impprt the classes
from uel.command.SystemArgument import SystemArgument
from uel.core.builder.Builder import Builder

# Import the types
from typing import List
from typing import Final

class Main:
    @staticmethod
    def main(argv: List[str]) -> None:
        # The function will execute building tasks
        
        sa: SystemArgument= SystemArgument(argv)
        sa.parserCommand()
        source_path: Final[str] = sa.source
        dist_path: Final[str] = sa.dist
        
        builder: Builder = Builder(*sa.build_config,source_path,dist_path)
        builder.build()
