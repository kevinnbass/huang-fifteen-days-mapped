"""Which saved news pages name each member of Congress: the counts the figure prints ("named on N of the saved pages").
In the builder's project this module reads the saved pages themselves; they are not in this copy (no article text is), so here
the same answer is read from research/story_pages.tsv, which lists every counted page by address and the members it names."""
import csv
from collections import defaultdict
from pathlib import Path
R = Path(__file__).resolve().parents[1] / 'research'


def count():
    """(pages counted, {surname: [page ids]}, {})"""
    hit = defaultdict(list); n = 0
    for r in csv.DictReader(open(R / 'story_pages.tsv', newline=''), delimiter='\t'):
        n += 1
        for s in (r['names'] or '').split(';'):
            if s:
                hit[s].append(r['id'])
    return n, hit, {}
