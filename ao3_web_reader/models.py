from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship, mapped_column
from ao3_web_reader.db import Base
from ao3_web_reader import db
from ao3_web_reader.consts import UpdateMessagesConsts


class User(Base, UserMixin):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), unique=False, nullable=False)

    tags = relationship("Tag", backref="owner", cascade="all, delete-orphan", lazy=True)
    works = relationship("Work", backref="owner", cascade="all, delete-orphan", lazy=True)

    def get_favorite_works(self):
        return [work for work in self.works if work.favorite]


class Tag(Base):
    __tablename__ = "tags"

    id = mapped_column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)

    works = relationship("Work", backref="tag", cascade="all, delete-orphan", lazy=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def get_favorite_works(self):
        return [work for work in self.works if work.favorite]


class Work(Base):
    __tablename__ = "works"

    id = mapped_column(Integer, primary_key=True)

    work_id = Column(String, unique=False, nullable=False)
    name = Column(String(200), unique=False, nullable=False)
    description = Column(String, unique=False, nullable=True)

    date = Column(DATETIME, unique=False, nullable=False, default=datetime.utcnow)
    last_updated = Column(DATETIME, unique=False, nullable=True, default=datetime.utcnow)

    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    favorite = Column(Boolean, nullable=True, default=False)
    was_removed = Column(Boolean, unique=False, nullable=False, default=False)

    chapters = relationship("Chapter", backref="work", cascade="all, delete-orphan", lazy=True)
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
    chapter_id = Column(String, unique=False, nullable=False)
    order_id = Column(Integer, unique=False, nullable=True)

    title = Column(String(200), unique=False, nullable=False)
    date = Column(DATETIME, unique=False, nullable=False, default=datetime.utcnow)

    text = Column(String, unique=False, nullable=False)

    was_removed = Column(Boolean, unique=False, nullable=False, default=False)
    completed = Column(Boolean, unique=False, nullable=True, default=False)

    work_id = Column(Integer, ForeignKey("works.id"), nullable=False)

    def get_formatted_text(self):
        return self.text.split("\n")

    def get_next_chapter(self):
        next_chapter = db.session.query(Chapter).filter_by(work_id=self.work_id, order_id=self.order_id + 1).first()

        return next_chapter

    def get_prev_chapter(self):
        prev_chapter = db.session.query(Chapter).filter_by(work_id=self.work_id, order_id=self.order_id - 1).first()

        return prev_chapter


class UpdateMessage(Base):
    __tablename__ = "update_messages"

    id = mapped_column(Integer, primary_key=True)
    chapter_name = Column(String, unique=False, nullable=True)
    type = Column(String, unique=False, nullable=False, default=UpdateMessagesConsts.MESSAGE_ADDED_TYPE)
    date = Column(DATETIME, unique=False, nullable=False, default=datetime.utcnow)

    work_id = Column(Integer, ForeignKey("works.id"), nullable=False)

    def get_message_by_type(self):
        message = None

        if self.type == UpdateMessagesConsts.MESSAGE_ADDED_TYPE:
            message = f"Added '{ self.chapter_name }' to"

        elif self.type == UpdateMessagesConsts.MESSAGE_REMOVED_TYPE:
            message = f"Removed '{self.chapter_name}' from"

        return message
