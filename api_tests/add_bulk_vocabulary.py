import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('host')
args = parser.parse_args()

if __name__ == '__main__':
    with open('google-10000-english/google-10000-english.txt') as f:
        words = f.read().splitlines()

    url = 'http://{host}/api/bulk-add-to-vocabulary'.format(host=args.host)
    requests.post(url, json={'words': words})