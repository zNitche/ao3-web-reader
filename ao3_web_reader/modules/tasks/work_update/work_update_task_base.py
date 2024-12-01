from ao3_web_reader.utils import works_utils
from ao3_web_reader.modules.tasks.task_base import ProcessTask
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import processes_manager, db


class WorkUpdateTaskBase(ProcessTask):
    def __init__(self, owner_id):
        super().__init__(owner_id)

    def _update_description(self, work):
        try:
            description = works_utils.get_work_description(work.work_id)

            work.description = description
            db.commit()

            self.logger.info("work's description has been updated successfully")

        except Exception as e:
            self.logger.exception("error while updating work's description")

    def _update_chapter(self, work, chapter):
        self.logger.info(f"updating {chapter.title}")

        chapter_data = works_utils.get_chapter(work.work_id, chapter.chapter_id)

        if chapter_data:
            chapter.text = chapter_data
            db.commit()

            self.logger.info(f"updated {chapter.title} content")

    def mainloop(self):
        raise NotImplementedError()

    def update_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.process_name,
        }

        processes_manager.set_process_data(self.unique_process_name, process_data)
