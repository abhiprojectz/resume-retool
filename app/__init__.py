import os
from celery import Celery

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aicoach.settings')

app = Celery('app')

# load task modules from all registered Django app configs
app.autodiscover_tasks()