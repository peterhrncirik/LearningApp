from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import Video, Learning
from accounts.models import CustomUser
from .forms import TimestampsForm, VideoLinkForm

import re
import time

# VIDEO
from pytube import YouTube
from .youtube import main

# DEBUG
from pprint import pprint
# assert something
# assert False, 'This is forbidden'


@login_required
def learning(request, id):
    
    TimestampsFormSet = formset_factory(TimestampsForm, extra=0)
    formset = TimestampsFormSet()
 
    if request.method == 'POST':
        
        User = CustomUser.objects.get(id=id)
        video_id = request.POST.get('video_id')

        return render(request, "learning/learning.html", {'video_id': video_id, 'formset': formset})
    
        
    
@login_required
def process_timestamps(request, id, video_id):
    
    TimestampsFormSet = formset_factory(TimestampsForm)
    marked_timestamps = []
    
    if request.method == 'POST':
        
        form = TimestampsFormSet(request.POST)

        if form.has_changed() and form.is_valid():
            
            #TODO: Insert new Learning session into DB
            
            # Start processing video
            timestamps = form.cleaned_data
            
            # Maybe I can directly here produce output for each input
            for row in timestamps:
                marked_timestamps.append([row['start'], row['end']])

            print('MARKED: ', marked_timestamps)
            
            # Start processing video > download > timestamps > cut captions / cut audio
            # video = YouTube(f'https://www.youtube.com/{video_id}')
            print('STARTING PROCESSING VIDEO.................')
            main.process_video(link=f'https://www.youtube.com/{video_id}', id=video_id, timestamps=marked_timestamps)

            return HttpResponse('CORRECT FORM!')
        else:
            return render(request, "learning/partials/form.html", {'video_id': video_id, 'formset': form})
        

