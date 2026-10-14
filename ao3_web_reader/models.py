import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ao3_web_reader.db import Base
from ao3_web_reader.consts import UpdateMessagesConsts


class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chapter_id: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)

    title: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DATETIME, unique=False,
                         nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))

    text: Mapped[str] = mapped_column(String, unique=False, nullable=False)

    was_removed: Mapped[bool] = mapped_column(
        Boolean, unique=False, nullable=False, default=False)
    completed: Mapped[bool] = mapped_column(Boolean, unique=False,
                              nullable=True, default=False)

    work_id: Mapped[int] = mapped_column(Integer, ForeignKey("works.id"), nullable=False)
    work: Mapped["Work"] = relationship("Work", back_populates="chapters")

    def get_next_chapter(self) -> "Chapter | None":
        next_chapter = Chapter.query.filter_by(
            work_id=self.work_id, order_id=self.order_id + 1).first()

        return next_chapter

    def get_prev_chapter(self) -> "Chapter | None":
        prev_chapter = Chapter.query.filter_by(
            work_id=self.work_id, order_id=self.order_id - 1).first()

        return prev_chapter


class Work(Base):
    __tablename__ = "works"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    work_id: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    name: Mapped[str] = mapped_column(
        String(200), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(
        String, unique=False, nullable=True)

    date: Mapped[datetime.datetime] = mapped_column(
        DATETIME, unique=False, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    last_updated: Mapped[datetime.datetime] = mapped_column(
        DATETIME, unique=False, nullable=True, default=datetime.datetime.now(datetime.timezone.utc))

    favorite: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=False)
    was_removed: Mapped[bool] = mapped_column(
        Boolean, unique=False, nullable=False, default=False)

    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tags.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    chapters: Mapped["Chapter"] = relationship("Chapter", back_populates="work",
                            cascade="all, delete-orphan", lazy="subquery")
    update_messages: Mapped["UpdateMessage"] = relationship(
        "UpdateMessage", back_populates="work", cascade="all, delete-orphan", lazy=True)

    def get_not_removed_chapters(self) -> list[Chapter]:
        return [chapter for chapter in self.chapters if not chapter.was_removed]

    def get_removed_chapters(self) -> list[Chapter]:
        return [chapter for chapter in self.chapters if chapter.was_removed]

    def get_completed_chapters(self) -> list[Chapter]:
        return [chapter for chapter in self.chapters if chapter.completed]

    def all_chapters_completed(self) -> bool:
        return all([chapter.completed for chapter in self.chapters])


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)

    works: Mapped[list["Work"]] = relationship(
        "Work", back_populates="tag", cascade="all, delete-orphan", lazy=False)
    owner_id: Mapped[list["Work"]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="tags")

    def get_favorite_works(self):
        return [work for work in self.works if work.favorite]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(
        String(128), unique=False, nullable=False)

    tags: Mapped[list["Tag"]] = relationship(
        "Tag", back_populates="owner", cascade="all, delete-orphan", lazy=False)
    works: Mapped[list["Work"]] = relationship(
        "Work", back_populates="owner", cascade="all, delete-orphan", lazy=False)

    def get_favorite_works(self):
        return [work for work in self.works if work.favorite]


class UpdateMessage(Base):
    __tablename__ = "update_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chapter_name: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    type: Mapped[str] = mapped_column(String, unique=False, nullable=False,
                         default=UpdateMessagesConsts.MESSAGE_ADDED_TYPE)
    date: Mapped[datetime.datetime] = mapped_column(DATETIME, unique=False,
                         nullable=False, default=datetime.datetime.now(tz=datetime.timezone.utc))

    work_id: Mapped[int] = mapped_column(Integer, ForeignKey("works.id"), nullable=False)

    def get_message_by_type(self) -> str | None:
        message = None

        if self.type == UpdateMessagesConsts.MESSAGE_ADDED_TYPE:
            message = f"Added '{self.chapter_name}' to"

        elif self.type == UpdateMessagesConsts.MESSAGE_REMOVED_TYPE:
            message = f"Removed '{self.chapter_name}' from"

        return message
