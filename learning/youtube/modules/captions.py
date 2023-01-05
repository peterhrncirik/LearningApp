import re
from .convert_time import convert_time, convert_time_from_srt

def extract_captions(start_time, end_time, id):
    
    with open(f'media/video/{id}/{id}.srt', encoding="utf-8") as file:
        
        pattern = r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3}) --> \|(.*?)\|"

        lines = file.readlines()
        
        # Empty list for sentences
        lines_to_extract = []
    
        for row in lines:
            
            for match in re.finditer(pattern, row):
                
                to_extract_start = convert_time(start_time, subs_start=True)
                to_extract_end = convert_time(end_time)
                sentence = match.group(3)
                
                
                start_ms = convert_time_from_srt(match.group(1))
                end_ms = convert_time_from_srt(match.group(2))
                
                # titulky predlzit start aj koniec o sekundu
                if to_extract_start <= start_ms <= to_extract_end:
                    lines_to_extract.append(sentence.strip())
                
         
    
        return lines_to_extract           
                
        