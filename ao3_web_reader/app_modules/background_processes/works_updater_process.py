from ao3_web_reader.utils import works_utils, db_utils, models_utils
from ao3_web_reader.app_modules.background_processes.background_process_base import BackgroundProcessBase
from ao3_web_reader import models
from config import Config
from datetime import datetime
import time


class WorksUpdaterProcess(BackgroundProcessBase):
    def __init__(self, app):
        super().__init__(app)

    def start_process(self):
        self.process.start()
        self.process_pid = self.process.pid

    def check_if_chapter_should_be_added(self, chapter_id, work_chapters):
        work_chapters_ids = [chapter.chapter_id for chapter in work_chapters]
        check = [id for id in work_chapters_ids if id == chapter_id]

        status = False if len(check) > 0 else True

        return status

    def mainloop(self):
        while True:
            try:
                with db_utils.db_session_scope(self.db_session) as session:
                    users = session.query(models.User).all()

                    for user in users:
                        for work in user.works:
                            chapters_struct = works_utils.get_chapters_struct(work.work_id)

                            work_data = works_utils.get_work(work.work_id, chapters_struct=chapters_struct)
                            fresh_chapters = models_utils.create_chapters_models(work_data)

                            for fresh_chapter in fresh_chapters:
                                if self.check_if_chapter_should_be_added(fresh_chapter.chapter_id, work.chapters):
                                    work.chapters.append(fresh_chapter)

                                    work.last_updated = datetime.now()

                                    update_message = models_utils.create_update_message_model(work.id,
                                                                                              fresh_chapter.title)

                                    session.add(update_message)

                            time.sleep(Config.WORKS_UPDATER_JOBS_DELAY)

            except Exception as e:
                self.app.logger.error(f"[{self.get_process_name()}] - {str(e)}")

            time.sleep(Config.WORKS_UPDATER_INTERVAL)
