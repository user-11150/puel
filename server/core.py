from tornado.web import Application
from server.handlers.urls import urls

from typing import Callable

# 地址
from server.constants import PORT
from server.constants import IP

# logstart
from server.no_important.logstart import logstart

def run_app() -> None:
    import asyncio
    async def _run_app() -> None:
        event = asyncio.Event()
        app = Application(urls) # type: ignore
        app.listen(PORT,address=IP)
        await event.wait()
    
    logstart(IP,PORT)
    asyncio.run(_run_app())

def main() -> None:
    run_app()
