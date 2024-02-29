from typing_extensions import Self
from sys import stdout
from textual.app import App


from textual.containers import Vertical
from textual.widgets import *
from textual.containers import Horizontal
from datetime import datetime

class PTS11150(App):
    def bind_address(self,ip,port):
        self.ip = ip
        self.port = port
    def compose(self):
        time = datetime.now().strftime("%B,%e. %Y %H:%M:%S %")
        yield Header()
        yield Static()
        yield Static(time,classes='center')
        yield Static("The server starting at:")
        with Horizontal(classes='center list-container'):
            yield ListView(
                ListItem(Static(f'Host:{str(self.ip)}')),
                ListItem(Static(f'Port{str(self.port)}')),
                
            )

class _LogBeforeStart:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port;
    
    
    def main(self) -> None:
        app = PTS11150(css_path='../../textual/index.css')
        app.bind_address(self.ip,self.port)
        app.run()

def logstart(ip,port) -> None:
    lbs = _LogBeforeStart(ip,port)
    lbs.main()
    