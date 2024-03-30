# Impprt the classes
from uel.command.SystemArgument import SystemArgument

# Import the types
from typing import List
from typing import Final

class Main:
    @staticmethod
    def main(argv: List[str]) -> None:
        # The function will execute building tasks
        
        sa: SystemArgument= SystemArgument(argv)
        sa.parserCommand()
        
