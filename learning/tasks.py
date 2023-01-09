from __future__ import absolute_import, unicode_literals

from celery import shared_task, Task
from celery_progress.backend import ProgressRecorder

from time import sleep

from pytube import YouTube
from .youtube.modules.audio import extract_audio
from .youtube.modules.captions import extract_captions


@shared_task(bind=True)
def process_video_async(self, link, video_id, user_id, timestamps):
    progress_recorder = ProgressRecorder(self)
    
    video = YouTube(link)
    
    # Download Audio
    try:
        audio = video.streams.get_audio_only('mp4')
        print('Downloading AUDIO....')
        audio.download(output_path=f'media/video/{video_id}_{user_id}/', filename=f'{video_id}.mp4')
        print('AUDIO Downloaded.')
    except:
        print('AUDIO NOT FOUND.')
    
    # Download Captions
    # Already checked in first view so maybe this can be removed
    try:
        
        if video.captions.get('de'):
            captions = video.captions['de']
        elif video.captions.get('a.de'):
            captions = video.captions['a.de']
            
        print('Downloading SUBTITLES....')
        captions.download(f'{video_id}', output_path=f'media/video/{video_id}_{user_id}/')
        print('SUBTITLES Downloaded.')
    except Exception as e:
        print('SUBTITLES Not Found.')
        print(e)


    # Handle audio
    for i, timestamp in enumerate(timestamps):
        
        start, end = timestamp
        
        print(f'Extracting Audio part {i}')
        extract_audio(start, end, video_id, user_id, current_iteration=i)
        print('Done.')
        
        print(f'Extracting Subtitles part {i}')
        sentences = extract_captions(start, end, video_id, user_id)
        
        print('Writing captions to a File.')
        
        with open(f'media/video/{video_id}_{user_id}/{i}/{i}.srt', 'w') as file:
            
            for sentence in sentences:
                
                file.write(sentence)
                file.write('\n')
            
        
        print('Done.')
        progress_recorder.set_progress(i + 1, len(timestamps), description='Processing video in CELERY......')