from models import NovelToken, Token
import nltk
from nltk.corpus import brown
from utils import timing
from sqlalchemy import desc


class GrammarFilter(object):
    """
    An object used to filter out all uncommon word sequences in a given chapter.
    """

    def __init__(self, current_chapter_id, vocabulary=None):
        self.chapter_id = current_chapter_id
        self.vocabulary = vocabulary if vocabulary else Token.query.all()
        self.corpus = brown.words(categories=['fiction'])
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    @staticmethod
    @timing
    def is_occurring_combination(corpus, candidate_token, preceding_token):
        """
        A Naive algorithm that checks whether a preceding token occurs in a given text corpus.
        :param candidate_token:
        :param preceding_token:
        :return:
        """
        match_detected = False

        for sentence in corpus:
            preceding_token_encountered = False
            for word in sentence[1:]:
                if word == candidate_token and preceding_token_encountered:
                    match_detected = True
                    break

                if word == preceding_token:
                    preceding_token_encountered = True
                else:
                    preceding_token_encountered = False
            if match_detected:
                break

        return match_detected

    def get_grammatically_correct_vocabulary_subset(self):
        """
        Returns a subset of a given vocabulary based on whether its tokens are "grammatically correct" following the
        latest words in the chapter.
        """
        preceding_tokens = self.get_preceding_tokens(num_of_preceding_tokens=1)
        if preceding_tokens:
            preceding_token = preceding_tokens[0]
            return [token for token in self.vocabulary
                    if self.is_occurring_combination(self.corpus, token.content, preceding_token)]
        else:
            return self.vocabulary

    def get_preceding_tokens(self, num_of_preceding_tokens=1):
        chapter_tokens = NovelToken.query.filter_by(chapter_id=self.chapter_id).order_by(NovelToken.ordinal)
        chapter_token_strings = zip(*list(chapter_tokens.with_entities(NovelToken.token)))[0]
        chapter_text = ' '.join(chapter_token_strings)
        last_sentence = self.tokenizer.tokenize(chapter_text)[-1]

        num_tokens = len(last_sentence.split(' '))
        last_sentence_tokens = NovelToken.query.filter_by(chapter_id=self.chapter_id)\
            .order_by(desc(NovelToken.ordinal))[:num_tokens]

        preceding_tokens = last_sentence_tokens[:num_of_preceding_tokens]
        return preceding_tokens
