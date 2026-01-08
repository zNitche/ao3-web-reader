from typing import Any
import copy
import os
import config
from bs4 import BeautifulSoup
from ao3_web_reader import models
from ao3_web_reader.ebook_exporter import BaseExporter


class XHtmlExporter(BaseExporter):
    def __init__(self, user_id: str, work: models.Work, logger_extra: dict[str, Any]):
        super().__init__(user_id=user_id, work=work, logger_extra=logger_extra)

        self.templates_paths = os.path.join(
            config.APP_ROOT, "ebook_exporter", "templates")

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

    def _prettify_html(self, content: str):
        soup = BeautifulSoup(content, features="html.parser")
        return soup.prettify()

    def _build_index(self, chapters: list[models.Chapter], core_template="core"):
        core_template = self._load_html_template(core_template)
        item_template = self._load_html_template("chapter_item")

        core_template = self._replace_html_template_value(
            core_template, "work_name", self.work.name)
        core_template = self._replace_html_template_value(core_template, "work_added_date",
                                                          self._convert_date(self.work.date))
        core_template = self._replace_html_template_value(core_template, "work_last_update",
                                                          self._convert_date(self.work.last_updated))
        core_template = self._replace_html_template_value(
            core_template, "work_description", self.work.description)

        results = []

        for ind, chapter in enumerate(chapters, start=1):
            template = copy.copy(item_template)

            template = self._replace_html_template_value(
                template, "href", f"{ind}.html")
            template = self._replace_html_template_value(
                template, "title", chapter.title)

            results.append(template)

        core_template = self._replace_html_template_value(
            core_template, "items", "".join(results))

        return core_template

    def _build_chapter(self, chapter: models.Chapter, template: str):
        self.logger.debug(f"building {chapter.title}...")

        template = self._replace_html_template_value(
            template, "title", chapter.title)
        template = self._replace_html_template_value(
            template, "date", self._convert_date(chapter.date))
        template = self._replace_html_template_value(
            template, "content", chapter.text)

        self.logger.debug(f"{chapter.title} has been completed")

        return template

    def _write_xhtml_file(self, path: str, content: str, prettify: bool):
        with open(path, "w") as file:
            if prettify:
                content = self._prettify_html(content)

            file.write(content)

    def export(self, output_dir_path: str):
        raise NotImplementedError()
