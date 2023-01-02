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

    #TODO: Check for duplicate URLValidation
    link = forms.URLField(
                    widget=forms.URLInput(attrs={
                        'placeholder': 'Link to video',
                        'hx-indicator': '#indicator',
                        'name': 'link',
                        'id': 'link',
                        'hx-get': reverse_lazy('learning:load_video'),
                        'hx-target': '#main',
                        'hx-trigger': 'keyup',
                    }),
                    required=False)
    
    # I can use regex field to accept only 00:00:00 format
    

class TimestampsForm(forms.Form):
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.fields['start'].label = "From"
    #     self.fields['end'].label = "To"

    
    # start = forms.CharField(
    #                 max_length=100,
    #                 widget=forms.TextInput(attrs={
    #                     'placeholder': '00:00:00',
    #                 }),
    #                 required=True)
    start =  forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'), initial='00:00:00', input_formats=['%H:%M:%S'])
    # end = forms.CharField(
    #                 max_length=100,
    #                 widget=forms.TextInput(attrs={
    #                     'placeholder': '00:00:00',
    #                 }),
    #                 required=True)
    end =  forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'), initial='00:00:00', input_formats=['%H:%M:%S'])
    

class TimestampsFormSetHelper(FormHelper):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.template = 'learning/partials/formset.html'
        self.layout = Layout(
            'start',
            'end',
        )
        # self.form_id = 'timestamps'
        # form.helper.form_action = reverse('url_name', args=[event.id])
        # form.helper.form_action = reverse('url_name', kwargs={'book_id': book.id})
        # self.add_input(Submit('submit', 'Save', css_class='btn btn-success'))
        # self.add_input(Button('add', 'Add more', css_class='btn btn-danger'))
        

        