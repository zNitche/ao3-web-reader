import os
from flask import Flask
import flask_login
from ao3_web_reader.modules.managers import ProcessesManager
from ao3_web_reader.modules.managers.redis_client import RedisClient
from config import Config
from ao3_web_reader.db import Database


db = Database()

processes_cache = RedisClient(0)
processes_manager = ProcessesManager(cache_db=processes_cache)


def setup_app_managers(app):
    processes_cache.setup(address=app.config["REDIS_SERVER_ADDRESS"], port=int(app.config["REDIS_SERVER_PORT"]))


def setup_background_processes(app):
    from ao3_web_reader.modules.background_processes import WorksUpdaterProcess

    WorksUpdaterProcess(app).start_process()


def register_blueprints(app):
    from ao3_web_reader import blueprints

    app.register_blueprint(blueprints.core)
    app.register_blueprint(blueprints.errors)
    app.register_blueprint(blueprints.auth)
    app.register_blueprint(blueprints.works)
    app.register_blueprint(blueprints.tags)
    app.register_blueprint(blueprints.api)
    app.register_blueprint(blueprints.files)


def create_app(config_class=Config, detached=False):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(25)
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

        if not app.config["TESTING"] and not detached:
            setup_background_processes(app)

        register_blueprints(app)

        return app
