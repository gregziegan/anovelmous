from models import NovelToken, FormattedNovelToken, db
from sqlalchemy import desc
import string


def update_formatted_novel_tokens(novel_token, quote_punctuation=None):
    prev_formatted_novel_token = FormattedNovelToken.query.order_by(desc(FormattedNovelToken.ordinal)).first()

    if not prev_formatted_novel_token:
        create_new_formatted_novel_token(novel_token, first_in_chapter=True)
    elif novel_token.token not in string.punctuation:
        if prev_formatted_novel_token == '"':
            update_previous_formatted_novel_token(novel_token, prev_formatted_novel_token)
        else:
            create_new_formatted_novel_token(novel_token)
    elif novel_token.token in string.punctuation and quote_punctuation != 'RIGHT':
        update_previous_formatted_novel_token(novel_token, prev_formatted_novel_token)
    elif quote_punctuation == 'RIGHT':
        create_new_formatted_novel_token(novel_token)


def create_new_formatted_novel_token(novel_token, first_in_chapter=False):
    ordinal = 0 if first_in_chapter else novel_token.ordinal + 1
    new_formatted_novel_token = FormattedNovelToken(
        token=novel_token.token,
        ordinal=ordinal,
        chapter_id=novel_token.chapter_id
    )
    db.session.add(new_formatted_novel_token)
    db.session.commit()


def update_previous_formatted_novel_token(novel_token, prev_formatted_novel_token):
    prev_formatted_novel_token.token += novel_token.token
    db.session.add(prev_formatted_novel_token)
    db.session.commit()
