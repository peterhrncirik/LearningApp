from pytube import YouTube

def check_video(link):
    
    
    #TODO: Urob to viac detailed, ak chybaju captions napis to, resp. daj nejaku info co chyba
    
    video = YouTube(link)
    audio = video.streams.get_audio_only('mp4')
    captions = False
    
    if video.captions.get('de'):
        captions = video.captions['de']
    elif video.captions.get('a.de'):
        captions = video.captions['a.de']
        
    return True if audio and captions else False
    