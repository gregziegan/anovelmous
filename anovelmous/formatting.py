from models import NovelToken, FormattedNovelToken, db
from sqlalchemy import desc
import string


def update_formatted_novel_tokens(novel_token, quote_punctuation=None):
    previous_formatted_token = FormattedNovelToken.query.order_by(desc(FormattedNovelToken.ordinal)).first()

    if not previous_formatted_token:
        first_formatted_novel_token = FormattedNovelToken(
            token=novel_token.token,
            ordinal=0,
            chapter_id=novel_token.chapter_id
        )
        db.session.add(first_formatted_novel_token)
        db.session.commit()

    elif novel_token.token not in string.punctuation:
        if previous_formatted_token == '"':
            previous_formatted_token.token += novel_token.token
            db.session.add(previous_formatted_token)
            db.session.commit()
        else:
            new_formatted_novel_token = FormattedNovelToken(
                token=novel_token.token,
                ordinal=previous_formatted_token.ordinal+1,
                chapter_id=novel_token.chapter_id
            )
            db.session.add(new_formatted_novel_token)
            db.session.commit()
    elif quote_punctuation == 'LEFT':
        previous_formatted_token.token += novel_token.token

        db.session.add(previous_formatted_token)
        db.session.commit(previous_formatted_token)
