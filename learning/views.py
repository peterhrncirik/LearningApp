import os
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import FileResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import Video
from accounts.models import CustomUser
from .forms import TimestampsForm
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
    
    TimestampsFormSet = formset_factory(TimestampsForm, extra=1, can_delete=True)
    formset = TimestampsFormSet()
    print(formset)
    if request.method == 'POST':
        
        User = CustomUser.objects.get(id=id)
        video_id = request.POST.get('video_id')

        return render(request, "learning/learning.html", {'video_id': video_id, 'formset': formset})
    
        
    
@login_required
def process_timestamps(request, id, video_id):
    
    if not request.user.is_member:
        FORMS_MAX_NUMBER = 5
    elif request.user.is_member and not request.user.is_unlimited:
        FORMS_MAX_NUMBER = 10
    else:
        FORMS_MAX_NUMBER = 100
    
    #TODO: max_num, validate_max = premium future check
    TimestampsFormSet = formset_factory(TimestampsForm, max_num=FORMS_MAX_NUMBER, validate_max=True, min_num=1, validate_min=True, can_delete=True)
    marked_timestamps = []
    
    if request.method == 'POST':
        
        #TODO: Zatial takyto limit check, sem sa to ani nema preco dostat, ale len pre istotu
        if request.user.videos_monthly_limit:
            return redirect('pages:home')
        
        formset = TimestampsFormSet(request.POST)

        if formset.has_changed() and formset.is_valid():
            
            # Update User
            user = CustomUser.objects.get(id=request.user.id)
            user.current_videos_month += 1

            # Check premium limits
            if not user.is_member and user.current_videos_month == 5:
                user.videos_monthly_limit = True
            elif user.is_member and not user.is_unlimited and user.current_videos_month == 10:
                user.videos_monthly_limit = True
            
            user.save()
            
            # Update Video
            #TODO: output_size bude nieco ine / ide to, ale zahrna to aj tie checked na DELETE
            Video.objects.create(user=user, video_id=video_id, output_size=len(formset))
            
            # Start processing video
            timestamps = formset.cleaned_data

            # Maybe I can directly here produce output for each input
            for row in timestamps:
                
                # Skip the ones marked for deletion
                if row['DELETE']:
                    continue

                marked_timestamps.append([row['start'], row['end']])

            print('MARKED: ', marked_timestamps)
            
            # Start processing video 
            print('STARTING PROCESSING VIDEO.................')
            #TODO: Tu som zmenil current_user.id na request.user.id - nemal by byt bug ale just in case
            result = process_video_async.delay(link=f'https://www.youtube.com/{video_id}', video_id=video_id, user_id=request.user.id, timestamps=marked_timestamps)
            
            #TODO: Skus timestamp vacsi ako cele video aky bug to daa
            
            # return HttpResponse('Data downloaded.')
            return render(request, 'learning/progress.html', {'task_id': result.task_id, 'video_id': video_id})
        else:
            return render(request, "learning/learning.html", {'video_id': video_id, 'formset': formset})
    
    #FIXME: Redirect on get here is not the best but avoids bigger bug for now
    return redirect(reverse_lazy('pages:start'))

def download(request, video_id):
    
    zipped_file = open(f'media/video/{video_id}_{request.user.id}/files.zip', 'rb')
    return FileResponse(zipped_file)
    