"""Which saved articles name each member of Congress: the counts the figure prints ("named in N of the articles counted").
In the builder's project this module reads the saved pages themselves; they are not in this copy (no article text is), so here
the same answer is read from research/story_pages.tsv, which lists every saved page by address with the article it is a copy of,
whether it is counted, and the members its text names. An article is counted once, whatever the number of its copies."""
import csv
from collections import defaultdict
from pathlib import Path
R = Path(__file__).resolve().parents[1] / 'research'


def count():
    """(articles counted, {surname: [article ids]}, {})"""
    hit = defaultdict(set); arts = set()
    for r in csv.DictReader(open(R / 'story_pages.tsv', newline=''), delimiter='\t'):
        if r['counted'] != 'yes':
            continue
        arts.add(r['article'])
        for s in (r['names'] or '').split(';'):
            if s:
                hit[s].add(r['article'])
    return len(arts), defaultdict(list, {s: sorted(v) for s, v in hit.items()}), {}
