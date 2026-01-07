from typing import Any
import os
import config
from ao3_web_reader import models
from ao3_web_reader.logging import Logger


class BaseExporter:
    def __init__(self, user_id: str, work: models.Work, logger_extra: dict[str, Any]):
        self.user_id = user_id
        self.work = work

        logs_path = os.path.join(
            config.Config.LOGS_DIR_PATH, "ebook_exporters")

        logger_extras = {**{"user_id": user_id,
                            "work_id": str(work.id)}, **logger_extra}

        logger_name = self.__class__.__name__
        self.logger = Logger.get_expandable_logger(logger_name=logger_name,
                                                   extra=logger_extras,
                                                   logs_filename=f"{logger_name}.log",
                                                   logs_path=logs_path,
                                                   backup_log_files_count=1)

        def export(self, output_dir_path: str):
            raise NotImplementedError()
