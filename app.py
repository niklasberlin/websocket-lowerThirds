import json
from pathlib import Path
from typing import Mapping

import data
import models
import requests
from config import ASSET_PATH, DATA_DIR
from pydantic import parse_raw_as
from schedule_import import update_from_schedule
from tornado import ioloop, web, websocket

DATA_DIR.mkdir(exist_ok=True)

cl = []


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render(str(ASSET_PATH / "index-new.html"))


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
        lineOne = self.get_argument("first_line")
        lineTwo = self.get_argument("second_line")
        delay = self.get_argument("delay")

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


class StorageApiHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        storage = data.load_data()
        self.write(storage.json())
        self.finish()

    @web.asynchronous
    def post(self):
        storage = models.Storage.parse_raw(self.request.body.decode())
        data.save_data(storage)
        self.finish()

    @web.asynchronous
    def delete(self):
        data.reset()
        self.finish()

class ScheduleApiHandler(web.RequestHandler):
    @web.asynchronous
    def post(self):
        storage = data.load_data()
        storage = update_from_schedule(storage)
        data.save_data(storage)
        self.finish()



app = web.Application(
    [
        (r"/", IndexHandler),
        (r"/ws", SocketHandler),
        (r"/api", ApiHandler),
        (r"/api/storage", StorageApiHandler),
        (r"/api/import_schedule", ScheduleApiHandler),
        (r"/(favicon.ico)", web.StaticFileHandler, {"path": ASSET_PATH}),
        (r"/(control-vue.html)", web.StaticFileHandler, {"path": ASSET_PATH}),
    ],
    static_path=ASSET_PATH.resolve(),
    autoreload=True,
)
if __name__ == "__main__":
    print("starting server on Port 8888")
    app.listen(8888)
    ioloop.IOLoop.instance().start()
