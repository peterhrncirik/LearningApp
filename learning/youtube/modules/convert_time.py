def convert_time(timestamp):
    
    hours = timestamp.hour
    minutes = timestamp.minute
    seconds = timestamp.second
    total = (hours * 3600 + minutes * 60 + seconds) * 1000
    
    return(total)

def convert_time_from_srt(timestamp):
    
    # Split into parts
    parts = timestamp.split(':')
    
    # Convert to ints
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds_milliseconds = parts[2].split(",")
    seconds = int(seconds_milliseconds[0]) - 1
    print('REQUESTED SECONDS: ', int(seconds_milliseconds[0]))
    print('REAL SECONDS: ', seconds)
    milliseconds = int(seconds_milliseconds[1])
    
    # Convert time to milliseconds
    # total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
    total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 
      
    return total_ms