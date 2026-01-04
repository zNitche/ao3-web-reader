from flask import Flask
from ao3_web_reader.jinja_context import common


def setup_constext_processor(app: Flask):
    app.context_processor(
        lambda: {"get_styles_lib": common.get_styles_lib})
