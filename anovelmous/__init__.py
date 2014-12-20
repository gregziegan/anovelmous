from flask import Flask, url_for, redirect, g, abort, render_template
import flask_restless
from models import db, Novel, Chapter, Vote, StoryToken, User

app = Flask(__name__)
app.config.from_object("config")
app.config.from_envvar("ANOVELMOUS_SETTINGS")


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
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()