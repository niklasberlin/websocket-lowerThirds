import json
from pathlib import Path

from tornado import ioloop, web, websocket

ASSET_PATH = Path("./assets")

cl = []


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render(str(ASSET_PATH / "index-new.html"))


class ControlHandler(web.RequestHandler):
    def get(self):
        self.render(str(ASSET_PATH / "control.html"))


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)


class ApiHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        self.finish()
        ##id = self.get_argument("id")
        ##value = self.get_argument("value")
        lineOne = self.get_argument("l1")
        lineTwo = self.get_argument("l2")
        delay = self.get_argument("d")

        ##check for datatype and plausible values

        ##convert string to int for delay
        if isinstance(delay, str):
            delay = int(delay)

        if not (isinstance(delay, int) and delay >= 2000 and delay <= 20000):
            delay = 5000

        if not isinstance(lineOne, str):
            lineOne = ""

        if not isinstance(lineTwo, str):
            lineTwo = ""

        data = {"lineOne": lineOne, "lineTwo": lineTwo, "delay": delay}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

    @web.asynchronous
    def post(self):
        pass


app = web.Application(
    [
        (r"/", IndexHandler),
        (r"/ws", SocketHandler),
        (r"/api", ApiHandler),
        (r"/(favicon.ico)", web.StaticFileHandler, {"path": ASSET_PATH}),
        (r"/(style.css)", web.StaticFileHandler, {"path": ASSET_PATH}),
        (r"/(rest_api_example.png)", web.StaticFileHandler, {"path": ASSET_PATH}),
        (r"/(logo.png)", web.StaticFileHandler, {"path": ASSET_PATH}),
        (r"/control.html", ControlHandler),
        (r"/control", ControlHandler),
        (r"/(control.css)", web.StaticFileHandler, {"path": ASSET_PATH}),
        (r"/(control.js)", web.StaticFileHandler, {"path": ASSET_PATH}),
        (r"/(jquery.js)", web.StaticFileHandler, {"path": ASSET_PATH}),
        (r"/(PoliticsHead.otf)", web.StaticFileHandler, {"path": ASSET_PATH}),
    ]
)

if __name__ == "__main__":
    print("starting server on Port 8888")
    app.listen(8888)
    ioloop.IOLoop.instance().start()
