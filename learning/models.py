from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Video(models.Model):
    
    video_id = models.CharField(max_length=200)
    
class Learning(models.Model):
    
    user = models.ForeignKey(get_user_model(), related_name='user', on_delete=models.CASCADE)
    video_id = models.CharField(max_length=200)
    # created = models.DateTimeField(auto_now_add=True)