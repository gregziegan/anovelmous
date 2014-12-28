from flask import Flask, url_for, redirect, g, abort, render_template, request, jsonify
import flask_restless
from models import db, Novel, Chapter, Vote, NovelToken, User, Token
import utils
import random

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
    novel_chapters = Chapter.query.order_by('id').all()
    if current_chapter:
        current_chapter_tokens = NovelToken.query.filter_by(chapter_id=current_chapter.id).all()
    return render_template('index.html', current_novel=current_novel, novel_chapters=novel_chapters,
                           current_chapter_tokens=current_chapter_tokens)


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
    chapter_content = NovelToken.query.filter_by(chapter_id=most_recent_chapter.id).all()

    template_variables = {
        'novel': novel,
        'most_recent_chapter': most_recent_chapter,
        'chapter_content': chapter_content
    }
    return render_template('read_novel.html', **template_variables)


def get_tokens_postprocessor(result=None, search_params=None, **kw):
    """Accepts two arguments, `result`, which is the dictionary
    representation of the JSON response which will be returned to the
    client, and `search_params`, which is a dictionary containing the
    search parameters for the request (that produced the specified
    `result`).

    """
    if search_params.get('bit_stream'):
        del result['objects']
        tokens = list(Token.query.all())
        random.shuffle(tokens)
        available_tokens = tokens[:100]  # TODO: temporary until grammar is built
        utils.substitute_bit_stream(result, available_tokens)


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Novel, methods=['GET', 'POST'])
manager.create_api(Chapter, methods=['GET', 'POST'])
manager.create_api(User, primary_key='username', exclude_columns=['is_active', 'password'], methods=['GET', 'POST'])
manager.create_api(Vote, methods=['GET', 'POST'])
manager.create_api(Token, methods=['GET', 'POST'], exclude_columns=['created_at', 'index'],
                   postprocessors={'GET_MANY': [get_tokens_postprocessor]})
manager.create_api(NovelToken, methods=['GET', 'POST'], allow_functions=True)


@app.route('/api/bulk-add-to-vocabulary', methods=['POST'])
def add_to_vocabulary():
    words = request.json['words']
    words = [word.lower() for word in words]

    if len(set(words)) != len(words):
        return jsonify({'message': "All words must be unique."})

    for word in words:
        token = Token(word)
        db.session.add(token)

    db.session.commit()
    return jsonify({'message': "All words added successfully."})

if __name__ == '__main__':
    if app.debug:
        db.init_app(app)
    app.run()