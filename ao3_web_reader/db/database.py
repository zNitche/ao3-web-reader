from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import exc
from ao3_web_reader.db import Base


class Database:
    def __init__(self):
        self.engine = None
        self.session_maker = None
        self.session = None

    def setup(self, db_uri):
        self.engine = create_engine(db_uri)
        self.session_maker = self.__create_session_maker()
        self.session = self.get_session()

    def create_all(self):
        from ao3_web_reader import models

        Base.query = self.session.query_property()
        Base.metadata.create_all(bind=self.engine)

    def __create_session_maker(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
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

    def add(self, obj):
        self.session.add(obj)
        self.commit()

    def remove(self, obj):
        self.session.delete(obj)
        self.commit()

    def commit(self):
        try:
            self.session.commit()

        except Exception as exception:
            self.session.rollback()
            raise exception
