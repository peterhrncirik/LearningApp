from celery import shared_task
from .models import CustomUser

@shared_task(name='reset_videos')
def reset_videos():
    CustomUser.objects.all().update(current_videos_month=0, videos_monthly_limit=False)

