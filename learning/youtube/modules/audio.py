from pydub import AudioSegment
from .convert_time import convert_time


def extract_audio(start_time, end_time, id):
    
    # Load Audio File
    print('Looking for file')
    audio = AudioSegment.from_file(f"media/video/{id}/{id}.mp4", "mp4")
    print('File found')
    # audio = AudioSegment.from_file("audio.mp4", "mp4")

    print('Extracting specific part')
    # Extract specific part
    start = convert_time(start_time)
    end = convert_time(end_time)
    extracted_audio = audio[start:end]

    # Save to New File
    extracted_audio.export('media/video/new.mp3', format='mp3')

