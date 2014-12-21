from flask import Flask, url_for, redirect, g, abort, render_template
import flask_restless
from models import db, Novel, Chapter, Vote, StoryToken, User

app = Flask(__name__)
app.config.from_envvar("ANOVELMOUS_SETTINGS")

@app.before_first_request
def initialize_database():
    if not app.debug:
        db.init_app(app)
    db.create_all()


@app.route('/')
def index():
    current_novel = Novel.query.order_by('-id').first()
    current_chapter = Chapter.query.order_by('-id').first()
    current_chapter_tokens = []
    if current_chapter:
        current_chapter_tokens = StoryToken.query.filter_by(chapter_id=current_chapter.id).all()
    return render_template('index.html', current_novel=current_novel, current_chapter_tokens=current_chapter_tokens)


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
    chapter_content = StoryToken.query.filter_by(chapter_id=most_recent_chapter.id).all()

    template_variables = {
        'novel': novel,
        'most_recent_chapter': most_recent_chapter,
        'chapter_content': chapter_content
    }
    return render_template('read_novel.html', **template_variables)


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Novel, methods=['GET', 'POST'])
manager.create_api(Chapter, methods=['GET', 'POST'])
manager.create_api(User, primary_key='username', exclude_columns=['is_active', 'password'], methods=['GET', 'POST'])
manager.create_api(Vote, methods=['GET', 'POST'])
manager.create_api(StoryToken, methods=['GET', 'POST'], allow_functions=True)


if __name__ == '__main__':
    if app.debug:
        db.init_app(app)
    app.run()