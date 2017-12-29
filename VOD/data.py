import requests
import time
import calendar
import cfg

def expand_time(hms_time):
    h_idx = hms_time.find('h')
    m_idx = hms_time.find('m')
    s_idx = hms_time.find('s')
    hours = int(hms_time[:h_idx]) if h_idx != -1 else 0
    mins = int(hms_time[h_idx+1:m_idx]) if m_idx != -1 else 0
    secs = int(hms_time[m_idx+1:s_idx]) if s_idx != -1 else 0
    return ((hours*60)+mins)*60+secs

r = requests.get('https://api.twitch.tv/helix/videos?user_id={}'.format(cfg.USER_ID), headers={'Client-ID': cfg.CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'})

vods = r.json()['data']
pattern = '%Y-%m-%dT%H:%M:%SZ'
with open('metadata.csv', 'w+') as f:
    for vod in vods:
        date_time = vod['created_at']
        duration = vod['duration']
        end_time = calendar.timegm(time.strptime(date_time, pattern))
        start_time = end_time - expand_time(duration)
        vod_id = vod['id']
        f.write('{}\t{}\t{}\n'.format(vod_id, start_time, end_time))
