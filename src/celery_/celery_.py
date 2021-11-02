from celery import Celery
from src.config.settings import (
    CELERY_APP_NAME, 
    CELERY_BROKER, 
    CELERY_BACKEND, 
    CELERY_INCLUDES
)


app = Celery(
    CELERY_APP_NAME, 
    broker=CELERY_BROKER, 
    backend=CELERY_BACKEND,
    include=CELERY_INCLUDES
)
