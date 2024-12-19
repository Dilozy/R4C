import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'R4C.settings')
app = Celery('orders')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
