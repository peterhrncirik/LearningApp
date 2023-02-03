from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from allauth.account.forms import SignupForm
 
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
  
class SimpleSignupForm(SignupForm):
    language = forms.ChoiceField(choices=LANGUAGES, label='Language I am learning', help_text='1 Language/Basic Account')

    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.language = self.cleaned_data['language']
        user.save()
        return user  



class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):

        model = CustomUser
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)