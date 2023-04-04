from ao3_web_reader import models
from ao3_web_reader.consts import WorksConsts, ChaptersConsts


def create_chapters_models(work_data):
    chapters = []

    for chapter_data in work_data[WorksConsts.CHAPTERS_DATA]:
        chapters.append(create_chapter_model(chapter_data))

    return chapters


def create_chapter_model(chapter_data):
    chapter_id = chapter_data[ChaptersConsts.ID]
    title = chapter_data[ChaptersConsts.NAME]
    content = chapter_data[ChaptersConsts.CONTENT]
    order_id = chapter_data[ChaptersConsts.ORDER_ID]
    chapter_date = chapter_data[ChaptersConsts.DATE]

    chapter = models.Chapter(title=title, chapter_id=chapter_id, text="\n".join(content),
                             order_id=order_id, date=chapter_date, completed=False)

    return chapter


def create_work_model(work_data, owner_id, tag_id, description):
    work = models.Work(name=work_data[WorksConsts.NAME],
                       owner_id=owner_id,
                       tag_id=tag_id,
                       work_id=work_data[WorksConsts.WORK_ID],
                       description=description)

    return work


def create_update_message_model(work_id, chapter_name, message_type):
    message = models.UpdateMessage(work_id=work_id, chapter_name=chapter_name, type=message_type)

    return message
