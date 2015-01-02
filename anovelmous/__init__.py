from flask import Flask, url_for, redirect, g, abort, render_template, request, jsonify
import flask_restless
from models import db, Novel, Chapter, Vote, NovelToken, User, Token
import selection
from grammar import GrammarFilter
import utils
import random
import pkg_resources

VERSION = pkg_resources.require('anovelmous')[0].version

app = Flask(__name__)
app.config.from_envvar("ANOVELMOUS_SETTINGS")


@app.before_first_request
def initialize_database():
    if not app.debug:
        db.init_app(app)
    db.create_all()
    most_recent_chapter_id = Chapter.query.order_by('-id').first().id
    gf = GrammarFilter(current_chapter_id=most_recent_chapter_id)
    g.grammar_filter = gf



@app.route('/')
def index():
    current_novel = Novel.query.order_by('-id').first()
    current_chapter = Chapter.query.order_by('-id').first()
    current_chapter_tokens = []
    novel_chapters = Chapter.query.order_by('id').all()
    if current_chapter:
        current_chapter_tokens = NovelToken.query.filter_by(chapter_id=current_chapter.id).order_by('ordinal').all()

    full_vocabulary = zip(*list(Token.query.with_entities(Token.content)))[0]
    template_variables = {
        'current_novel': current_novel,
        'novel_chapters': novel_chapters,
        'current_chapter_tokens': current_chapter_tokens,
        'full_vocabulary': full_vocabulary
    }
    return render_template('index.html', **template_variables)


@app.route('/novel/<int:novel_id>/vote', methods=['POST'])
def vote(novel_id):
    token = request.form['token']
    current_chapter = Chapter.query.filter_by(novel_id=novel_id).order_by('-id').first()
    candidate_ordinal = utils.get_candidate_ordinal(current_chapter.id)

    new_novel_token = NovelToken(token=token, ordinal=candidate_ordinal, chapter_id=current_chapter.id)
    db.session.add(new_novel_token)
    db.session.commit()
    return jsonify(message="Successfully voted!")


def get_many_tokens_postprocessor(result=None, search_params=None, **kwargs):
    """Accepts two arguments, `result`, which is the dictionary
    representation of the JSON response which will be returned to the
    client, and `search_params`, which is a dictionary containing the
    search parameters for the request (that produced the specified
    `result`).

    """
    if search_params.get('grammatically_correct'):
        del result['objects']
        result['total_pages'] = 1

        tokens = g.grammar_filter.get_grammatically_correct_vocabulary_subset()
        result['num_results'] = len(tokens)
        utils.substitute_bit_stream(result, tokens)


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Novel, methods=['GET', 'POST'])
manager.create_api(Chapter, methods=['GET', 'POST'], exclude_columns=['content'])
manager.create_api(User, primary_key='username', exclude_columns=['is_active', 'password'], methods=['GET', 'POST'])
manager.create_api(Vote, methods=['GET', 'POST'])
manager.create_api(Token, methods=['GET', 'POST'], exclude_columns=['created_at', 'index'],
                   postprocessors={'GET_MANY': [get_many_tokens_postprocessor]})
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


@app.route('/api/metadata')
def get_api_metadata():
    return jsonify({'version': VERSION})


if __name__ == '__main__':
    if app.debug:
        db.init_app(app)
    app.run()