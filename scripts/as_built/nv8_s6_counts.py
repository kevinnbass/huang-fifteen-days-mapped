"""Counts for the footnote's sentences on the search of the actors' own channels, from research/nv8_s6_items.tsv.

Run: python3 -I scripts/nv8_s6_counts.py   -> research/nv8_s6_counts.tsv (what, count)
Every line of an actor's own channel gets one class, and an actor is counted once, by the best class any of its lines has:
  held     an item about the affair that the project holds and has read (drawn or folded into a chip, saved and cited, or on a chip
           whose original the project holds);
  reader   an item about the affair that the reader opened and matched to a chip, of which the project holds no copy (the site
           refused the project's own fetch, or the original could not be opened again);
  located  links to items were found and none could be read (a paywall);
  context  the only items are not about the affair (a share-sale filing, a policy paper, a letter on another subject) or are not the
           actor's own;
  none     a channel could be read and held nothing;
  unread   no channel could be read.
"About the affair" means the item names Huang's case, the reports on it, Megaspeed's part in it or an act taken because of it. A chip
can draw a context item (Anthropic's share-sale filing, OpenAI's policy paper): being on a chip does not make it an item about the
affair, and an item counts as held only where the project holds the page (two readings of Nov 15, 2026 found the earlier counts wrong
on both points)."""
import csv
from collections import Counter, defaultdict
from pathlib import Path
R = Path(__file__).resolve().parent.parent / 'research'
CONTEXT_CHIPS = {'MA68', 'MA69'}          # Anthropic's share-sale filing; OpenAI's policy paper: drawn as context, neither names the affair
ORDER = ['held', 'reader', 'located', 'context', 'none', 'unread']


def chip_kind(r):
    d = r['what_was_done']
    if d.startswith('now cited (post): '):      # the reader could not open the post; the project saved it afterwards by its id
        return 'post later'
    if d.startswith('now cited: '):             # the search did not yield the original; a saved copy of the publisher's page is cited now
        return 'cited later'
    if 'first remark' in d:
        return 'part'
    if 'not saved' in d:
        return 'found, not saved'
    if d.startswith('gap: blocked'):
        return 'blocked'
    if d.startswith('gap: not found'):
        return 'not found'
    assert r['lane_result'] == 'found' and ('cited' in d or 'cites' in d), (r['key'], d)
    return 'cited'


def main():
    rows = list(csv.DictReader(open(R / 'nv8_s6_items.tsv', newline=''), delimiter='\t'))
    chips = [r for r in rows if r['part'] == 'original of a chip']
    ck = {r['key']: chip_kind(r) for r in chips}
    assert len(ck) == len(chips)

    def kind(r):
        d, res, key = r['what_was_done'], r['lane_result'], r['key']
        if d.startswith('already on chip'):
            if key in CONTEXT_CHIPS:
                return 'context'
            if 'hand-saved' in d or ck.get(key, 'cited') in ('cited', 'cited later', 'post later', 'part'):      # a chip outside the searches was drawn from its original
                return 'held'
            return 'reader'
        if 'policy-blueprint' in d or 'does not mention the matter' in d or 'is about another report' in d or 'by another author' in d:
            return 'context'
        if d.startswith(('drawn: chip', 'folded into chip', 'saved as', 'saved and cited')) or 'which is chip' in d or "reproduces the ministry's transcript" in d:
            return 'held'
        if d.startswith(('not read', 'not saved')):
            return 'located'
        if res.startswith('nothing on the matter'):
            return 'none'
        assert res == 'blocked' and d == 'nothing to draw', (r['actor'], res, d)
        return 'unread'

    best = defaultdict(set)
    for r in rows:
        if r['part'] == "actor's own channel":
            best[r['actor']].add(kind(r))
    cls = {a: next(o for o in ORDER if o in ks) for a, ks in best.items()}
    c = Counter(cls.values()); cc = Counter(ck.values())
    assert sum(cc.values()) == len(chips) and sum(c.values()) == len(cls)
    out = [('actors whose own channels were searched', len(cls)),
           ('actors: an item about the affair is held and was read', c['held']),
           ('actors: the reader matched an item about the affair to a chip, and the project holds no copy', c['reader']),
           ('actors: links located, none could be read', c['located']),
           ('actors: only items that are not about the affair or not their own', c['context']),
           ('actors: nothing found on a channel that could be read', c['none']),
           ('actors: no channel could be read', c['unread']),
           ('chips whose original was searched for', len(chips)), ('chips: original read and cited on the chip', cc['cited']),
           ('chips: the search did not yield the original; a saved copy of the publisher\'s page is now cited', cc['cited later']),
           ('chips: the search could not open the post; the post itself, saved afterwards by its id, is now cited', cc['post later']),
           ('chips: original carries the first of the chip\'s two remarks', cc['part']), ('chips: original could not be opened', cc['blocked']),
           ('chips: original found by the reader and refused to the project (not saved)', cc['found, not saved']),
           ('chips: original not found', cc['not found']),
           ('chips still without their original that now also cite a paper\'s own report of the act', sum(1 for r in chips if r['what_was_done'].startswith('gap: ') and "a paper's own report of it" in r['what_was_done']))]
    with open(R / 'nv8_s6_counts.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['what', 'count']); w.writerows(out)
    for k, v in out:
        print(f'{v:>5}  {k}')
    for o in ORDER:
        print(o, sorted(a for a, v in cls.items() if v == o))


if __name__ == '__main__':
    main()
