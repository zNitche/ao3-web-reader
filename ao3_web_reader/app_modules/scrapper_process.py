import multiprocessing
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from datetime import datetime
from ao3_web_reader.utils import works_utils, db_utils


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
        self.is_running = True

        self.process.start()
        self.process_pid = self.process.pid

    def mainloop(self):
        work_data = works_utils.get_work(self.work_id)

        with db_utils.db_session_scope(self.db_session) as session:
            work = works_utils.create_work_model(work_data, self.owner_id)
            work.chapters = works_utils.create_chapters_models(work_data)

            session.add(work)

        self.is_running = False
