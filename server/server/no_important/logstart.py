from typing_extensions import Self
from typing import Callable
from typing import TypeVar
from typing import Any
from functools import wraps
from datetime import datetime

import traceback

T = TypeVar("T")

def chain(fn: Callable[[T],Any]) -> Callable[...,T]:
    @wraps(fn)
    def inject(self: T,*args: Any,**kwargs: Any) -> T:
        fn(self,*args,**kwargs)
        return self
    return inject
        
def center(text: str) -> str:
    import os
    try:
        terminal_size = os.get_terminal_size().columns
        return text.center(terminal_size)
    except (OSError):
        exe = traceback.format_exc()
        print(exe)
        print("（可忽略）")
        return text

class _LogBeforeStart:
    def __init__(self: Self,ip: str,port: int) -> None:
        self.ip = ip
        self.port = port
        self.time = datetime.now()
    
    
    
    def main(self) -> None:
        app = self
        (app.print_package_name()
            .print_time()
            .print_line()
            .print_address_info()
            .print_line()
            .print_version())
     
    @chain
    def print_package_name(self) -> None:
        print(center('PTS11150'))
    
    @chain
    def print_time(self) -> None:
        
        print(
          center(self.time.strftime('%B,%d. %Y %H:%M:%S %p %A'))
        )
    @chain
    def print_line(self) -> None:
        print()
    @chain
    def print_address_info(self) -> None:
        
        print('You can open:')
        def independence(IP: str,PORT: int) -> None:
           
            before = "\t"
            print(f'{before}IP: {IP}')
            print(f'{before}PORT:{PORT}')
            print()
            print(f'{before}URL: http://{IP}:{PORT}/')
        independence(self.ip,self.port)
        if self.ip == "0.0.0.0":
            print("  Or open:")
            independence("127.0.0.1",self.port)
        
    @chain
    def print_version(self) -> None:
        print('Python version',__import__("sys").version.splitlines()[0])
        print('Tornado version:',__import__("tornado").version)
        print("Server version:",__import__("__main__").__version__)
    
        
def logstart(ip: str,port: int) -> None:
    lbs = _LogBeforeStart(ip,port)
    lbs.main()
    