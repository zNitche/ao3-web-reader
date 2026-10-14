from ao3_web_reader.db import Database, migrations
from config import Config


def main():
    db = Database()
    db.setup(Config.DATABASE_URI)

    if db.engine is None:
        raise Exception("can't create database engine, exiting...")

    migrations.init_migrations(Config.MIGRATIONS_DIR_PATH, db.engine)
    migrations.migrate(Config.MIGRATIONS_DIR_PATH, db.engine)


if __name__ == '__main__':
    main()
