import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_app.settings")

app = Celery("redis_darsi_drf")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
