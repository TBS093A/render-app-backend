import importlib
import sys
import os

from celery import Celery
from celery.signals import worker_init
from work.settings import (
    BPY_DEFAULT_RENDER_FILE,
    BPY_RENDER_DIR,
    BPY_DEVICE,
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'work.settings')

app = Celery('rendering')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
