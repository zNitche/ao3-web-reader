from flask import current_app
from ao3_web_reader import db

from ao3_web_reader.blueprints.auth.routes import auth
from ao3_web_reader.blueprints.errors.routes import errors
from ao3_web_reader.blueprints.api.routes import api
from ao3_web_reader.blueprints.works.routes import works
from ao3_web_reader.blueprints.tags.routes import tags
from ao3_web_reader.blueprints.core.routes import core
from ao3_web_reader.blueprints.files.routes import files


@current_app.teardown_appcontext
def teardown_appcontext(exception=None):
    db.close_session(exception=exception)
