import os
import copy
from ao3_web_reader import models
from ao3_web_reader.ebook_exporter import BaseExporter


class HTMLExporter(BaseExporter):
    def __init__(self, user_id: str, work: models.Work):
        super().__init__(user_id=user_id, work=work, logger_extra={})

    def __build_table_of_contents(self, chapters: list[models.Chapter]):
        core_template = self._load_html_template("core")
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

    def __build_chapter(self, chapter: models.Chapter, template: str):
        self.logger.debug(f"building {chapter.title}...")

        template = self._replace_html_template_value(
            template, "title", chapter.title)
        template = self._replace_html_template_value(
            template, "date", self._convert_date(chapter.date))
        template = self._replace_html_template_value(
            template, "content", chapter.text)

        self.logger.debug(f"{chapter.title} has been completed")

        return template

    def __write_file(self, path: str, content: str, prettify: bool):
        with open(path, "w") as file:
            if prettify:
                content = self._prettify_html(content)

            file.write(content)

    def export(self, output_dir_path: str, prettify=True):
        self.logger.info("stating export process...")

        try:
            self.logger.debug("building table of contents...")
            table_of_contents = self.__build_table_of_contents(
                self.work.chapters)

            self.logger.debug("building chapters...")
            chapter_template = self._load_html_template("chapter")
            chapters = []

            for chapter in self.work.chapters:
                self.logger.debug(f"building html for {chapter.title}...")

                chapter_template_cp = copy.copy(chapter_template)
                chapters.append(self.__build_chapter(
                    chapter, chapter_template_cp))

            self.logger.debug("saving exported data...")

            self.__write_file(os.path.join(
                output_dir_path, "index.html"), table_of_contents, prettify)

            for ind, chapter in enumerate(chapters, start=1):
                self.__write_file(os.path.join(
                    output_dir_path, f"{ind}.html"), chapter, prettify)

            self.logger.info(f"exported data has been saved...")

        except Exception as e:
            self.logger.exception(f"error while exporting {self.work.name}")
