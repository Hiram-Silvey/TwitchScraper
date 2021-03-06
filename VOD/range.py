"""Usage:
    range.py <incsv> <outcsv> <overlap_in_minutes>
"""

import networkx as nx
from docopt import docopt

args = docopt(__doc__)

min_overlap = int(args['<overlap_in_minutes>'])*60
G = nx.Graph()

def is_overlap(node_a, node_b):
    a_vid, a_start, a_end = node_a
    b_vid, b_start, b_end = node_b
    a_len = a_end - a_start
    if a_len < 0:
        a = ((a_start, 86400), (0, a_end))
        a_len = 86400 + a_len
    else:
        a = ((a_start, a_end),)
    b_len = b_end - b_start
    if b_len < 0:
        b = ((b_start, 86400), (0, b_end))
        b_len = 86400 + b_len
    else:
        b = ((b_start, b_end),)
    if a_len < min_overlap or b_len < min_overlap:
        return False
    ab_overlap = min((a[0][1], b[0][1])) - max((a[0][0], b[0][0]))
    if len(a) == 2 and len(b) == 2:
        ab2_overlap = min((a[1][1] - a[1][0], b[1][1] - b[1][0]))
        ab_overlap += ab2_overlap
    elif len(a) == 2:
        ab2_overlap = min((a[1][1], b[0][1])) - max((a[1][0], b[0][0]))
        ab_overlap = max((ab_overlap, ab2_overlap))
    elif len(b) == 2:
        ab2_overlap = min((a[0][1], b[1][1])) - max((a[0][0], b[1][0]))
        ab_overlap = max((ab_overlap, ab2_overlap))
    if ab_overlap > min_overlap:
        return True
    return False

def get_overlap(nodes):
    if len(nodes) == 0:
        return (None, None)
    vid, start, end = nodes[0]
    for node in nodes[1:]:
        vid, vstart, vend = node
        update_start = False
        update_end = False
        if end - start < 0 and vend - vstart > 0 and vstart < end:
            update_start = True
        elif vstart > start:
            update_start = True
        if end - start < 0 and vend - vstart > 0 and vend > start:
            update_end = True
        elif vend < end:
            update_end = True
        start = vstart if update_start else start
        end = vend if update_end else end
    return (start, end)

with open(args['<incsv>'], 'r') as f:
    for line in f:
        vid, start, end = map(int, line.split('\t'))
        curr_node = (vid, start, end)
        G.add_node(curr_node)
        nodes = (node for node in G.nodes if node != curr_node)
        for node in nodes:
            if is_overlap(node, curr_node):
                G.add_edge(node, curr_node)

max_len = 0
best_clique = None
for clique in nx.find_cliques(G):
    clique_len = len(clique)
    if clique_len > max_len:
        max_len = clique_len
        best_clique = clique

if best_clique is not None:
    start, end = get_overlap(best_clique)
    with open(args['<outcsv>'], 'w+') as f:
        f.write('{}\t{}\n'.format(start, end))
        for (vid, vstart, vend) in best_clique:
            f.write('{}\t{}\t{}\n'.format(vid, vstart, vend))
