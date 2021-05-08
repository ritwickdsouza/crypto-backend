from celery.schedules import crontab

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"


CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "core.tasks.sample_task",
        "schedule": crontab(minute="*/1"),
    },
}
