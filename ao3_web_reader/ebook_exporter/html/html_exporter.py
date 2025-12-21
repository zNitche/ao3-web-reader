import os
import config
import copy
from bs4 import BeautifulSoup
from datetime import datetime
from ao3_web_reader import models
from ao3_web_reader.logger import Logger


class HTMLExporter:
    def __init__(self, user_id: str, work: models.Work):
        self.user_id = user_id
        self.work = work

        self.extension = "html"

        self.logger = Logger(logger_name=f"HTMLExporter_{self.user_id}",
                             logs_filename="HTMLExporter.log",
                             logs_path=os.path.join(config.Config.LOGS_DIR_PATH, "ebook_exporters"),
                             backup_log_files_count=1)

    def __load_template(self, type: str):
        template_path = os.path.join(config.APP_ROOT, "ebook_exporter", "html", "templates", f"{type}.html")

        if not os.path.exists(template_path):
            raise Exception(f"template file doesn't exist: {template_path}")

        with open(template_path, "r") as template_file:
            template_content = template_file.read()

        return template_content

    def __replace_template_value(self, template: str, tag: str, value: str, replace_all=True):
        return template.replace("{{" + tag + "}}", value, -1 if replace_all else 1)

    def __convert_date(self, date: datetime, format="%d-%m-%Y"):
        return date.strftime(format)

    def __prettify(self, content: str):
        soup = BeautifulSoup(content, features="html.parser")
        return soup.prettify()

    def __build_table_of_contents(self, chapters: list[models.Chapter]):
        core_template = self.__load_template("core")
        item_template = self.__load_template("chapter_item")

        core_template = self.__replace_template_value(core_template, "work_name", self.work.name)
        core_template = self.__replace_template_value(core_template, "work_added_date",
                                                      self.__convert_date(self.work.date))
        core_template = self.__replace_template_value(core_template, "work_last_update",
                                                      self.__convert_date(self.work.last_updated))
        core_template = self.__replace_template_value(core_template, "work_description", self.work.description)

        results = []

        for ind, chapter in enumerate(chapters, start=1):
            template = copy.copy(item_template)

            template = self.__replace_template_value(template, "href", f"{ind}.html")
            template = self.__replace_template_value(template, "title", chapter.title)

            results.append(template)

        core_template = self.__replace_template_value(core_template, "items", "".join(results))

        return core_template

    def __build_chapter(self, chapter: models.Chapter, template: str):
        self.logger.info(f"building {chapter.title}...")

        template = self.__replace_template_value(template, "title", chapter.title)
        template = self.__replace_template_value(template, "date", self.__convert_date(chapter.date))
        template = self.__replace_template_value(template, "content", chapter.text)

        self.logger.info(f"{chapter.title} has been completed")

        return template

    def __write_file(self, path: str, content: str, prettify: bool):
        with open(path, "w") as file:
            if prettify:
                content = self.__prettify(content)

            file.write(content)

    def export(self, output_dir_path: str, prettify=True):
        self.logger.info("stating export process...")

        try:
            self.logger.info("building table of contents...")
            table_of_contents = self.__build_table_of_contents(self.work.chapters)

            self.logger.info("building chapters...")
            chapter_template = self.__load_template("chapter")
            chapters = []

            for chapter in self.work.chapters:
                self.logger.info(f"building html for {chapter.title}...")

                chapter_template_cp = copy.copy(chapter_template)
                chapters.append(self.__build_chapter(chapter, chapter_template_cp))

            self.logger.info("saving exported data...")

            self.__write_file(os.path.join(output_dir_path, "index.html"), table_of_contents, prettify)

            for ind, chapter in enumerate(chapters, start=1):
                self.__write_file(os.path.join(output_dir_path, f"{ind}.html"), chapter, prettify)

            self.logger.info(f"exported data has been saved...")

        except Exception as e:
            self.logger.exception(f"error while exporting {self.work.name}")
