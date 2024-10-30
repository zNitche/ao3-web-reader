import os
from flask import Flask
import flask_login
from ao3_web_reader.modules.managers import ProcessesManager
from ao3_web_reader.modules.managers.redis_client import RedisClient
from config import Config
from ao3_web_reader.db import Database


db = Database()

processes_cache = RedisClient(db_id=0)
processes_manager = ProcessesManager(cache_db=processes_cache)


def setup_app_managers(app):
    redis_address = app.config["REDIS_SERVER_ADDRESS"]
    redis_port = int(app.config["REDIS_SERVER_PORT"])

    processes_cache.setup(address=redis_address, port=redis_port)


def register_blueprints(app):
    from ao3_web_reader import blueprints

    app.register_blueprint(blueprints.core)
    app.register_blueprint(blueprints.errors)
    app.register_blueprint(blueprints.auth)
    app.register_blueprint(blueprints.works)
    app.register_blueprint(blueprints.tags)
    app.register_blueprint(blueprints.api)
    app.register_blueprint(blueprints.files)


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(25) if not config_class.DEBUG_MODE else "debug_secret"
    app.config.from_object(config_class)

    db.setup(app.config["DATABASE_URI"])
    db.create_all()

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    from ao3_web_reader import models

    @login_manager.user_loader
    def user_loader(user_id):
        return db.session.query(models.User).filter_by(id=user_id).first()

    with app.app_context():
        setup_app_managers(app)

        register_blueprints(app)

        return app
