from ao3_web_reader.utils import works_utils, models_utils
from ao3_web_reader.modules.tasks.task_base import TaskBase
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import models, db, processes_manager


class ScraperTask(TaskBase):
    def __init__(self, owner_id, tag_name, work_id):
        super().__init__(owner_id)

        self.tag_name = tag_name
        self.work_id = work_id
        self.work_title = ""

        self.progress = 0

    def calc_progres(self, current_step, max_steps):
        self.progress = int(current_step * 100 / max_steps)

    def get_work_update_callback(self, current_step, total_steps):
        self.calc_progres(current_step, total_steps)
        self.update_process_data()

    def mainloop(self):
        try:
            self.work_title = works_utils.get_work_name(self.work_id)
            self.update_process_data()

            work_data = works_utils.get_work(self.work_id, progress_callback=self.get_work_update_callback)
            work_description = works_utils.get_work_description(self.work_id)

            self.logger.info(f"got {self.work_title} data")

            tag = models.Tag.query.filter_by(owner_id=self.owner_id, name=self.tag_name).first()

            work = models_utils.create_work_model(work_data, self.owner_id, tag.id, work_description)
            work.chapters = models_utils.create_chapters_models(work_data)

            db.add(work)

        except Exception as e:
            self.logger.exception("mainloop error")

        finally:
            self.finish_process()

    def update_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.WORK_ID: self.work_id,
            ProcessesConsts.WORK_TITLE: self.work_title,
            ProcessesConsts.PROCESS_NAME: self.process_name,
            ProcessesConsts.PROGRESS: self.progress,
        }

        processes_manager.set_process_data(self.unique_process_name, process_data)
