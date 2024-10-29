import os
from flask import Flask
import flask_login
from config import Config
from ao3_web_reader.db import Database


db = Database()


def setup_app_managers(app):
    from ao3_web_reader.app_modules.managers.redis_manager import RedisManager
    from ao3_web_reader.app_modules.managers.processes_manager import ProcessesManager

    managers = [RedisManager(app, 0), ProcessesManager(app)]

    for manager in managers:
        manager.setup()

        setattr(app, manager.get_name(), manager)


def setup_background_processes(app):
    from ao3_web_reader.utils import processes_utils

    processes_utils.start_work_updater_processes(app)


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
