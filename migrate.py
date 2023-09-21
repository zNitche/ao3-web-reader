import flask_migrate
import os
from ao3_web_reader import create_app
from ao3_web_reader import db, migrate


def main():
    app = create_app(detached=True)

    migrations_dir_path = app.config["MIGRATIONS_DIR_PATH"]

    with app.app_context():
        migrate.init_app(app, db, directory=migrations_dir_path)

        if not os.path.exists(migrations_dir_path):
            flask_migrate.init(migrations_dir_path)

        flask_migrate.migrate(migrations_dir_path)
        flask_migrate.upgrade(migrations_dir_path)


if __name__ == '__main__':
    main()
