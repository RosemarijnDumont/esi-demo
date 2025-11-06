
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "financial_export_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_track_started=True, # Track STARTED state
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

# Auto-discover tasks in 'app.services'
# This assumes your tasks are defined in modules under app.services
celery_app.autodiscover_tasks(['app.services'])

