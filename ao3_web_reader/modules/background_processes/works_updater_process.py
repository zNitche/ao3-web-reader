from ao3_web_reader.utils import works_utils, models_utils
from ao3_web_reader.modules.background_processes.background_process_base import BackgroundProcessBase
from ao3_web_reader import models
from ao3_web_reader.consts import UpdateMessagesConsts, ProcessesConsts, ChaptersConsts
from config import Config
from datetime import datetime
import time, random


class WorksUpdaterProcess(BackgroundProcessBase):
    def __init__(self):
        super().__init__(startup_delay=60)

        self.is_sync_running = False
        self.progress = 0

    def get_process_data(self):
        process_data = {
            ProcessesConsts.IS_RUNNING: self.is_sync_running,
            ProcessesConsts.PROGRESS: self.progress,
        }

        return process_data

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

    def check_chapters_for_removed_ones(self, chapters_struct, work):
        work_chapters_ids = [chapter.chapter_id for chapter in work.get_not_removed_chapters()]
        source_chapters_ids = [chapter.get(ChaptersConsts.ID) for chapter in chapters_struct]

        if all(work_chapters_ids) and all(source_chapters_ids):
            removed_chapters_ids = list(set(work_chapters_ids).difference(source_chapters_ids))

            for chapter_id in removed_chapters_ids:
                chapter = self.get_chapter_by_id(work.chapters, chapter_id)

                if chapter:
                    self.mark_chapter_as_removed(work, chapter)

    def update_chapters_order_ids(self, chapters):
        not_removed_chapters = [chapter for chapter in chapters if not chapter.was_removed]
        not_removed_chapters.sort(key=lambda chapter: chapter.order_id)

        for order_id, chapter in enumerate(not_removed_chapters):
            chapter.order_id = order_id

    def update_works_states(self, works):
        for work in works:
            if not works_utils.check_if_work_exists(work.work_id):
                work.was_removed = True

            time.sleep(random.randrange(1, Config.WORKS_EXIST_CHECK_JOBS_DELAY))

    def add_chapter(self, work, chapter):
        work.chapters.append(chapter)
        work.last_updated = datetime.now()

        update_message = models_utils.create_update_message_model(work.id,
                                                                  chapter.title,
                                                                  UpdateMessagesConsts.MESSAGE_ADDED_TYPE)

        self.db.add(update_message)

    def mark_chapter_as_removed(self, work, chapter):
        chapter.was_removed = True
        chapter.order_id = None
        work.last_updated = datetime.now()

        update_message = models_utils.create_update_message_model(work.id,
                                                                  chapter.title,
                                                                  UpdateMessagesConsts.MESSAGE_REMOVED_TYPE)

        self.db.add(update_message)

    def mainloop(self):
        self.logger.info("starting mainloop")

        while True:
            try:
                processed_works = 0

                self.is_sync_running = True
                self.update_process_data()

                users = models.User.query.all()
                works_count = sum([len(user.works) for user in users])

                for user in users:
                    works = user.works
                    self.logger.info(f"updating {len(works)} works of {user.username}")

                    self.logger.info(f"updating works states")
                    self.update_works_states(works)

                    for id, work in enumerate(works):
                        if not work.was_removed:
                            self.logger.info(f"updating {work.name} chapters")

                            if id > 0:
                                time.sleep(random.randrange(2, Config.WORKS_UPDATER_JOBS_DELAY))

                            chapters_struct = works_utils.get_chapters_struct(work.work_id)

                            if len(chapters_struct) > 0:
                                for chapter_struct in chapters_struct:
                                    if self.check_if_new_chapter(chapter_struct.get(ChaptersConsts.ID),
                                                                 work.chapters):

                                        chapter_struct_data = works_utils.get_chapter_data_struct(chapter_struct)
                                        new_chapter = models_utils.create_chapter_model(chapter_struct_data)


                                        self.add_chapter(work, new_chapter)

                                self.check_chapters_for_removed_ones(chapters_struct, work)
                                self.update_chapters_order_ids(work.chapters)

                        processed_works += 1
                        self.progress = int(processed_works * 100 / works_count)

                        self.update_process_data()

            except Exception as e:
                self.logger.exception("mainloop exception")

            finally:
                self.is_sync_running = False
                self.update_process_data()

                self.progress = 0

            self.logger.info(f"update completed, waiting {Config.WORKS_UPDATER_INTERVAL} for next iteration...")

            time.sleep(Config.WORKS_UPDATER_INTERVAL)
