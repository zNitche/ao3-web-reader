from ao3_web_reader import models
from ao3_web_reader.modules.scrapers import ChapterStruct, WorkStruct


def create_chapters_models(work_data: WorkStruct):
    chapters = []

    for chapter_data in work_data.chapters:
        chapters.append(create_chapter_model(chapter_data))

    return chapters


def create_chapter_model(chapter_data: ChapterStruct):
    chapter_id = chapter_data.id
    title = chapter_data.name
    content = chapter_data.content
    order_id = chapter_data.order_id
    chapter_date = chapter_data.date

    chapter = models.Chapter(title=title, chapter_id=chapter_id, text=content,
                             order_id=order_id, date=chapter_date, completed=False)

    return chapter


def create_work_model(work_data: WorkStruct, owner_id: str, tag_id: str, description: str):
    work = models.Work(name=work_data.name,
                       owner_id=owner_id,
                       tag_id=tag_id,
                       work_id=work_data.id,
                       description=description)

    return work


def create_update_message_model(work_id, chapter_name, message_type):
    message = models.UpdateMessage(
        work_id=work_id, chapter_name=chapter_name, type=message_type)

    return message
