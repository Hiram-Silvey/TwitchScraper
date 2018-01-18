
#!/usr/bin/env python

 

import requests
chat = []



def get_comments(vid_id, vstart, vend):
    start = 39483
    end = 43778
    duration = end-start if end-start >= 0 else 86400-start+end
    offset_start = start-vstart if start-vstart >= 0 else 86400-start+vstart
    url = 'https://api.twitch.tv/v5/videos/'+str(vid_id)+'/comments?client_id=9jkelimecr9yevu0ez4n51orefunjv'
    #try to find first chunk of data with desired start time
    found_data = 0 #flag to say if we found the chunk of 59 with the time we want
    entry_data = 0 #so we can keep track of which entry in a chunk of 59 is the start of the comments we want
    cursor = 0
    while not found_data:
        if cursor!=0:
            url = url+'&cursor='+str(cursor)
        r = requests.get(url)
        current_cursor = cursor
        print(r.json()['_next'])
        cursor = r.json()['_next']
        data = r.json()['comments']
        for i,x in enumerate(data):
            if(x['content_offset_seconds']>=offset_start):
                found_data = 1 #set flag to found
                entry_data = i
                cursor=current_cursor #so that we start from the chunk of comments that we found the correct time in
                end_time = x['content_offset_seconds'] + duration #for later when we need to stop finding comments
                break
    #now that we have found the data and the entry number we need to go until we get to the end
    stop_searching = 0 #flag for when to stop getting comments
    first_data = 1 #flag for first data set we pull only needs to start at entry_data
    while  not stop_searching:
        url = url+'&cursor='+str(cursor) 
        r = requests.get(url)
        cursor = r.json()['_next']
        data = r.json()['comments']      
        for i,x in enumerate(data):
            body = str(x['message']['body'])
            name = str(x['commenter']['display_name'])
            time = str(x['content_offset_seconds'])
            line = [name, time, body]
            if first_data:
                if i>=entry_data and line not in chat and time<=end_time:
                    chat.append(line)
                    first_data=0
            elif line not in chat and time<=end_time:
                chat.append(line)
            elif time>end_time:
                stop_searching=1
                break
    print("test")

   

    

 ##I can give you video IDs, video start times, video end times, and the specific start and end time that we want
##times are in the format: ((hour*60)+mins)*60+secs
##seconds from 00:00 in the day
##so 16:43:23 = ((16*60)+43)*60+23 = 60203
##if I give you the start time, end time, as well as the relative start time of the 1hr period then you should be good
##like if the start time is 60000
##and the start time of the 1hr period is 75000
##then you know that you need to go 15000 seconds forward in the video to get to the start of the 1hr period
##one tricky part is that sometimes streamers stream overnight
##so if they start at 11PM and end at 4AM
##the start time will be a large number
##and the end will be a small number
##86400 is the total number of seconds in a day
##so you have to have some logic that understands
##if the stream starts at like 85000 and the start of the 1hr period is 2000, that you need to go 1400+2000=3400 seconds forward to get to the start of the 1hr period
##
