from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Video(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    output_size = models.IntegerField(default=0)
    
    #TODO: __str__