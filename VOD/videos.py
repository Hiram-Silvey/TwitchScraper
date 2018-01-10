"""Usage:
    videos.py [--keep-original] <videolist.csv> <output_folder>
"""

import os, sys, subprocess
from multiprocessing import Pool
from itertools import repeat
from docopt import docopt
sys.path.append(os.path.abspath('./youtube-dl'))
import youtube_dl

args = docopt(__doc__)
slash = '/' if not args['<output_folder>'].endswith('/') else ''
out_folder = args['<output_folder>'] + slash
trim_folder = out_folder + 'trimmed/'
if not os.path.isdir(out_folder):
    os.mkdir(out_folder)
if not os.path.isdir(trim_folder):
    os.mkdir(trim_folder)

def get_ffmpeg_time(time_in_secs):
    secs = time_in_secs%60
    time_in_mins = time_in_secs/60
    mins = time_in_mins%60
    hours = time_in_mins/60
    return '{}:{}:{}'.format(hours, mins, secs)

def download(metadata, params):
        vid, vstart, vend = metadata
        start, end = params
        outfile = out_folder + vid
        ydl = youtube_dl.YoutubeDL({})
        ydl.params['outtmpl'] = outfile
        downloaded = ydl.download(['https://www.twitch.tv/videos/{}'.format(vid)])
        if downloaded == 0:
            print('{} successfully downloaded.'.format(vid))
        else:
            print('Error downloading {}, try again.'.format(vid))
        trimmed = subprocess.run(['ffmpeg', '-v', 'quiet', '-y', '-i', outfile, '-vcodec', 'copy', '-acodec', 'copy', '-ss', get_ffmpeg_time(start-vstart), '-t', get_ffmpeg_time(end-vend), '-sn', trim_folder + vid])
        if trimmed == 0:
            print('{} successfully trimmed.'.format(vid))
            if not args['--keep-original']:
                os.remove(outfile)
        else:
            print('Error trimming {}, try again.'.format(vid))

with open(args['<videolist.csv>'], 'r') as f:
    start, end = f.readline().split('\t')
    vids = []
    for line in f:
        vid, vstart, vend = line.split('\t')
        vids.append((vid, vstart, vend))
    p = Pool()
    p.starmap(download, zip(vids, repeat((start, end))))
