import time
import random
from ao3_web_reader.utils import works_utils
from ao3_web_reader.modules.tasks.task_base import ProcessTask
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import models, processes_manager, db


class TagUpdaterTask(ProcessTask):
    def __init__(self, owner_id, tag_id):
        super().__init__(owner_id)

        self.tag_id = tag_id

    def mainloop(self):
        self.update_process_data()
        works_updated = 0

        try:
            tag = models.Tag.query.filter_by(owner_id=self.owner_id, id=self.tag_id).first()

            if tag:
                works = models.Work.query.filter_by(owner_id=self.owner_id).all()

                works_count = len(works)
                self.logger.info(f"{tag.name} force update")

                for work in works:
                    if not work.was_removed:
                        self.logger.info(f"updating {work.name}, {works_count - works_updated} to go...")

                        for chapter in work.chapters:
                            if not chapter.was_removed:
                                self.logger.info(f"updating {chapter.title}")

                                try:
                                    chapter_data = works_utils.get_chapter(work.work_id, chapter.chapter_id)

                                    if chapter_data:
                                        chapter.text = chapter_data
                                        db.commit()

                                        self.logger.info(f"updated data for {chapter.title}")

                                    delay = random.randint(10, 20)
                                    self.logger.info(f"waiting for {delay} seconds...")

                                    time.sleep(delay)

                                except Exception as e:
                                    self.logger.exception(f"error while updating: {chapter.title}")

                    works_updated += 1

                    delay = random.randint(50, 70)
                    self.logger.info(f"{work.name} update has been completed, waiting for {delay} seconds...")

                    time.sleep(delay)

        except Exception as e:
            self.logger.exception("mainloop error")

        finally:
            self.finish_process()

    def update_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.process_name,
        }

        processes_manager.set_process_data(self.unique_process_name, process_data)
