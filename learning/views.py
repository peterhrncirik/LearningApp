from django.shortcuts import render, redirect, HttpResponse
from django.forms import formset_factory
from .forms import TimestampsForm, VideoLinkForm, TimestampsFormSetHelper
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re


def learning(request):
    
    TimestampsFormSet = formset_factory(TimestampsForm, extra=0)
    formset = TimestampsFormSet()

    
    # form-n-start
    # form-n-end
    
    if request.method == 'POST':
        marked = []
        print('-----------------------------------------------------')
        print(request.POST)
        print('-----------------------------------------------------')
        
        form = TimestampsFormSet(request.POST)
        if form.is_valid():
            print('VALID')
        else:
            print('INVALID')
        
        
        form = TimestampsFormSet(request.POST)
        if form.has_changed() and form.is_valid():
            timestamps = form.cleaned_data
            print(timestamps)
            for _ in timestamps:
                marked.append([_['start'], _['end']])
                
        else:
            print('-------------------') 
            print('Fill the form first')
    
    url_form = VideoLinkForm()

    
    return render(request, "learning/learning.html", {'url_form': url_form, 'formset': formset})
        

def get_video(request):
    
    validator = URLValidator()
    link = request.GET.get('link')

    try:
        validator(link)
        match = re.search(r"/watch\?v=([^&]*)", link)
        id = match.group(1)
        return render(request, 'learning/partials/video.html', {'link': id})
    except ValidationError:
        return HttpResponse('Please insert a youtube video :)')
    
        

