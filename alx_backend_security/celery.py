import os
from celery import celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')

app = Celery('alx_backend_security')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# connection to rabbitmq tends to fail on initial startup. this solves that
app.conf.broker_connection_retry_on_startup = True

#Celery will read the tasks in'tasks.py' from all registered Django apps.
app.autodiscover_tasks()
