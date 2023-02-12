from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from accounts.models import CustomUser


class VideoLinkForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse_lazy('pages:start')
        self.fields['link'].label = "Paste link to your video here"
        # self.fields["languages"] = forms.ChoiceField(choices=choices)
        # self.fields['languages'].label = "Language"
        self.helper.layout = Layout(Field('l'), FloatingField("link"),)
        
    link = forms.URLField(
                    widget=forms.URLInput(attrs={
                        'hx-indicator': '#spinner',
                        'name': 'link',
                        'id': 'link',
                        'hx-post': reverse_lazy('pages:start'),
                        'hx-target': '#main',
                        'hx-trigger': 'keyup changed delay:500ms',
                        'hx-swap': 'outerhtml',
                    }),
                    required=False)
    
    # languages = forms.ChoiceField(label='Select Language')

class ContactUsForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_action = reverse_lazy('pages:start')
        self.fields['sender'].label = "Your E-Mail Address"
        self.fields['message'].label = "Your Message"
        self.helper.layout = Layout(
            FloatingField("sender"), 
            Field('message'),
            Submit('Send Message', 'Send Message', css_class='btn btn-success'),
            )
    
    sender = forms.EmailField(label='Your E-Mail')    
    message = forms.CharField(widget=forms.Textarea)    
    