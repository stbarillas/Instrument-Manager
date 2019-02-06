import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# This line allows you to use celery > 4.0 with Win 10 although Win 10 is not officially supported
# If you get an error when calling .delay, try commenting it out
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

# Sets project and broker for celery execution
app = Celery('mysite', broker='amqp://guest@localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')

#discovers modules, particularly in tasks.py
app.autodiscover_tasks()