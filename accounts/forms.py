from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from allauth.account.forms import SignupForm
 
# Language options
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
  
class SimpleSignupForm(SignupForm):
    language = forms.ChoiceField(choices=LANGUAGES, label='Language I am learning', help_text='1 Language/Basic Account')
    # language = forms.MultipleChoiceField(choices=LANGUAGES, label='Language I am learning', help_text='1 Language/Basic Account')

    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.language = self.cleaned_data['language']
        user.save()
        return user  

class LanguagesForm(forms.ModelForm):
    languages = forms.ChoiceField(choices=LANGUAGES, label='Change language', widget=forms.Select(attrs={'class':'form-select'}))

    class Meta:
        model = CustomUser
        fields = ['languages']


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):

        model = CustomUser
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)