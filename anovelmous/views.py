from anovelmous import app
from flask import render_template, request, jsonify, g
from grammar import GrammarFilter
from models import Novel, Chapter, NovelToken, Token, db
import utils


@app.before_first_request
def initialize_database():
    most_recent_chapter = Chapter.query.order_by('-id').first()
    if most_recent_chapter:
        most_recent_chapter_id = most_recent_chapter.id
    else:
        most_recent_chapter_id = 1
    gf = GrammarFilter(current_chapter_id=most_recent_chapter_id)
    g.grammar_filter = gf


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/novel/<int:novel_id>/vote', methods=['POST'])
def vote(novel_id):
    token = request.form['token']
    current_chapter = Chapter.query.filter_by(novel_id=novel_id).order_by('-id').first()
    candidate_ordinal = utils.get_candidate_ordinal(current_chapter.id)

    new_novel_token = NovelToken(token=token, ordinal=candidate_ordinal, chapter_id=current_chapter.id)
    db.session.add(new_novel_token)
    db.session.commit()
    return jsonify(message="Successfully voted!")
