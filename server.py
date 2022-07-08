import pathlib
import asyncio

from tornado.web import Application as App
from tornado.web import RequestHandler
from tornado.options import parse_command_line

from modules import Paginator
from models import Post

BASE_URL = pathlib.Path(__file__).parent


class HomeHandler(RequestHandler):
    def get(self):
        self.render("index.html")

    def get_template_namespace(self):
        ctx = super().get_template_namespace()
        posts = Post.select()
        ctx.update({"posts": posts})
        return ctx


class Application(App):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
        ]
        settings = {
            "debug": True,
            "template_path": BASE_URL / "templates",
            "ui_modules": {
                "paginator": Paginator,
            }
        }
        super().__init__(handlers, **settings)


if __name__ == "__main__":
    parse_command_line()
    Application().listen(8000)
    io_loop = asyncio.get_event_loop()
    io_loop.run_forever()

