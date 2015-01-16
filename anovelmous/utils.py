from models import NovelToken, Token
import time
import requests
import os
import string
import random


def substitute_bit_stream(result, available_tokens):
    available_token_indices = [token.id for token in available_tokens]
    bit_stream = []
    last_index = 0
    for token_index in available_token_indices:
        num_zeroes = token_index - last_index - 1
        zeroes = ['0' for i in range(num_zeroes)]
        bit_stream.extend(zeroes)
        bit_stream.append('1')
        last_index = token_index

    last_available_token_index = available_token_indices[-1]
    trailing_zeroes = ['0' for i in range(result['num_results'] - last_available_token_index)]
    bit_stream.extend(trailing_zeroes)
    bit_stream = ''.join(bit_stream)
    result['bit_stream'] = bit_stream


def get_candidate_ordinal(chapter_id):
    current_novel_token = NovelToken.query.filter_by(chapter_id=chapter_id).order_by('-ordinal').first()
    return current_novel_token.ordinal + 1


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f seconds' % (f.func_name, (time2-time1))
        # TODO: Eventually log this timing decorator
        return ret
    return wrap


def is_allowed_punctuation(symbol):
    if symbol in '!"$%&\'(),.:;?':
        return True
    return False


def add_initial_vocabulary(host, word_cap=None):
    with open(os.path.join(os.path.dirname(__file__), 'data/google-10000-english/google-10000-english.txt')) as f:
        vocabulary = f.read().splitlines()

    if word_cap:
        random.shuffle(vocabulary)
        vocabulary = vocabulary[:word_cap]

    for symbol in string.punctuation:
        if is_allowed_punctuation(symbol):
            vocabulary.append(symbol)

    url = 'http://{host}/api/bulk-add-to-vocabulary'.format(host=host)
    requests.post(url, json={'words': vocabulary})


def is_valid_vocabulary_word(token):
    valid_token = Token.query.filter_by(content=token).first()
    if valid_token:
        return True
    return False