from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy_utils import ArrowType
from flask_user import UserMixin
import string
import arrow

db = SQLAlchemy()

LONGEST_ENGLISH_WORD_LENGTH = 28
MAX_PUNCTUATION_LENGTH = 7


class Novel(db.Model):
    """
    A model consisting of chapters of dynamic content.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, unique=True, nullable=False)
    created_at = db.Column(ArrowType, nullable=False)

    def __init__(self, title):
        self.title = title
        self.created_at = arrow.utcnow()


class Chapter(db.Model):
    """
    A model consisting of many tokens.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)
    created_at = db.Column(ArrowType, nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False)
    novel = db.relationship('Novel', backref=db.backref('chapters', lazy='dynamic'))

    def __init__(self, title, novel_id):
        self.title = title
        self.created_at = arrow.utcnow()
        self.novel_id = novel_id


class Token(db.Model):
    """
    One of the allowed tokens (word or punctuation) for producing a NovelToken.
    The entire collection is the user vocabulary.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Unicode(LONGEST_ENGLISH_WORD_LENGTH), unique=True, nullable=False)
    is_punctuation = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(ArrowType, nullable=False)

    def __init__(self, content):
        self.content = content
        self.is_punctuation = True if content in string.punctuation else False
        self.created_at = arrow.utcnow()

    def __str__(self):
        return self.content


class NovelToken(db.Model):
    """
    A token tied to a Novel's chapter.
    """
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Unicode(LONGEST_ENGLISH_WORD_LENGTH), db.ForeignKey('token.content'), nullable=False)
    ordinal = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    created_at = db.Column(ArrowType, nullable=False)

    def __init__(self, token, ordinal, chapter_id):
        self.token = token
        self.ordinal = ordinal
        self.chapter_id = chapter_id
        self.created_at = arrow.utcnow()

    def __str__(self):
        return self.token


class FormattedNovelToken(db.Model):
    """
    A token concatenated with surrounding punctuation. This allows for queries to return a space delimited, formatted
    chapter text.
    """
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Unicode(LONGEST_ENGLISH_WORD_LENGTH + MAX_PUNCTUATION_LENGTH), nullable=False)
    ordinal = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    chapter = db.relationship('Chapter', backref=db.backref('content', lazy='dynamic'))
    created_at = db.Column(ArrowType, nullable=False)

    def __init__(self, token, ordinal, chapter_id):
        self.token = token
        self.ordinal = ordinal
        self.chapter_id = chapter_id
        self.created_at = arrow.utcnow()

    def __str__(self):
        return self.token


class Vote(db.Model):
    """
    A model used to cast a vote for a new NovelToken. The most popular vote during the voting window will determine the
    next NovelToken.
    """
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Unicode, nullable=False)
    is_punctuation = db.Column(db.Boolean, nullable=False)
    ordinal = db.Column(db.Integer, nullable=False)
    selected = db.Column(db.Boolean, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    username = db.Column(db.Unicode, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(ArrowType, nullable=False)
    ForeignKeyConstraint(['user_id', 'username'], ['user.id', 'user.username'])

    def __init__(self, token, is_punctuation, ordinal, selected, chapter_id, username, user_id):
        self.token = token
        self.is_punctuation = is_punctuation
        self.ordinal = ordinal
        self.selected = selected
        self.chapter_id = chapter_id
        self.username = username
        self.user_id = user_id
        self.created_at = arrow.utcnow()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Email Info
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(ArrowType)

    # User Info
    is_active = db.Column(db.Boolean, nullable=False, server_default='0')
    created_at = db.Column(ArrowType, nullable=False)

    # Relationships
    user_auth = db.relationship('UserAuth', uselist=False)
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, is_active=True):
        self.email = email
        self.is_active = is_active
        self.created_at = arrow.utcnow()


class UserAuth(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    # User Auth Info
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    is_active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # Relationships
    user = db.relationship('User', uselist=False)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))