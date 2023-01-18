import os
from pydub import AudioSegment
from .convert_time import convert_time


def extract_audio(start_time, end_time, video_id, user_id, current_iteration):
    
    # Load Audio File
    print('Looking for file')
    audio = AudioSegment.from_file(f"media/video/{video_id}_{user_id}/{video_id}.mp4", "mp4")
    print('File found')

    print('Extracting specific part')
    # Extract specific part
    start = convert_time(start_time)
    end = convert_time(end_time)
    extracted_audio = audio[start:end]

    # Save to New File
    os.makedirs(f'media/video/{video_id}_{user_id}/output/{current_iteration}/')
    extracted_audio.export(f'media/video/{video_id}_{user_id}/output/{current_iteration}/{current_iteration}.mp3', format='mp3')

