from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_member = models.BooleanField(default=False)
    is_unlimited = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class StripeCustomer(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    
    
    
    
    
    
    