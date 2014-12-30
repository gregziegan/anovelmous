from celery import Celery
from celery.schedules import crontab

from selection import select_new_novel_token
from utils import get_most_recent_votes


app = Celery('tasks', backend='redis://localhost', broker='amqp://guest@localhost//')

SELECT_STORY_TOKEN_SCHEDULE = {
    # Executes every ten minutes
    'select_story_token': {
        'task': 'tasks.select_story_token',
        'schedule': crontab(minute='*/10'),
        'args': (get_most_recent_votes()),
    },
}


@app.task
def create_story_token(word_counts):
    new_story_token = select_new_novel_token(word_counts)
    return new_story_token