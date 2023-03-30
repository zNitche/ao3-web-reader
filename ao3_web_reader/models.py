from ao3_web_reader import db
from flask_login import UserMixin
from datetime import datetime
from ao3_web_reader.consts import UpdateMessagesConsts


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)

    tags = db.relationship("Tag", backref="owner", cascade="all, delete-orphan", lazy=True)
    works = db.relationship("Work", backref="owner", cascade="all, delete-orphan", lazy=True)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)

    works = db.relationship("Work", backref="tag", cascade="all, delete-orphan", lazy=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Work(db.Model):
    __tablename__ = "works"

    id = db.Column(db.Integer, primary_key=True)

    work_id = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String(200), unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)

    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, unique=False, nullable=True, default=datetime.utcnow)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    was_removed = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    chapters = db.relationship("Chapter", backref="work", cascade="all, delete-orphan", lazy=True)
    update_messages = db.relationship("UpdateMessage", backref="work", cascade="all, delete-orphan", lazy=True)


class Chapter(db.Model):
    __tablename__ = "chapters"

    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.String, unique=False, nullable=False)
    chapter_order_id = db.Column(db.Integer, unique=False, nullable=False)

    title = db.Column(db.String(200), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    text = db.Column(db.String, unique=False, nullable=False)

    was_removed = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    work_id = db.Column(db.Integer, db.ForeignKey("works.id"), nullable=False)

    def get_formatted_text(self):
        return self.text.split("\n")

    def get_next_chapter(self):
        prev_chapter = Chapter.query.filter_by(work_id=self.work_id, chapter_order_id=self.chapter_order_id + 1).first()

        return prev_chapter

    def get_prev_chapter(self):
        next_chapter = Chapter.query.filter_by(work_id=self.work_id, chapter_order_id=self.chapter_order_id - 1).first()

        return next_chapter


class UpdateMessage(db.Model):
    __tablename__ = "update_messages"

    id = db.Column(db.Integer, primary_key=True)
    chapter_name = db.Column(db.String, unique=False, nullable=True)
    type = db.Column(db.String, unique=False, nullable=False, default=UpdateMessagesConsts.MESSAGE_ADDED_TYPE)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    work_id = db.Column(db.Integer, db.ForeignKey("works.id"), nullable=False)

    def get_message_by_type(self):
        message = None

        if self.type == UpdateMessagesConsts.MESSAGE_ADDED_TYPE:
            message = f"Added '{ self.chapter_name }' to"

        elif self.type == UpdateMessagesConsts.MESSAGE_REMOVED_TYPE:
            message = f"Removed '{self.chapter_name}' from"

        return message
