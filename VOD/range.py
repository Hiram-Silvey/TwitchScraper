"""Usage:
    range.py <mdfile>
"""

from docopt import docopt

args = docopt(__doc__)

starts = []
ends = []
start_to_end = {}
end_to_start = {}

with open(args['<mdfile>'], 'r') as f:
    for line in f:
        vid, start, end = map(int, line.split('\t'))
        starts.append(start)
        start_to_end[start] = end
        ends.append(end)
        end_to_start[end] = start

starts.sort()
ends.sort(reverse=True)

while len(starts) > 0 and starts[-1] > ends[-1]:
    print(starts)
    print(ends)
    start_gain = ends[-1] - starts[-2]
    end_gain = ends[-2] - starts[-1]
    print(start_gain)
    print(end_gain)
    if start_gain > end_gain:
        start = starts.pop()
        end = start_to_end[start]
        ends.remove(end)
    else:
        end = ends.pop()
        start = end_to_start[end]
        starts.remove(start)

print(starts)
print(ends)
