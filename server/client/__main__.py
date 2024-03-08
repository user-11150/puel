#!/usr/bin/env python

"""
  当服务端启动时，可以通过
    python -m client
"""

import webbrowser
import sys
import socket
import os

__version__ = None

os.chdir(os.path.dirname(os.path.dirname(__file__)))

sys.path.append("./")

import server.constants

ADDR = server.constants.IP,server.constants.PORT

def try_connection() -> bool:
    try:
        conn = socket.socket()
        conn.connect(ADDR)
    except: # pylint: disable=W
        return False
    return True

def main() -> None:
    print("http://"+ADDR[0]+":"+str(ADDR[1])+'/')
    webbrowser.open("http://"+ADDR[0]+":"+str(ADDR[1])+'/')

if __name__ == "__main__":
    main()
