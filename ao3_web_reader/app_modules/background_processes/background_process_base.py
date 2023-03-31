import multiprocessing
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


class BackgroundProcessBase:
    def __init__(self, app):
        self.app = app

        self.process = multiprocessing.Process(target=self.mainloop)
        self.process_pid = None

        self.db_session = self.init_db_session()

    def get_process_name(self):
        return type(self).__name__

    def init_db_session(self):
        db_engine = sqlalchemy.create_engine(self.app.config["SQLALCHEMY_DATABASE_URI"], poolclass=NullPool)
        session = sessionmaker(bind=db_engine, expire_on_commit=False)

        return session()

    def mainloop(self):
        pass

    def set_process_data(self):
        self.app.processes_manager.set_process_data(self.get_process_name(), self.get_process_data())

    def get_process_data(self):
        return {}
