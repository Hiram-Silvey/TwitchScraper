import os, chat
from multiprocessing import Pool
from itertools import repeat

overlap_file = '../VOD/overlap.csv'
out_dir = 'data/'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

def save_chat(video_data, overlap_data):
    start, end = overlap_data
    vid, vstart, vend = map(int, video_data.split('\t'))
    offset_start = start-vstart if start-vstart >= 0 else 86400-start+vstart
    duration = end-start if end-start >= 0 else 86400-start+vstart
    offset_end = offset_start+duration
    comments = chat.get_chat(vid, offset_start, offset_end)
    if len(comments) == 0:
        return
    with open(out_dir+str(vid)+'.csv', 'w+') as o:
        for comment in comments:
            o.write('\t'.join(comment)+'\n')

with open(overlap_file, 'r') as f:
    start, end = map(int, f.readline().split('\t'))
    lines = [line for line in f]
    p = Pool()
    p.starmap(save_chat, zip(lines, repeat((start, end))))
