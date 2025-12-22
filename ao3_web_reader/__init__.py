__version__ = "2.2.0"


import os
from flask import Flask
from ao3_web_reader.modules.managers import ProcessesManager
from ao3_web_reader.modules.managers.redis_client import RedisClient
from config import Config
from ao3_web_reader.db import Database
from ao3_web_reader.authentication import AuthManager
from ao3_web_reader.logging import AppLogging


db = Database()

processes_cache = RedisClient(db_id=0)
processes_manager = ProcessesManager(cache_db=processes_cache)

auth_db = RedisClient(db_id=1)
auth_manager = AuthManager(auth_db=auth_db)


def setup_app_managers(app):
    is_debug = app.config.get("DEBUG_MODE")

    redis_address = app.config["REDIS_SERVER_ADDRESS"]
    redis_port = int(app.config["REDIS_SERVER_PORT"])

    processes_cache.setup(address=redis_address, port=redis_port)
    auth_db.setup(address=redis_address, port=redis_port,
                  flush=False if is_debug else True)
    

def setup_app_logging(app):
    app_logging = AppLogging(
        app=app,
        logs_filename="app.log",
        logs_path=app.config.get("LOGS_DIR_PATH"),
        backup_log_files_count=3)
    
    app_logging.setup()


def register_blueprints(app):
    from ao3_web_reader import blueprints

    app.register_blueprint(blueprints.core)
    app.register_blueprint(blueprints.errors)
    app.register_blueprint(blueprints.auth)
    app.register_blueprint(blueprints.works)
    app.register_blueprint(blueprints.tags)
    app.register_blueprint(blueprints.api)


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(
        25) if not config_class.DEBUG_MODE else "debug_secret"
    app.config.from_object(config_class)

    setup_app_logging(app)

    db.setup(app.config["DATABASE_URI"])
    db.create_all()

    with app.app_context():
        setup_app_managers(app)

        register_blueprints(app)

        app.logger.info("app has been created")

        return app
