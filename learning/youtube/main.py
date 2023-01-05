from pytube import YouTube
from .modules.audio import extract_audio
from .modules.captions import extract_captions
import time

def process_video(link, video_id, user_id, timestamps):
    
    # Load video
    video = YouTube(link)
    
    # Download Audio
    try:
        audio = video.streams.get_audio_only('mp4')
        print('Downloading AUDIO....')
        audio.download(output_path=f'media/video/{video_id}_{user_id}/', filename=f'{video_id}.mp4')
        print('AUDIO Downloaded.')
    except:
        print('AUDIO NOT FOUND.')
    
    # Handle audio
    for i, timestamp in enumerate(timestamps):
        start, end = timestamp
        print(f'Extracting Audio part {i}')
        extract_audio(start, end, video_id, user_id, current_iteration=i)
        print('Done.')
    
    
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


    
    # Handle Captions
    for i, timestamp in enumerate(timestamps):
        
        
        #TODO: Hod sem aj audio a rob to pod jednym Loopom
        #TODO: Ukladanie zmen na videoid_userid/
        
        start, end = timestamp
        print(f'Extracting Subtitles part {i}')
        sentences = extract_captions(start, end, video_id, user_id)
        
        print('Writing captions to a File.')
        
        with open(f'media/video/{video_id}_{user_id}/{i}/{i}.srt', 'w') as file:
            
            for sentence in sentences:
                
                file.write(sentence)
                file.write('\n')
            
        
        print('Done.')
    
  
