from ao3_web_reader.utils import works_utils, db_utils
from ao3_web_reader.app_modules.processes.process_base import ProcessBase


class ScrapperProcess(ProcessBase):
    def __init__(self, app, owner_id, work_id):
        super().__init__(app, owner_id)

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
                work = works_utils.create_work_model(work_data, self.owner_id)
                work.chapters = works_utils.create_chapters_models(work_data)

                session.add(work)

        except Exception as e:
            pass

        finally:
            self.finish_process()

    def update_process_data(self):
        process_data = {
            "pid": self.process_pid,
            "owner_id": self.owner_id,
            "work_id": self.work_id,
            "work_title": self.work_title
        }

        self.app.processes_manager.set_process_data(self.timestamp, process_data)