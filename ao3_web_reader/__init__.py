from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_migrate
import flask_login
import os
from config import Config


db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def init_migrations(app):
    migrations_dir_path = app.config["MIGRATIONS_DIR_PATH"]

    migrate.init_app(app, db, directory=migrations_dir_path)

    if not os.path.exists(migrations_dir_path):
        flask_migrate.init(migrations_dir_path)

    flask_migrate.migrate(migrations_dir_path)
    flask_migrate.upgrade(migrations_dir_path)


def register_blueprints(app):
    from ao3_web_reader.blueprints.main.routes import main
    from ao3_web_reader.blueprints.errors.routes import errors
    from ao3_web_reader.blueprints.auth.routes import auth
    from ao3_web_reader.blueprints.works.routes import works

    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(auth)
    app.register_blueprint(works)


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(25)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    from ao3_web_reader import models

    @login_manager.user_loader
    def user_loader(user_id):
        return models.User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        init_migrations(app)

        register_blueprints(app)

        return app
