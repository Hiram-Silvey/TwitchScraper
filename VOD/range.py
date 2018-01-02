"""Usage:
    range.py <incsv> <outcsv> <overlap_in_minutes>
"""

from docopt import docopt
from IPython import embed

args = docopt(__doc__)

min_overlap = int(args['<overlap_in_minutes>'])*60

starts = []
ends = []
start_to_end = {}
end_to_start = {}

with open(args['<incsv>'], 'r') as f:
    for line in f:
        vid, start, end = map(int, line.split('\t'))
        starts.append(start)
        start_to_end[start] = (vid, end)
        ends.append(end)
        end_to_start[end] = start

starts.sort()
ends.sort(reverse=True)

while len(starts) > 1 and (starts[-1]+min_overlap)%86400 >= ends[-1]:
    linked_end = start_to_end[starts[-1]][1]
    next_end = ends[-1] if linked_end != ends[-1] else ends[-2]
    start_gain = next_end - starts[-2]
    linked_start = end_to_start[ends[-1]]
    next_start = starts[-1] if linked_start != starts[-1] else starts[-2]
    end_gain = ends[-2] - next_start
    if start_gain > end_gain:
        start = starts.pop()
        ends.remove(linked_end)
    else:
        end = ends.pop()
        starts.remove(linked_start)

with open(args['<outcsv>'], 'w+') as f:
    f.write('{}\t{}\n'.format(starts[-1], ends[-1]))
    for start in starts:
        f.write('{}\t{}\t{}\n'.format(start_to_end[start][0], start, start_to_end[start][1]))
