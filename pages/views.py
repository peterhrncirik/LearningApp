import re
import time
from django.shortcuts import render, redirect, HttpResponse
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
      
            #TODO: check for subtitles and tell them if video is okay and we can continue
            # Check video
            video_is_correct = check_video(cd['link'])
            
            if not video_is_correct:
                return HttpResponse('Looks like you have to use another video :(')
            
            # Load video and get info
            video = YouTube(cd['link'])
            video_details = {
                'title': video.title,
                'thumbnail': video.thumbnail_url
            }
            
            #FIXME: Bug ked dam url len https://www.youtube.com/
            match = re.search(r"/watch\?v=([^&]*)", cd['link'])
            id = match.group(1)
            
            # AJAX SLEEP
            time.sleep(3)
            
            return render(request, 'pages/partials/video.html', {'video_id': id, 'video': video_details, 'link': cd['link']})
        else:
            #FIXME: Bug, ak uz raz nastane tento response check_video() sa nespusta znova + text ostava na stranke a nerefreshuje sa
            return HttpResponse('Please insert a youtube video :)')

    return render(request, 'pages/start.html', {'form': form})

def about(request):
    pass
