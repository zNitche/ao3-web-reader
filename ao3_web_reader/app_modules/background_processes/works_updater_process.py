from ao3_web_reader.utils import works_utils, db_utils, models_utils
from ao3_web_reader.app_modules.background_processes.background_process_base import BackgroundProcessBase
from ao3_web_reader import models
from config import Config
from datetime import datetime
import time


class WorksUpdaterProcess(BackgroundProcessBase):
    def __init__(self, app, user_id):
        super().__init__(app)

        self.user_id = user_id

    def start_process(self):
        self.process.start()
        self.process_pid = self.process.pid

    def get_works_titles(self):
        with db_utils.db_session_scope(self.db_session) as session:
            works = session.query(models.Work).filter_by(owner_id=self.user_id).all()

            titles = [work.name for work in works]

        return titles

    def check_if_chapter_should_be_added(self, chapter_model, work_model):
        work_chapters_ids = [chapter.chapter_id for chapter in work_model.chapters]
        check = [id for id in work_chapters_ids if id == chapter_model.chapter_id]

        status = False if len(check) > 0 else True

        return status

    def mainloop(self):
        while True:
            try:
                for work_name in self.get_works_titles():
                    with db_utils.db_session_scope(self.db_session) as session:
                        work = session.query(models.Work).filter_by(name=work_name).first()

                        if work:
                            work_data = works_utils.get_work(work.work_id)
                            chapters = models_utils.create_chapters_models(work_data)

                            for fresh_chapter in chapters:
                                if self.check_if_chapter_should_be_added(fresh_chapter, work):
                                    work.chapters.append(fresh_chapter)

                                    work.last_updated = datetime.now()

                                    update_message = models_utils.create_update_message_model(work.name,
                                                                                              fresh_chapter.title)

                                    session.add(update_message)

            except Exception as e:
                self.app.logger.error(f"[{self.get_process_name()}] - {str(e)}")

            time.sleep(Config.WORKS_UPDATER_INTERVAL)
