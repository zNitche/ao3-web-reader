import time
import random
from ao3_web_reader.utils import works_utils
from ao3_web_reader.modules.tasks.task_base import ProcessTask
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import models, processes_manager, db


class WorkUpdaterTask(ProcessTask):
    def __init__(self, owner_id, work_id):
        super().__init__(owner_id)

        self.work_id = work_id

    def mainloop(self):
        self.update_process_data()

        try:
            work = models.Work.query.filter_by(work_id=self.work_id, owner_id=self.owner_id).first()
            self.logger.info(f"{work.name} force update")

            for chapter in work.chapters:
                if not chapter.was_removed:
                    try:
                        chapter_data = works_utils.get_chapter(self.work_id, chapter.chapter_id)

                        if chapter_data:
                            chapter.text = chapter_data
                            db.commit()

                            self.logger.info(f"updated data for {chapter.title}")

                        time.sleep(random.randint(3, 5))

                    except Exception as e:
                        self.logger.exception(f"error while updating: {chapter.title}")

                self.update_process_data()

        except Exception as e:
            self.logger.exception("mainloop error")

        finally:
            self.finish_process()

    def update_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.WORK_ID: self.work_id,
            ProcessesConsts.PROCESS_NAME: self.process_name,
        }

        processes_manager.set_process_data(self.unique_process_name, process_data)
