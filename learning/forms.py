from django import forms
from django.forms import formset_factory
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Div, HTML, Fieldset
from crispy_bootstrap5.bootstrap5 import FloatingField

class VideoLinkForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['link'].label = "Paste link to your video here"
        self.helper.layout = Layout(FloatingField("link"))

    link = forms.URLField(
                    widget=forms.URLInput(attrs={
                        'placeholder': 'Link to video',
                        'hx-indicator': '#spinner',
                        'name': 'link',
                        'id': 'link',
                        'hx-post': reverse_lazy('learning:load_video'),
                        'hx-target': '#main',
                        'hx-trigger': 'keyup changed delay:500ms',
                        # 'hx-swap': 'outerhtml',
                    }),
                    required=False)
    
    

class TimestampsForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['start'].label = "From"
        self.fields['end'].label = "To"

    
    start =  forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'), initial='00:00:00', input_formats=['%H:%M:%S'])

    end =  forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'), initial='00:00:00', input_formats=['%H:%M:%S'])
    


        

        