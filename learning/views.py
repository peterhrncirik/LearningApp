import os
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import FileResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import Video, Learning
from accounts.models import CustomUser
from .forms import TimestampsForm, VideoLinkForm
from django.core.exceptions import ValidationError

import re
import time
from shutil import make_archive

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
    
    TimestampsFormSet = formset_factory(TimestampsForm, can_delete=True)
    form = TimestampsFormSet()
 
    if request.method == 'POST':
        
        User = CustomUser.objects.get(id=id)
        video_id = request.POST.get('video_id')

        return render(request, "learning/learning.html", {'video_id': video_id, 'formset': form})
    
        
    
@login_required
def process_timestamps(request, id, video_id):
    
    #TODO: max_num, validate_max = premium future check
    TimestampsFormSet = formset_factory(TimestampsForm, max_num=3, validate_max=True, min_num=1, validate_min=True, can_delete=True)
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
                
                # Skip the ones marked for deletion
                if row['DELETE']:
                    continue

                marked_timestamps.append([row['start'], row['end']])

            print('MARKED: ', marked_timestamps)
            
            # Start processing video 
            print('STARTING PROCESSING VIDEO.................')
            result = process_video_async.delay(link=f'https://www.youtube.com/{video_id}', video_id=video_id, user_id=current_user.id, timestamps=marked_timestamps)
            
            #TODO: Skus timestamp vacsi ako cele video aky bug to daa
            
            # return HttpResponse('Data downloaded.')
            return render(request, 'learning/progress.html', {'task_id': result.task_id, 'video_id': video_id})
        else:
            return render(request, "learning/learning.html", {'video_id': video_id, 'formset': form})
    
    #FIXME: Redirect on get here is not the best but avoids bigger bug for now
    return redirect(reverse_lazy('pages:start'))

def download(request, video_id):
    
    zipped_file = open(f'media/video/{video_id}_{request.user.id}/files.zip', 'rb')
    return FileResponse(zipped_file)
    