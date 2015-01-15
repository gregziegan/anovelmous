from models import NovelToken, Token
import nltk
from nltk.corpus import brown
from utils import timing
from sqlalchemy import desc
import numpy as np
import string
import os.path
import json


class GrammarFilter(object):
    """
    An object used to filter out all uncommon word sequences in a given chapter.
    """

    def __init__(self, current_chapter_id, vocabulary=None, corpus=None):
        self.chapter_id = current_chapter_id

        self.vocabulary = vocabulary if vocabulary else Token.query.all()
        self.vocabulary_lookup = {term.content: True for term in self.vocabulary}
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

        corpora_cache_fp = os.path.join(os.path.dirname(__file__), 'data/corpora_cache')
        if not os.path.exists(corpora_cache_fp):
            os.makedirs(corpora_cache_fp)

        full_brown_corpus_file_path = os.path.join(corpora_cache_fp, 'full_brown_corpus.npy')
        full_brown_bigrams_file_path = os.path.join(corpora_cache_fp, 'full_brown_bigrams.json')

        if corpus:
            self.corpus = corpus
            self.bigrams = self.build_vocab_targeted_bigrams()
        elif not corpus \
                and os.path.exists(full_brown_corpus_file_path)\
                and os.path.exists(full_brown_bigrams_file_path):
            self.corpus = np.load(full_brown_corpus_file_path)
            with open(full_brown_bigrams_file_path) as f:
                self.bigrams = json.load(f)
        else:
            brown_text = nltk.Text(word.lower() for word in brown.words())
            self.corpus = np.array(brown_text.tokens)
            self.bigrams = self.build_vocab_targeted_bigrams()
            np.save(full_brown_corpus_file_path, self.corpus)
            with open(full_brown_bigrams_file_path, 'w') as f:
                json.dump(self.bigrams, f)

    @timing
    def build_vocab_targeted_bigrams(self):
        vocab_occurrences = {vocab_term.content: {} for vocab_term in self.vocabulary}

        preceding_token = self.corpus[0]
        encountered_punctuation = False
        for token in self.corpus[1:]:
            if token in string.punctuation:
                encountered_punctuation = True
                continue

            if encountered_punctuation:
                preceding_token = token
                encountered_punctuation = False
                continue

            if self.vocabulary_lookup.get(token):
                vocab_occurrences[token][preceding_token] = True

            preceding_token = token

        return vocab_occurrences

    def is_occurring_combination(self, candidate_token, preceding_token):
        return self.bigrams[candidate_token].get(preceding_token)

    def get_grammatically_correct_vocabulary_subset(self):
        """
        Returns a subset of a given vocabulary based on whether its tokens are "grammatically correct" following the
        latest words in the chapter.
        """
        preceding_tokens = self.get_preceding_tokens(num_of_preceding_tokens=1)
        if preceding_tokens:
            preceding_token = preceding_tokens[0]
            return [token for token in self.vocabulary
                    if self.is_occurring_combination(token.content, preceding_token.token)]
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
