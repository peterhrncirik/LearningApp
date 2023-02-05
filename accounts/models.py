from django.contrib.auth.models import AbstractUser
from django.db import models

# Language options
LANGUAGES = (
    ('de', 'German'),
    ('eng', 'English'),
    ('jap', 'Japanase'),
    ('rus', 'Russian'),
    ('chi', 'Chinese'),
    ('spa', 'Spanish'),
    ('ita', 'Italian'),
    ('por', 'Portuguese'),
    ('fr', 'French'),
    ('kor', 'Korean'),
)

class CustomUser(AbstractUser):
    is_member = models.BooleanField(default=False)
    is_unlimited = models.BooleanField(default=False)
    language = models.CharField(max_length=40, choices=LANGUAGES, null=True, blank=True)
    current_videos_month = models.IntegerField(default=0)
    videos_monthly_limit = models.BooleanField(default=False)
    
    #TODO: languages for premium users

    def __str__(self):
        return self.email


class StripeCustomer(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
    
    
    
    
    
    
    