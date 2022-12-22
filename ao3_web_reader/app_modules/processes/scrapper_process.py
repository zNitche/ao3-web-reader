from ao3_web_reader.utils import works_utils, db_utils, models_utils
from ao3_web_reader.app_modules.processes.process_base import ProcessBase
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import models


class ScrapperProcess(ProcessBase):
    def __init__(self, app, owner_id, tag_name, work_id):
        super().__init__(app, owner_id)

        self.tag_name = tag_name
        self.work_id = work_id
        self.work_title = ""

    def start_process(self):
        self.process.start()
        self.process_pid = self.process.pid

    def mainloop(self):
        self.work_title = works_utils.get_work_name(self.work_id)
        self.update_process_data()

        try:
            work_data = works_utils.get_work(self.work_id)

            with db_utils.db_session_scope(self.db_session) as session:
                tag = session.query(models.Tag).filter_by(owner_id=self.owner_id, name=self.tag_name).first()

                work = models_utils.create_work_model(work_data, self.owner_id, tag.id)
                work.chapters = models_utils.create_chapters_models(work_data)

                session.add(work)

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
        }

        self.app.processes_manager.set_process_data(self.timestamp, process_data)
