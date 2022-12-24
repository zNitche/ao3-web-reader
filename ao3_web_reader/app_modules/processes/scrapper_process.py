from ao3_web_reader.utils import works_utils, db_utils, models_utils
from ao3_web_reader.app_modules.processes.process_base import ProcessBase
from ao3_web_reader.consts import ProcessesConsts, WorksConsts
from ao3_web_reader import models


class ScrapperProcess(ProcessBase):
    def __init__(self, app, owner_id, tag_name, work_id):
        super().__init__(app, owner_id)

        self.tag_name = tag_name
        self.work_id = work_id
        self.work_title = ""

        self.progress = 0

    def start_process(self):
        self.process.start()
        self.process_pid = self.process.pid

    def calc_progres(self, current_step, max_steps):
        self.progress = int(current_step * 100 / max_steps)

    def get_work(self):
        # like works_utils.get_work()

        nav_soup = works_utils.get_work_nav_soup(self.work_id)
        chapters_urls_data = works_utils.get_chapters_urls_data(nav_soup)

        work_data = works_utils.get_work_struct(self.work_id)

        for id, chapter_url_data in enumerate(chapters_urls_data):
            chapter_data = works_utils.get_chapter_data_from_url_data(id, chapter_url_data)

            work_data[WorksConsts.CHAPTERS_DATA].append(chapter_data)

            self.calc_progres(id, len(chapters_urls_data))
            self.update_process_data()

        return work_data

    def mainloop(self):
        self.work_title = works_utils.get_work_name(self.work_id)
        self.update_process_data()

        try:
            # work_data = works_utils.get_work(self.work_id)
            work_data = self.get_work()

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
            ProcessesConsts.PROGRESS: self.progress,
        }

        self.app.processes_manager.set_process_data(self.timestamp, process_data)
