from ao3_web_reader.utils import works_utils, models_utils
from ao3_web_reader.modules.processes.process_base import ProcessBase
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import models, db


class ScraperProcess(ProcessBase):
    def __init__(self, app, owner_id, tag_name, work_id):
        super().__init__(app, owner_id)

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
        self.work_title = works_utils.get_work_name(self.work_id)
        self.update_process_data()

        try:
            work_data = works_utils.get_work(self.work_id, progress_callback=self.get_work_update_callback)

            work_description = works_utils.get_work_description(self.work_id)

            tag = db.session.query(models.Tag).filter_by(owner_id=self.owner_id, name=self.tag_name).first()

            work = models_utils.create_work_model(work_data, self.owner_id, tag.id, work_description)
            work.chapters = models_utils.create_chapters_models(work_data)

            db.add(work)

        except Exception as e:
            self.app.logger.error(f"[{self.get_process_name()}] - {str(e)}")

        finally:
            self.finish_process()

    def update_process_data(self):
        process_data = {
            ProcessesConsts.PID: self.process_pid,
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.WORK_ID: self.work_id,
            ProcessesConsts.WORK_TITLE: self.work_title,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROGRESS: self.progress,
        }

        self.app.processes_manager.set_process_data(self.timestamp, process_data)
