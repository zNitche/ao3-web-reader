import os
import copy
from ao3_web_reader import models
from ao3_web_reader.ebook_exporter import XHtmlExporter


class HTMLExporter(XHtmlExporter):
    def __init__(self, user_id: str, work: models.Work):
        super().__init__(user_id=user_id, work=work, logger_extra={})

    def export(self, output_dir_path: str, prettify=True):
        self.logger.info("stating export process...")

        try:
            self.logger.debug("building table of contents...")
            table_of_contents = self._build_index(
                self.work.chapters)

            self.logger.debug("building chapters...")
            chapter_template = self._load_html_template("chapter")
            chapters = []

            for chapter in self.work.chapters:
                self.logger.debug(f"building html for {chapter.title}...")

                chapter_template_cp = copy.copy(chapter_template)
                chapters.append(self._build_chapter(
                    chapter, chapter_template_cp))

            self.logger.debug("saving exported data...")

            self._write_xhtml_file(os.path.join(
                output_dir_path, "index.html"), table_of_contents, prettify)

            for ind, chapter in enumerate(chapters, start=1):
                self._write_xhtml_file(os.path.join(
                    output_dir_path, f"{ind}.html"), chapter, prettify)

            self.logger.info(f"exported data has been saved...")

        except Exception as e:
            self.logger.exception(f"error while exporting {self.work.name}")
