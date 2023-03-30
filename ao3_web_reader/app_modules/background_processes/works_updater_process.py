from ao3_web_reader.utils import works_utils, db_utils, models_utils
from ao3_web_reader.app_modules.background_processes.background_process_base import BackgroundProcessBase
from ao3_web_reader import models
from ao3_web_reader.consts import UpdateMessagesConsts
from config import Config
from datetime import datetime
import time


class WorksUpdaterProcess(BackgroundProcessBase):
    def __init__(self, app):
        super().__init__(app)

    def start_process(self):
        self.process.start()
        self.process_pid = self.process.pid

    def check_if_new_chapter(self, chapter_id, work_chapters):
        status = False if chapter_id in [chapter.chapter_id for chapter in work_chapters] else True

        return status

    def get_chapter_by_id(self, chapters, chapter_id):
        result_chapter = None

        for chapter in chapters:
            if chapter.chapter_id == chapter_id:
                result_chapter = chapter
                break

        return result_chapter

    def check_chapters_for_removed_ones(self, fresh_chapters, work, session):
        work_chapters_ids = [chapter.chapter_id for chapter in work.chapters if not chapter.was_removed]
        fresh_chapters_ids = [chapter.chapter_id for chapter in fresh_chapters if not chapter.was_removed]

        removed_chapters_ids = list(set(work_chapters_ids).difference(fresh_chapters_ids))

        for chapter_id in removed_chapters_ids:
            chapter = self.get_chapter_by_id(work.chapters, chapter_id)

            if chapter:
                self.mark_chapter_as_removed(work, chapter, session)

    def update_works(self, works):
        for work in works:
            if not works_utils.check_if_work_exists(work.work_id):
                work.was_removed = True

            time.sleep(Config.WORKS_UPDATER_JOBS_DELAY)

    def add_chapter(self, work, chapter, session):
        work.chapters.append(chapter)
        work.last_updated = datetime.now()

        update_message = models_utils.create_update_message_model(work.id,
                                                                  chapter.title,
                                                                  UpdateMessagesConsts.MESSAGE_ADDED_TYPE)

        session.add(update_message)

    def mark_chapter_as_removed(self, work, chapter, session):
        chapter.was_removed = True
        work.last_updated = datetime.now()

        update_message = models_utils.create_update_message_model(work.id,
                                                                  chapter.title,
                                                                  UpdateMessagesConsts.MESSAGE_REMOVED_TYPE)

        session.add(update_message)

    def mainloop(self):
        while True:
            try:
                with db_utils.db_session_scope(self.db_session) as session:
                    users = session.query(models.User).all()

                    for user in users:
                        works = user.works
                        self.update_works(works)

                        for id, work in enumerate(works):
                            if not work.was_removed:
                                if id > 0:
                                    time.sleep(Config.WORKS_UPDATER_JOBS_DELAY)

                                chapters_struct = works_utils.get_chapters_struct(work.work_id)

                                work_data = works_utils.get_work(work.work_id, chapters_struct=chapters_struct,
                                                                 delay_between_chapters=2)
                                fresh_chapters = models_utils.create_chapters_models(work_data)

                                for fresh_chapter in fresh_chapters:
                                    if self.check_if_new_chapter(fresh_chapter.chapter_id, work.chapters):
                                        self.add_chapter(work, fresh_chapter, session)

                                self.check_chapters_for_removed_ones(fresh_chapters, work, session)

            except Exception as e:
                self.app.logger.error(f"[{self.get_process_name()}] - {str(e)}")

            time.sleep(Config.WORKS_UPDATER_INTERVAL)
