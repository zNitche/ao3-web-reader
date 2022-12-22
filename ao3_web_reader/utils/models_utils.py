from ao3_web_reader import models
from ao3_web_reader.consts import WorksConsts


def create_chapters_models(work_data):
    chapters = []

    for chapter_data in work_data[WorksConsts.CHAPTERS_DATA]:
        chapter_id = chapter_data[WorksConsts.ID]
        title = chapter_data[WorksConsts.NAME]
        content = chapter_data[WorksConsts.CONTENT]

        chapter = models.Chapter(title=title, chapter_id=chapter_id)

        for text in content:
            text_row = models.TextRow(content=text)
            chapter.rows.append(text_row)

        chapters.append(chapter)

    return chapters


def create_chapter_model(chapter_data):
    chapter_id = chapter_data[WorksConsts.ID]
    title = chapter_data[WorksConsts.NAME]
    content = chapter_data[WorksConsts.CONTENT]

    chapter = models.Chapter(title=title, chapter_id=chapter_id)

    for text in content:
        text_row = models.TextRow(content=text)
        chapter.rows.append(text_row)

    return chapter


def create_work_model(work_data, owner_id, tag_id):
    work = models.Work(name=work_data[WorksConsts.NAME],
                       owner_id=owner_id,
                       tag_id=tag_id,
                       work_id=work_data[WorksConsts.WORK_ID])

    return work


def create_update_message_model(work_name, chapter_name):
    message = models.UpdateMessage(work_name=work_name, chapter_name=chapter_name)

    return message
