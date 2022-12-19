import multiprocessing
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from datetime import datetime
from ao3_web_reader import models
from ao3_web_reader.utils import works_utils


class ScrapperProcess:
    def __init__(self, owner_id, app, work_id):
        self.app = app
        self.owner_id = owner_id

        self.work_id = work_id
        self.process = multiprocessing.Process(target=self.mainloop)

        self.timestamp = str(datetime.timestamp(datetime.now()))
        self.process_pid = None
        self.is_running = False

        self.db_session = self.init_db_session()

    def init_db_session(self):
        db_engine = sqlalchemy.create_engine(self.app.config["SQLALCHEMY_DATABASE_URI"], poolclass=NullPool)
        session = sessionmaker(bind=db_engine, expire_on_commit=False)

        return session()

    def start_process(self):
        self.process.start()
        self.process_pid = self.process.pid
        self.is_running = True

    def mainloop(self):
        self.is_running = False
