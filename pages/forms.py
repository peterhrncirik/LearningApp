from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Div, HTML, Fieldset
from crispy_bootstrap5.bootstrap5 import FloatingField


class VideoLinkForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse_lazy('pages:start')
        self.fields['link'].label = "Paste link to your video here"
        self.helper.layout = Layout(FloatingField("link"))

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
    

    
    