from tornado.web import Application
from .handlers.urls import urls
from .constants import PORT

import asyncio

async def run_app() -> None:
    event = asyncio.Event()
    app = Application(urls) # type: ignore
    app.listen(PORT)
    await event.wait()

def main() -> None:
    asyncio.run(run_app())
