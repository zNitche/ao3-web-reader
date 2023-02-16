from config import Config
import sqlalchemy
import sqlalchemy.orm


def init_db_session(db_path=None):
    db_path = Config.SQLALCHEMY_DATABASE_URI if db_path is None else f"sqlite:////{db_path}"
    engine = sqlalchemy.create_engine(db_path)

    return sqlalchemy.orm.sessionmaker(engine)
