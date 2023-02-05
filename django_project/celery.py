import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Reset User Videos Every Month
app.conf.beat_schedule = {
    'reset_videos': {
        'task': 'reset_videos',
        'schedule': crontab(0, 0, day_of_month='1'),
    },
}

app.conf.timezone = 'UTC'
 