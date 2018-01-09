
#!/usr/bin/env python

 

import requests
import numpy as np
chat = []
 

def get_comments(vid_id, video_start, video_end, desire_start,desire_end):

    r = requests.get('https://api.twitch.tv/v5/videos/'+str(vid_id)+'/comments?client_id=9jkelimecr9yevu0ez4n51orefunjv')

    data = r.json()['comments']
    for x in data:
        body = str(test['message']['body'])
        name = str(test['commenter']['display_name'])
        time = str(test['content_offset_seconds'])
        line = [name, time, body]
        if line not in chat:
            chat.append(line)
   

    

 

#get_comments(1,1)


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
