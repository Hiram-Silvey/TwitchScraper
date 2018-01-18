"""Usage:
    trim.py [--keep-original] <videolist.csv> <video_dir>
"""

import os, sys, subprocess
from multiprocessing import Pool
from docopt import docopt

args = docopt(__doc__)
slash = '/' if not args['<video_dir>'].endswith('/') else ''
out_dir = args['<video_dir>'] + slash + 'trimmed/'
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

def get_ffmpeg_time(time_in_secs):
    secs = time_in_secs%60
    time_in_mins = time_in_secs//60
    mins = time_in_mins%60
    hours = time_in_mins//60
    return '{:02}:{:02}:{:02}'.format(hours, mins, secs)

def trim(vfile, vid, vstart, vend, start, end):
    duration = end-start if end-start >= 0 else 86400-start+end
    offset_start = start-vstart if start-vstart >= 0 else 86400-start+vstart
    trimmed = subprocess.run(['ffmpeg', '-v', 'quiet', '-y', '-i', vfile, '-vcodec', 'copy', '-acodec', 'copy', '-ss', get_ffmpeg_time(offset_start), '-t', get_ffmpeg_time(duration), '-sn', out_dir + str(vid) + '.mp4'])
    if trimmed.returncode == 0:
        print('{} successfully trimmed.'.format(vid))
        if not args['--keep-original']:
            os.remove(vfile)
    else:
        print('Error trimming {}, try again.'.format(vid))

with open(args['<videolist.csv>'], 'r') as f:
    start, end = map(int, f.readline().split('\t'))
    vids = {}
    for line in f:
        vid, vstart, vend = map(int, line.split('\t'))
        vids[vid] = (vstart, vend)

params = []
for f in os.listdir(args['<video_dir>']):
    f_path = args['<video_dir>'] + slash + f
    if not os.path.isfile(f_path) or not f.endswith('.mp4'):
        continue
    vid = int(f[:-4])
    params.append((f_path, vid, *vids[vid], start, end))

def worker(param):
    trim(*param)

p = Pool()
p.map(worker, params)
