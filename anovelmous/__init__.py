from flask import Flask, url_for, redirect, g, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import flask_restless

import datetime

app = Flask(__name__)
app.config.from_object("config")
app.config.from_envvar("ANOVELMOUS_SETTINGS")
db = SQLAlchemy(app)


class Novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name=None):
        self.name = name
        self.created_at = datetime.datetime.utcnow()


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False)
    novel = db.relationship('Novel', backref=db.backref('chapters', lazy='dynamic'))

    def __init__(self, name=None, novel_id=None):
        self.name = name
        self.created_at = datetime.datetime.utcnow()
        self.novel_id = novel_id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True, nullable=False)
    first_name = db.Column(db.Unicode, nullable=False)
    last_name = db.Column(db.Unicode, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Unicode, nullable=False)
    ordinal = db.Column(db.Integer, nullable=False)
    selected = db.Column(db.Boolean, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    chapter = db.relationship('Chapter', backref=db.backref('content', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('votes', lazy='dynamic'))


db.create_all()


@app.route('/')
def index():

    novels = Novel.query.all()
    current_novel = novels[-1] if novels else None
    return render_template('index.html', current_novel=current_novel)


@app.route('/browse')
def browse_novels():
    novels = Novel.query.all()
    return render_template('browse_novels.html', novels=novels)


@app.route('/read-novel/<novel_name>')
def read_novel(novel_name):
    novel = Novel.query.filter_by(name=novel_name).first()
    most_recent_chapter = Chapter.query.filter_by(novel_id=novel.id)\
        .order_by(Chapter.created_at).first()
    if not most_recent_chapter:
        abort(404)
    chapter_content = Vote.query.filter_by(chapter_id=most_recent_chapter.id).all()

    template_variables = {
        'novel': novel,
        'most_recent_chapter': most_recent_chapter,
        'chapter_content': chapter_content
    }
    return render_template('read_novel.html', **template_variables)


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Novel, methods=['GET', 'POST'])
manager.create_api(Chapter, methods=['GET', 'POST'])
manager.create_api(User, primary_key='username', exclude_columns=['password'])
manager.create_api(Vote, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run()