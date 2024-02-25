from tornado.web import RequestHandler
from ..constants import STATIC_PATH

import aiofiles
import os

__all__ = [
    "Frontend"
]

class Frontend(RequestHandler):
    """
    处理请求静态资源
    """
    async def get(self):
        """
        处理请求静态资源
        """
        request_path = self.request.path[1:]
        data_path = os.path.join(STATIC_PATH,request_path or "index.html")
        try:
            async with aiofiles.open(data_path,"rb") as fp:
                data = await fp.read()
                self.set_status(200)
                self.write(data)
        except (IsADirectoryError, FileNotFoundError):
            self.set_status(404)
            self.write("404 Not Found")
