from flask import Flask, url_for, redirect, g, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import flask_restless

app = Flask(__name__)
app.config.from_object("config")
app.config.from_envvar("ANOVELMOUS_SETTINGS")
db = SQLAlchemy(app)


class Novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'), nullable=False)
    novel = db.relationship('Novel', backref=db.backref('chapters', lazy='dynamic'))


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
    return render_template('index.html')


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Novel)
manager.create_api(Chapter)
manager.create_api(User, primary_key='username', exclude_columns=['password'])
manager.create_api(Vote, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run()