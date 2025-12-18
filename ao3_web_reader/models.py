from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship, mapped_column
from ao3_web_reader.db import Base
from ao3_web_reader.consts import UpdateMessagesConsts


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(20), unique=True, nullable=False)
    password = mapped_column(String(128), unique=False, nullable=False)

    tags = relationship("Tag", backref="owner", cascade="all, delete-orphan", lazy=True)
    works = relationship("Work", backref="owner", cascade="all, delete-orphan", lazy=True)

    def get_favorite_works(self):
        return [work for work in self.works if work.favorite]


class Tag(Base):
    __tablename__ = "tags"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=False, nullable=False)

    works = relationship("Work", backref="tag", cascade="all, delete-orphan", lazy=True)
    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    def get_favorite_works(self):
        return [work for work in self.works if work.favorite]


class Work(Base):
    __tablename__ = "works"

    id = mapped_column(Integer, primary_key=True)

    work_id = mapped_column(String, unique=False, nullable=False)
    name = mapped_column(String(200), unique=False, nullable=False)
    description = mapped_column(String, unique=False, nullable=True)

    date = mapped_column(DATETIME, unique=False, nullable=False, default=datetime.utcnow)
    last_updated = mapped_column(DATETIME, unique=False, nullable=True, default=datetime.utcnow)

    tag_id = mapped_column(Integer, ForeignKey("tags.id"), nullable=False)
    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    favorite = mapped_column(Boolean, nullable=True, default=False)
    was_removed = mapped_column(Boolean, unique=False, nullable=False, default=False)

    chapters = relationship("Chapter", backref="work", cascade="all, delete-orphan", lazy="subquery")
    update_messages = relationship("UpdateMessage", backref="work", cascade="all, delete-orphan", lazy=True)

    def get_not_removed_chapters(self):
        return [chapter for chapter in self.chapters if not chapter.was_removed]

    def get_removed_chapters(self):
        return [chapter for chapter in self.chapters if chapter.was_removed]

    def get_completed_chapters(self):
        return [chapter for chapter in self.chapters if chapter.completed]

    def all_chapters_completed(self):
        chapters_completion = [chapter.completed for chapter in self.chapters]

        return all(chapters_completion)


class Chapter(Base):
    __tablename__ = "chapters"

    id = mapped_column(Integer, primary_key=True)
    chapter_id = mapped_column(String, unique=False, nullable=False)
    order_id = mapped_column(Integer, unique=False, nullable=True)

    title = mapped_column(String(200), unique=False, nullable=False)
    date = mapped_column(DATETIME, unique=False, nullable=False, default=datetime.utcnow)

    text = mapped_column(String, unique=False, nullable=False)

    was_removed = mapped_column(Boolean, unique=False, nullable=False, default=False)
    completed = mapped_column(Boolean, unique=False, nullable=True, default=False)

    work_id = mapped_column(Integer, ForeignKey("works.id"), nullable=False)

    def get_next_chapter(self):
        next_chapter = Chapter.query.filter_by(work_id=self.work_id, order_id=self.order_id + 1).first()

        return next_chapter

    def get_prev_chapter(self):
        prev_chapter = Chapter.query.filter_by(work_id=self.work_id, order_id=self.order_id - 1).first()

        return prev_chapter


class UpdateMessage(Base):
    __tablename__ = "update_messages"

    id = mapped_column(Integer, primary_key=True)
    chapter_name = mapped_column(String, unique=False, nullable=True)
    type = mapped_column(String, unique=False, nullable=False, default=UpdateMessagesConsts.MESSAGE_ADDED_TYPE)
    date = mapped_column(DATETIME, unique=False, nullable=False, default=datetime.utcnow)

    work_id = mapped_column(Integer, ForeignKey("works.id"), nullable=False)

    def get_message_by_type(self):
        message = None

        if self.type == UpdateMessagesConsts.MESSAGE_ADDED_TYPE:
            message = f"Added '{ self.chapter_name }' to"

        elif self.type == UpdateMessagesConsts.MESSAGE_REMOVED_TYPE:
            message = f"Removed '{self.chapter_name}' from"

        return message
