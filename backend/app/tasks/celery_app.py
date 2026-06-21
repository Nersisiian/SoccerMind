from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "soccermind",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Регистрируем задачи явно
import app.tasks.fetch_data        # noqa
import app.tasks.train_models      # noqa
import app.tasks.generate_predictions  # noqa

celery_app.conf.beat_schedule = {
    "fetch-live-odds-every-15-min": {
        "task": "app.tasks.fetch_data.fetch_all_sources",
        "schedule": 900.0,
        "options": {"expires": 600},
    },
    "retrain-models-daily": {
        "task": "app.tasks.train_models.retrain_models",
        "schedule": crontab(hour=3, minute=0),  # каждый день в 3 утра
    },
    "generate-predictions-every-6-hours": {
        "task": "app.tasks.generate_predictions.generate_upcoming_predictions",
        "schedule": 21600.0,  # каждые 6 часов
        "options": {"expires": 3600},
    },
}

import app.tasks.load_history  # noqa

import app.tasks.load_history  # noqa
