from alembic import command, config
from sqlalchemy import Engine
import os
import shutil
from config import PROJECT_ROOT


def get_config(migrations_dir: str, db_engine: Engine):
    cfg = config.Config(os.path.join(migrations_dir, "alembic.ini"))

    cfg.set_main_option("sqlalchemy.url", str(db_engine.url))
    cfg.set_main_option("script_location", migrations_dir)
    cfg.set_main_option("compare_type", "true")

    return cfg


def init_migrations(migrations_dir: str, db_engine: Engine):
    if not os.path.exists(migrations_dir):
        cfg = get_config(migrations_dir, db_engine)

        command.init(cfg, migrations_dir)

        env_template_path = os.path.join(
            PROJECT_ROOT, "io_remastered", "db", "alembic_template", "env.template.py")
        shutil.copy2(env_template_path, os.path.join(migrations_dir, "env.py"))

        command.stamp(cfg, "head", purge=True)


def migrate(migrations_dir: str, db_engine: Engine):
    alembic_config = get_config(migrations_dir, db_engine)

    with db_engine.begin() as connection:
        alembic_config.attributes["connection"] = connection

        command.revision(alembic_config, autogenerate=True)
        command.upgrade(alembic_config, "head")
