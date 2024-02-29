from tornado.web import Application
from server.handlers.urls import urls

from typing import Callable

# 地址
from server.constants import PORT
from server.constants import IP

# logstart
from server.no_important.logstart import logstart

# Feb.29[User-11150]: <优化> 虽然总的时间没有变化，甚至还可能增加
#     但是，在函数内部导入可以使 “loading...” 提示语尽早出现，用户
#     体验相对更好
def run_app() -> None:
    import asyncio
    async def _run_app():
        event = asyncio.Event()
        app = Application(urls) # type: ignore
        app.listen(PORT,address=IP)
        await event.wait()
    
    def chilren_process_execute_async_task(fn: Callable[[],asyncio.Condition]) -> None:
        import multiprocessing
        def _wrapped_task():
            asyncio.set_event_loop(asyncio.new_event_loop())
            asyncio.run(fn())
        process = multiprocessing.Process(target=_wrapped_task)
        process.start()
    chilren_process_execute_async_task(_run_app)
    logstart(IP,PORT)

def main() -> None:
    print('Loading...')
    run_app()
