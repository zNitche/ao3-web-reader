from contextlib import contextmanager
from sqlalchemy import create_engine, Engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from ao3_web_reader.db import ModelBase


class Database:
    def __init__(self):
        self.engine: Engine | None = None
        self.session_maker: sessionmaker[Session] | None = None
        self.session: scoped_session[Session] = None  # type: ignore

    def setup(self, db_uri):
        self.engine = create_engine(db_uri)
        self.session_maker = self.__create_session_maker()
        self.session = self.get_session()

    def create_all(self):
        from ao3_web_reader import models

        if self.session is None or self.engine is None:
            raise Exception("session doesn't exist!")

        ModelBase.metadata.create_all(bind=self.engine)
        ModelBase.get_db_session = lambda: self.session


    def __create_session_maker(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        if self.session_maker is None:
            raise Exception("session_maker doesn't exist!")

        return scoped_session(self.session_maker)

    def close_session(self, exception=None):
        if self.session:
            if isinstance(exception, exc.SQLAlchemyError):
                self.session.rollback()

            self.session.remove()

    def update_instance(self, instance, update_dict):
        for key, value in update_dict.items():
            setattr(instance, key, value)

        self.commit()

    def add(self, obj, commit_on_completion=True):
        if self.session is None:
            raise Exception("session doesn't exist!")

        self.session.add(obj)

        if commit_on_completion:
            self.commit()

    def remove(self, obj, commit_on_completion=True):
        if self.session is None:
            raise Exception("session doesn't exist!")

        self.session.delete(obj)

        if commit_on_completion:
            self.commit()

    def commit(self):
        if self.session is None:
            raise Exception("session doesn't exist!")

        try:
            self.session.commit()

        except Exception as exception:
            self.session.rollback()
            raise exception

    @contextmanager
    def session_context(self):
        session = self.get_session()

        try:
            yield session

        except Exception as e:
            session.rollback()
            raise

        finally:
            session.remove()
