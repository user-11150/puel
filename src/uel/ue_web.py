import os.path
import atexit
from http.server import BaseHTTPRequestHandler, HTTPServer
from uel.colors import RED, RESET
from uel.Constants import DIRNAME

dev = False
dirname = DIRNAME

if dev:
    dirname = "./src/uel"

static = os.path.join(dirname, "web")


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        filename = self.path[1:]
        if filename == "" or os.path.isdir(filename):
            filename = os.path.join(filename, "index.html")
        filename = os.path.join(static, filename)
        if not os.path.exists(filename):
            filename = os.path.join(static, "index.html")
        with open(filename, "rb") as f:
            data = f.read()
            size = len(data)
            self.send_response(200)
            self.send_header("Cache-Control", "max-age=0")
            self.send_header("Content-Length", str(size))
            self.end_headers()
            self.wfile.write(data)


def start(address: tuple[str, int]) -> None:
    ip, port = address
    print(
        f"Please open http://{ip if ip != '0.0.0.0' else '127.0.0.1'}:{port}/")
    server = HTTPServer((ip, int(port)), Handler)
    try:
        server.serve_forever()
    finally:
        print(f"{RED}The server is closed{RESET}")
        exit()
