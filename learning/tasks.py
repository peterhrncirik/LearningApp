from __future__ import absolute_import, unicode_literals

from shutil import make_archive
from time import sleep

from celery import shared_task
from celery_progress.backend import ProgressRecorder

from pytube import YouTube
from .youtube.modules.audio import extract_audio
from .youtube.modules.captions import extract_captions

@shared_task(bind=True)
def process_video_async(self, link, video_id, user_id, timestamps):
    
    """
    Process video async
    """
    progress_recorder = ProgressRecorder(self)
    
    # Load the video
    video = YouTube(link)
    audio = None
    captions = None
    
    # Handle Audio and Captions Extranctions
    for i, timestamp in enumerate(timestamps):
    
        start, end = timestamp
        
        if not audio or not captions:
            # Download Audio
            try:
                audio = video.streams.get_audio_only('mp4')
                print('Downloading AUDIO....')
                audio.download(output_path=f'media/video/{video_id}_{user_id}/', filename=f'{video_id}.mp4')
                print('AUDIO Downloaded.')
            except:
                print('AUDIO NOT FOUND.')
            
            # Download Captions
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
        
        print(f'Extracting Audio part {i}')
        extract_audio(start, end, video_id, user_id, current_iteration=i)
        print('Done.')
        
        print(f'Extracting Subtitles part {i}')
        sentences = extract_captions(start, end, video_id, user_id)
        
        print('Writing captions to a File.')
        
        with open(f'media/video/{video_id}_{user_id}/output/{i}/{i}.srt', 'w') as file:
            
            for sentence in sentences:
                
                if sentence:
                    file.write(sentence)
                    file.write('\n')
        
            
        percentage = (i + 1) / len(timestamps) * 100
        print('Done.')
        progress_recorder.set_progress(i + 1, len(timestamps), description=f'{percentage:.0f}% of files prepared.')


    make_archive(f'media/video/{video_id}_{user_id}/files', 'zip', f'media/video/{video_id}_{user_id}/output/')

    




    
