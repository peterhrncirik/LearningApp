import re
import time
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .forms import VideoLinkForm
from .video import check_video
from pprint import pprint
from pytube import YouTube


def home(request):
    
    return render(request, 'pages/home.html')

@login_required
def start(request):
    
    form = VideoLinkForm()
    
    if request.method == 'POST':
        
        form = VideoLinkForm(request.POST)
        video_details = {}

        if form.is_valid():
            
            cd = form.cleaned_data
            
            #FIXME: AJAX zacne aj na empty keyUp - fix
            
            # Check if url is correct by searching for ID in the link
            try:
                match = re.search(r"/watch\?v=([^&]*)", cd['link'])
            except:
                return HttpResponse('<p>This doesn\'t look like correct youtube URL.</p>')

            # URL is okay, assign video ID
            id = match.group(1)
            
            try:
                # What if ID is wrong though?
                video = YouTube(cd['link'])
            except:
                return HttpResponse('<p>This doesn\'t look like correct youtube URL.</p>')
            
        
      
            #TODO: check for subtitles and tell them if video is okay and we can continue
            # Check video
            video_is_correct = check_video(cd['link'])
            
            if not video_is_correct:
                return HttpResponse('<p>Looks like this video is not supported :(</p>')
            
            # Load video and get info
            video_details = {
                'title': video.title,
                'thumbnail': video.thumbnail_url
            }
            
            return render(request, 'pages/partials/video.html', {'video_id': id, 'video': video_details, 'link': cd['link']})
        else:
            #FIXME: Bug, ak uz raz nastane tento response check_video() sa nespusta znova + text ostava na stranke a nerefreshuje sa
            return HttpResponse('<p>This doesn\'t look like a correct URL.</p>')

    return render(request, 'pages/start.html', {'form': form})

def about(request):
    pass
