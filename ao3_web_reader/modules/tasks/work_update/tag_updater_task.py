import time
import random
from ao3_web_reader.modules.tasks.work_update.work_update_task_base import WorkUpdateTaskBase
from ao3_web_reader import models


class TagUpdaterTask(WorkUpdateTaskBase):
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

                        self.logger.info("starting description update...")

                        self._update_description(work)
                        self.logger.info("starting chapters update...")

                        for chapter in work.chapters:
                            if not chapter.was_removed:
                                try:
                                    self._update_chapter(work, chapter)

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
