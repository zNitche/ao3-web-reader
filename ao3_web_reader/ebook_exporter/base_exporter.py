from typing import Any
import os
import config
from bs4 import BeautifulSoup
from datetime import datetime
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

    def _load_html_template(self, type: str):
        template_path = os.path.join(
            config.APP_ROOT, "ebook_exporter", "templates", "html", f"{type}.html")

        if not os.path.exists(template_path):
            raise Exception(
                f"template file doesn't exist: {template_path}")

        with open(template_path, "r") as template_file:
            template_content = template_file.read()

        return template_content

    def _replace_html_template_value(self, template: str, tag: str, value: str, replace_all=True):
        return template.replace("{{" + tag + "}}", value, -1 if replace_all else 1)

    def _convert_date(self, date: datetime, format="%d-%m-%Y"):
        return date.strftime(format)

    def _prettify_html(self, content: str):
        soup = BeautifulSoup(content, features="html.parser")
        return soup.prettify()

    def export(self, output_dir_path: str):
        raise NotImplementedError()
