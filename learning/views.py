from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import Video, Learning
from accounts.models import CustomUser
from .forms import TimestampsForm, VideoLinkForm
from django.core.exceptions import ValidationError

import re
import time

# VIDEO
from pytube import YouTube
from .youtube import main

from .tasks import process_video_async

# DEBUG
from pprint import pprint
# assert something
# assert False, 'This is forbidden'


@login_required
def learning(request, id):
    
    TimestampsFormSet = formset_factory(TimestampsForm, extra=0)
    form = TimestampsFormSet()
 
    if request.method == 'POST':
        
        User = CustomUser.objects.get(id=id)
        video_id = request.POST.get('video_id')

        return render(request, "learning/learning.html", {'video_id': video_id, 'formset': form})
    
        
    
@login_required
def process_timestamps(request, id, video_id):
    
    TimestampsFormSet = formset_factory(TimestampsForm)
    marked_timestamps = []
    
    if request.method == 'POST':
        
        form = TimestampsFormSet(request.POST)
        current_user = request.user
        if form.has_changed() and form.is_valid():
            
            #TODO: Daj do template JS na disable enter event
            #TODO: Insert new Learning session into DB
            
            # Start processing video
            timestamps = form.cleaned_data
            
            # Maybe I can directly here produce output for each input
            for row in timestamps:
                
                marked_timestamps.append([row['start'], row['end']])

            print('MARKED: ', marked_timestamps)
            
            # Start processing video 
            print('STARTING PROCESSING VIDEO.................')
            # main.process_video(link=f'https://www.youtube.com/{video_id}', video_id=video_id, user_id=current_user.id, timestamps=marked_timestamps)
            result = process_video_async.delay(link=f'https://www.youtube.com/{video_id}', video_id=video_id, user_id=current_user.id, timestamps=marked_timestamps)
            
            # return HttpResponse('Data downloaded.')
            return render(request, 'learning/progress.html', context={'task_id': result.task_id})
        else:
            return render(request, "learning/learning.html", {'video_id': video_id, 'formset': form})
        

