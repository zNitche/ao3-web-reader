from flask import current_app
from ao3_web_reader import db


@current_app.teardown_appcontext
def teardown_appcontext(exception=None):
    db.close_session(exception=exception)
