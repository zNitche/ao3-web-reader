from ao3_web_reader.utils import works_utils
from ao3_web_reader.modules.processes.process_base import ProcessBase
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import models, processes_manager


class ChapterUpdaterProcess(ProcessBase):
    def __init__(self, owner_id, work_id, chapter_id):
        super().__init__(owner_id)

        self.work_id = work_id
        self.chapter_id = chapter_id

        self.progress = 0

    def calc_progres(self, current_step, max_steps):
        self.progress = int(current_step * 100 / max_steps)

    def get_work_update_callback(self, current_step, total_steps):
        self.calc_progres(current_step, total_steps)
        self.update_process_data()

    def mainloop(self):
        self.update_process_data()

        try:
            chapter = models.Chapter.query.filter_by(chapter_id=self.chapter_id).first()

            self.logger.info(f"{chapter.title} force update")

            chapter_data = works_utils.get_chapter(self.work_id, self.chapter_id)
            chapter.text = "\n".join(chapter_data)

            self.logger.info(f"got data for {chapter.title}")

        except Exception as e:
            self.logger.exception("mainloop error")

        finally:
            self.finish_process()

    def update_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.WORK_ID: self.work_id,
            ProcessesConsts.CHAPTER_ID: self.chapter_id,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROGRESS: self.progress,
        }

        processes_manager.set_process_data(self.timestamp, process_data)
