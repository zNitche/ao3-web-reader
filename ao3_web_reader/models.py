from ao3_web_reader import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)

    works = db.relationship("Work", backref="owner", lazy=True)


class Work(db.Model):
    __tablename__ = "works"

    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, unique=False, nullable=True, default=datetime.utcnow)

    chapters = db.relationship("Chapter", backref="work", lazy=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Chapter(db.Model):
    __tablename__ = "chapters"

    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    work_id = db.Column(db.Integer, db.ForeignKey("works.id"), nullable=False)
    rows = db.relationship("TextRow", backref="chapter", lazy=True)


class TextRow(db.Model):
    __tablename__ = "text_rows"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, unique=False, nullable=True)

    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id"), nullable=False)
