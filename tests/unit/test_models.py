from tests.consts import UsersConsts
from ao3_web_reader import models


def test_user():
    user = models.User(username=UsersConsts.TEST_USER_NAME,
                       password=UsersConsts.TEST_USER_PASSWORD)

    assert user.username == UsersConsts.TEST_USER_NAME
    assert user.password == UsersConsts.TEST_USER_PASSWORD


def test_tag():
    name = "test_tag"
    tag = models.Tag(name=name, owner_id=0)

    assert tag.name == name


def test_work():
    name = "work"
    work_id = "123321"
    description = "test desc"

    work = models.Work(name=name, work_id=work_id, owner_id=0, tag_id=0, description=description)

    assert work.name == name
    assert work.work_id == work_id
    assert work.description == description


def test_chapter():
    chapter_id = "321123"
    title = "chapter"

    chapter = models.Chapter(chapter_id=chapter_id, title=title, work_id=1)

    assert chapter.chapter_id == chapter_id
    assert chapter.title == title


def test_text_row():
    content = "test content"

    row = models.TextRow(content=content, chapter_id=0)

    assert row.content == content


def test_update_message():
    chapter_name = "chapter"

    message = models.UpdateMessage(chapter_name=chapter_name, work_id=0)

    assert message.chapter_name == chapter_name
