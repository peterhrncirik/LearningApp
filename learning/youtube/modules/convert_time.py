def convert_time_x(timestamp, subs_start=False):
    
    #TODO: Zatial to vyzera ze audio treba trochu predlzit, ale treba este otestovat
    
    # Convert to ints
    hours = timestamp.hour
    minutes = timestamp.minute
    
    if subs_start:
        seconds = timestamp.second - 1
        
    seconds = timestamp.second 
    
    # Convert time to milliseconds
    total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000
    
    return total_ms

def convert_time_from_srt(timestamp):
    
    # Split into parts
    parts = timestamp.split(':')
    
    # Convert to ints
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds_milliseconds = parts[2].split(",")
    seconds = int(seconds_milliseconds[0])
    milliseconds = int(seconds_milliseconds[1])
    
    # Convert time to milliseconds
    # total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
    total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 
    
    return total_ms

def convert_time(timestamp, subs_start=False):
    
    # Split into parts
    parts = timestamp.split(':')
    
    # Convert to ints
    hours = int(parts[0])
    minutes = int(parts[1])
    if subs_start:
        seconds = int(parts[2]) - 1
    seconds = int(parts[2])
    
    # Convert time to milliseconds
    total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 
    
    return total_ms