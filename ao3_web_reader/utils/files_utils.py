import zipfile
import os


def write_work_to_files(work, files_path):
    for chapter in work.chapters:
        chapter_file_path = os.path.join(files_path, f"{chapter.title}.txt")

        with open(chapter_file_path, "a") as chapter_file:
            for row in chapter.rows:
                chapter_file.write(row.content)
                chapter_file.write("\n")


def zip_files(archive_path, files_path, exclude_extensions=None):
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in os.listdir(files_path):
            if exclude_extensions is None or not file.endswith(exclude_extensions):
                file_path = os.path.join(files_path, file)

                archive.write(file_path, file)


def zip_dirs(archive_path, dirs_path, exclude_extensions=None):
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for root, _, files in os.walk(dirs_path, topdown=True):
            root_name = root.split("/")[-1]

            for file_name in files:
                if exclude_extensions is None or not file_name.endswith(exclude_extensions):
                    file_path = os.path.join(root, file_name)

                    archive.write(file_path, os.path.join(root_name, file_name))
