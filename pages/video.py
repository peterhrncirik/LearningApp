from pytube import YouTube

def check_video(link, language):
    
    
    #TODO: Urob to viac detailed, ak chybaju captions napis to, resp. daj nejaku info co chyba
    #NOTE: bud je to de alebo a.de ako auto-generated - pre kazdy language

    video = YouTube(link)
    audio = video.streams.get_audio_only('mp4')
    captions = False
    
    if video.captions.get(language):
        captions = video.captions[language]
    elif video.captions.get(f'a.{language}'):
        captions = video.captions[f'a.{language}']
    
    return True if audio and captions else False
    
