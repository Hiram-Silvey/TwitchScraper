"""Usage:
    videos.py <videolist.csv> <output_folder>
"""

import os, sys
from multiprocessing import Pool
from docopt import docopt
sys.path.append(os.path.abspath('./youtube-dl'))
import youtube_dl

args = docopt(__doc__)

def download(ydl, start, end, vid, vstart, vend):
        ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])

ydl_opts = {}
ydl = youtube_dl.YoutubeDL(ydl_opts)

with open(args['<videolist.csv>'], 'r') as f:
    start, end = f.readline().split('\t')
    vids = []
    for line in f:
        vid, vstart, vend = line.split('\t')
        vids.append((vid, vstart, vend))
