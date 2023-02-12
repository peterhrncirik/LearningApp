from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Language options
LANGUAGES = (
    ('de', 'German'),
    ('en', 'English'),
    ('zh-HK', 'Chinese'),
    ('pt-PT', 'Portuguese'),
    #TODO: Add spanish
    # ('zh-HK', 'Chinese (Hong Kong)'),
    # ('zh-TW', 'Chinese (Taiwan)'),
    # ('en-GB', 'English (United Kingdom)'),
    ('fr-FR', 'French'),
    # ('fr-FR', 'French (France)'),
    # ('fr-CA', 'French (Canada)'),
    ('ja', 'Japanese'),
    # ('pt-BR', 'Portuguese (Brazil)'),
    # ('pt-PT', 'Portuguese (Portugal)'),
    ('ru', 'Russian'),
    ('it', 'Italian'),
)


class CustomUser(AbstractUser):
    is_member = models.BooleanField(default=False)
    is_unlimited = models.BooleanField(default=False)
    language = models.CharField(max_length=40, choices=LANGUAGES, null=True, blank=True)
    # language = ArrayField(models.CharField(choices=LANGUAGES, max_length=15, blank=True), default=list, blank=True)
    current_videos_month = models.IntegerField(default=0)
    videos_monthly_limit = models.BooleanField(default=False)
    
    #TODO: languages for premium users
    
    def get_language(self):
        """
        Return name of language based on its code
        """
        langs = []
        for _ in self.language:
            langs.append(dict(LANGUAGES)[_])
        return langs

    def __str__(self):
        return self.email


class StripeCustomer(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


    
    
    
    
    
    
    