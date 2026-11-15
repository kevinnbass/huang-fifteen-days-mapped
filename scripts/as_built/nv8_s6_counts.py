"""Counts for the footnote's sentences on the search of the actors' own channels, from research/nv8_s6_items.tsv.

Run: python3 -I scripts/nv8_s6_counts.py   -> research/nv8_s6_counts.tsv (what, count)
An actor is counted once, by the best that any line of its own channel shows:
  read      an item on the matter was opened and read (it is on a chip, was drawn or folded into one, or repeats one);
  located   links to items were found and none could be read (a paywall, a refusing site);
  none      a channel could be read and held nothing on the matter (an item that does not mention it counts here);
  unread    no channel could be read.
A link that was located and not read is never counted as an item (reading of the corrections, Nov 15, 2026)."""
import csv
from collections import Counter, defaultdict
from pathlib import Path
R = Path(__file__).resolve().parent.parent / 'research'
ON = ('already on chip', 'drawn: chip', 'folded into chip', 'saved as', 'saved and cited')
RELAYS = ('which is chip', "reproduces the ministry's transcript")


def kind(r):
    d, res = r['what_was_done'], r['lane_result']
    if d.startswith(ON) or any(x in d for x in RELAYS):
        return 'read'
    if d.startswith(('not read', 'not saved')):
        return 'located'
    if d.startswith('not drawn') or res.startswith('nothing on the matter'):
        return 'none'
    assert res == 'blocked' and d == 'nothing to draw', (r['actor'], res, d)
    return 'unread'


def main():
    rows = list(csv.DictReader(open(R / 'nv8_s6_items.tsv', newline=''), delimiter='\t'))
    best = defaultdict(set); off = defaultdict(int)
    for r in rows:
        if r['part'] == "actor's own channel":
            k = kind(r); best[r['actor']].add(k)
            off[r['actor']] += k == 'none' and r['what_was_done'].startswith('not drawn')
    order = ['read', 'located', 'none', 'unread']
    cls = {a: next(o for o in order if o in ks) for a, ks in best.items()}
    c = Counter(cls.values())
    chips = [r for r in rows if r['part'] == 'original of a chip']
    def chip_kind(r):
        d = r['what_was_done']
        if 'first remark' in d:
            return 'part'
        if 'not saved' in d:
            return 'found, not saved'                 # the reader opened it; the site refused the project's own fetch
        if d.startswith('gap: blocked'):
            return 'blocked'
        if d.startswith('gap: not found'):
            return 'not found'
        assert r['lane_result'] == 'found' and ('cited' in d or 'cites' in d), (r['key'], d)
        return 'cited'
    cc = Counter(chip_kind(r) for r in chips)
    assert len({r['key'] for r in chips}) == len(chips) and sum(cc.values()) == len(chips)
    out = [('actors whose own channels were searched', len(cls)), ('actors: an item on the matter was read', c['read']),
           ('actors: links located, none could be read', c['located']), ('actors: nothing on the matter on a channel that could be read', c['none']),
           ('actors: of those, the only item found does not mention the matter', sum(1 for a, v in cls.items() if v == 'none' and off[a])),
           ('actors: no channel could be read', c['unread']),
           ('chips whose original was searched for', len(chips)), ('chips: original read and cited on the chip', cc['cited']),
           ('chips: original carries the first of the chip\'s two remarks', cc['part']), ('chips: original could not be opened', cc['blocked']),
           ('chips: original found by the reader and refused to the project (not saved)', cc['found, not saved']),
           ('chips: original not found', cc['not found'])]
    with open(R / 'nv8_s6_counts.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['what', 'count']); w.writerows(out)
    for k, v in out:
        print(f'{v:>5}  {k}')
    for o in order:
        print(o, sorted(a for a, v in cls.items() if v == o))


if __name__ == '__main__':
    main()
