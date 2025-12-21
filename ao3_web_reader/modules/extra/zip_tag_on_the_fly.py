from zipfile import ZipFile
import os
import tempfile
from ao3_web_reader.ebook_exporter import HTMLExporter
from ao3_web_reader.utils import works_utils
from ao3_web_reader.modules.extra.zip_on_the_fly import ZipFileStream, ZipOnTheFly


class ZipTagOnTheFly(ZipOnTheFly):
    def __init__(self, user_id, tag_name, works, chunk_size=1_000_000):
        super().__init__(chunk_size=chunk_size)

        self.tag_name = tag_name
        self.works = works
        self.user_id = user_id

    def __zip_work(self, files_path, work):
        exporter = HTMLExporter(self.user_id, work)

        exporter.export(files_path, prettify=True)
        work_name = works_utils.serialize_work_name(work.name)
        archive_name = f"{work_name}.zip"

        archive_path = os.path.join(tempfile.gettempdir(), archive_name)
        with ZipFile(archive_path, mode="w") as archive:
            for file in os.listdir(files_path):
                path = os.path.join(files_path, file)

                archive.write(path, arcname=file)

        return archive_path, archive_name

    def generator(self):
        core_dir_prefix = f"{str(self.user_id)}_{str(self.tag_name)}"

        with tempfile.TemporaryDirectory(prefix=core_dir_prefix) as tmp_dir_name:
            with ZipFileStream() as zip_stream:
                with ZipFile(zip_stream, mode="w") as zip_file:
                    for work in self.works:
                        dir_path = os.path.join(
                            tempfile.gettempdir(), tmp_dir_name, str(work.id))

                        if not os.path.exists(dir_path):
                            os.mkdir(dir_path)

                        work_archive_path, archive_name = self.__zip_work(
                            dir_path, work)

                        yield from self._handle_file(zip_file=zip_file, zip_stream=zip_stream,
                                                     file_name=archive_name, file_path=work_archive_path)

            # drain stream
            yield zip_stream.get()
