from tornado.web import Application
from .handlers.urls import urls
from .constants import PORT

import asyncio

async def run_app():
    event = asyncio.Event()
    app = Application(urls)
    app.listen(PORT)
    await event.wait()

def main():
    asyncio.run(run_app())
