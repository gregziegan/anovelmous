from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint

import datetime

db = SQLAlchemy()


class Novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name):
        self.name = name
        self.created_at = datetime.datetime.utcnow()


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False)
    novel = db.relationship('Novel', backref=db.backref('chapters', lazy='dynamic'))

    def __init__(self, name, novel_id):
        self.name = name
        self.created_at = datetime.datetime.utcnow()
        self.novel_id = novel_id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, primary_key=True)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    """__table_args__ = (
        UniqueConstraint("id", "username"),
    )"""

    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password = password
        self.is_active = is_active
        self.created_at = datetime.datetime.utcnow()


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Unicode, nullable=False)
    is_punctuation = db.Column(db.Boolean ,nullable=False)
    ordinal = db.Column(db.Integer, nullable=False)
    selected = db.Column(db.Boolean, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    username = db.Column(db.Unicode, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    ForeignKeyConstraint(['user_id', 'username'], ['user.id', 'user.username'])

    def __init__(self, token, is_punctuation, ordinal, selected, chapter_id, username, user_id):
        self.token = token
        self.is_punctuation = is_punctuation
        self.ordinal = ordinal
        self.selected = selected
        self.chapter_id = chapter_id
        self.username = username
        self.user_id = user_id
        self.created_at = datetime.datetime.utcnow()


class StoryToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Unicode, nullable=False)
    is_punctuation = db.Column(db.Boolean, nullable=False)
    ordinal = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    chapter = db.relationship('Chapter', backref=db.backref('content', lazy='dynamic'))
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, is_punctuation, ordinal, chapter_id):
        self.token = token
        self.is_punctuation = is_punctuation
        self.ordinal = ordinal
        self.chapter_id = chapter_id
        self.created_at = datetime.datetime.utcnow()