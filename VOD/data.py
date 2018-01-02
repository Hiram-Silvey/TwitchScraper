"""Usage:
    data.py <csvfile>
"""

import requests
import time
import calendar
from docopt import docopt
import cfg
from IPython import embed

args = docopt(__doc__)

def expand_date_time(date_time):
    date_time = date_time[date_time.find('T')+1:-1]
    hours, mins, secs = map(int, date_time.split(':'))
    return ((hours*60)+mins)*60+secs

def expand_duration(duration):
    h_idx = duration.find('h')
    m_idx = duration.find('m')
    s_idx = duration.find('s')
    hours = int(duration[:h_idx]) if h_idx != -1 else 0
    mins = int(duration[h_idx+1:m_idx]) if m_idx != -1 else 0
    secs = int(duration[m_idx+1:s_idx]) if s_idx != -1 else 0
    return ((hours*60)+mins)*60+secs

r = requests.get('https://api.twitch.tv/helix/videos?user_id={}&type={}&first={}'.format(cfg.PUBG, 'archive', 100), headers={'Client-ID': cfg.CLIENT_ID})

vods = r.json()['data']
pattern = '%Y-%m-%dT%H:%M:%SZ'
with open(args['<csvfile>'], 'w+') as f:
    for vod in vods:
        date_time = vod['created_at']
        duration = vod['duration']
        end_time = expand_date_time(date_time)
        start_time = end_time - expand_duration(duration)
        if start_time < 0:
            start_time = 86400 + start_time
        vod_id = vod['id']
        f.write('{}\t{}\t{}\n'.format(vod_id, start_time, end_time))
