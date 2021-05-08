import os

from celery.schedules import crontab


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379')


CELERY_BEAT_SCHEDULE = {
    'update_exchange_rates': {
        'task': 'core.tasks.update_exchange_rates',
        'schedule': crontab(minute='*/60'),
    },
}
