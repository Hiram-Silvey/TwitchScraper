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
out_folder = os.path.abspath(args['<output_folder>'])
trim_folder = out_folder + '/trimmed/'
if not os.path.isdir(args['<output_folder>']):
    os.mkdir(args['<output_folder>'])
if not os.path.isdir(trim_folder):
    os.mkdir(trim_folder)

def get_ffmpeg_time(time_in_secs):
    secs = time_in_secs%60
    time_in_mins = time_in_secs//60
    mins = time_in_mins%60
    hours = time_in_mins//60
    return '{:02}:{:02}:{:02}'.format(hours, mins, secs)

def trim(vfile, vid, vstart, vend, start, end):
    ivstart, ivend, istart, iend = map(int, [vstart, vend, start, end])
    duration = iend-istart if iend-istart >= 0 else 86400-istart+iend
    offset_start = istart-ivstart if istart-ivstart >= 0 else 86400-istart+ivstart
    trimmed = subprocess.run(['ffmpeg', '-v', 'quiet', '-y', '-i', vfile, '-vcodec', 'copy', '-acodec', 'copy', '-ss', get_ffmpeg_time(offset_start), '-t', get_ffmpeg_time(duration), '-sn', trim_folder + vid + '.mp4'])
    if trimmed.returncode == 0:
        print('{} successfully trimmed.'.format(vid))
        if not args['--keep-original']:
            os.remove(vfile)
    else:
        print('Error trimming {}, try again.'.format(vid))

def download(metadata, params):
        vid, vstart, vend = metadata
        start, end = params
        outfile = out_folder + '/' + vid + '.mp4'
        if os.path.isfile(outfile):
            print('{} already exists, trimming...'.format(out_file))
            trim(outfile, vid, vstart, vend, start, end)
        else:
            ydl = youtube_dl.YoutubeDL({'outtmpl': outfile, 'retries': 10, 'quiet': true})
            downloaded = ydl.download(['https://www.twitch.tv/videos/{}'.format(vid)])
            if downloaded == 0:
                print('{} successfully downloaded. trimming...'.format(vid))
                trim(outfile, vid, vstart, vend, start, end)
            else:
                print('Error downloading {}, try again.'.format(vid))

with open(args['<videolist.csv>'], 'r') as f:
    start, end = f.readline().split('\t')
    vids = []
    for line in f:
        vid, vstart, vend = line.split('\t')
        vids.append((vid, vstart, vend))
    p = Pool()
    p.starmap(download, zip(vids, repeat((start, end))))
