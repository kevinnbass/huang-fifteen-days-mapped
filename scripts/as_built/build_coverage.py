"""Bind each piece in the coverage plot to the saved aggregator page that lists it.
Run: python3 -I scripts/build_coverage.py -> research/coverage_rows.tsv (one row per web address on the story)
For each address in research/harvest.tsv that story_scope places on the story, find the headline in a saved aggregator
page: first the page recorded as its first listing; failing that, the earliest other saved page that holds it. The
passage kept is the page's own run of text (a page can put spaces around a link inside a headline, so the match
allows spaces to differ and then copies what the page has). An address whose headline is found on no saved page is
kept and marked unbound; it is not dropped. Identity is the address; nothing is merged on a headline."""
import csv, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import check_rows as cr, story_scope, harvest_links as H
FIRST, LAST = '2026-10-29', '2026-11-12'
REG = R / 'coverage_row_ids.csv'


def find(hay, headline):
    """The run of `hay` that equals the headline once spaces are ignored, or ''."""
    n = cr.norm(headline)
    if n in hay:
        return n
    toks = [re.escape(t) for t in re.findall(r'\S', n)]
    if len(toks) < 8:
        return ''
    m = re.search(r'\s*'.join(toks), hay)
    return m.group(0) if m else ''


def main():
    snaps = sorted(d.name for d in (R / 'primary').iterdir() if d.name.startswith(('techmeme-', 'memeorandum-', 'mediagazer-')))
    out, how = [], {'first': 0, 'other': 0, 'unbound': 0}
    # row ids are frozen once an audit has read them: the register maps each address to its id (seeded from the audited table)
    if not REG.exists():
        with open(REG, 'w', newline='') as f:
            w = csv.writer(f, lineterminator='\n'); w.writerow(['url', 'row_id'])
            w.writerows([r['url'], r['row_id']] for r in csv.DictReader(open(R / 'coverage_rows.tsv', newline=''), delimiter='\t'))
    # keyed by what makes two links the same piece (harvest_links.key), so that a later page listing the same piece under
    # another spelling of its address (a tracking field, a longer headline's link) keeps the id and the address first recorded
    reg = list(csv.DictReader(open(REG, newline=''))); ids = {H.key(r['url']): (r['row_id'], r['url']) for r in reg}; new_ids = []
    assert len(ids) == len(reg), 'two registered addresses are the same piece'
    for r in csv.DictReader(open(R / 'harvest.tsv', newline=''), delimiter='\t'):
        if story_scope.scope(r['url'], r['anchor_text']) != 'story':
            continue
        cite, q = '', ''
        # a page saved for a day before the piece was first listed cannot be its citing page: such a page can still carry the headline in
        # a live sidebar of the other aggregator (second audit, Nov 15, 2026: two pieces of Nov 12 were cited from an Oct 29 page)
        day_of = lambda x: (lambda m: f'2026-{m.group(1)}-{m.group(2)}' if m else '9999')(re.search(r'-(\d{2})(\d{2})-', x))
        for s in [r['first_snapshot']] + [x for x in snaps if x != r['first_snapshot'] and day_of(x) >= (r['first_listed'] or '0000')]:
            h = cr.haystack(s)
            q = find(h, r['anchor_text']) if h else ''
            if q:
                cite = s; break
        how['first' if cite == r['first_snapshot'] else ('other' if cite else 'unbound')] += 1
        k = H.key(r['url'])
        if k not in ids:                             # a new piece takes the next id; an id once given is never reused or moved
            ids[k] = (f'CV{max(int(v[0][2:]) for v in ids.values()) + 1:04d}', r['url']); new_ids.append(k)
        out.append([ids[k][0], ids[k][1], r['domain'], r['anchor_text'], r['first_listed'], r['first_snapshot'], cite, q,
                    'yes' if FIRST <= r['first_listed'] <= LAST else 'no'])
    assert len({o[0] for o in out}) == len(out)
    with open(REG, 'a', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows([ids[k][1], ids[k][0]] for k in new_ids)
    print('row ids: kept', len(out) - len(new_ids), '| new', len(new_ids), [ids[k][0] for k in new_ids][:4])
    with open(R / 'coverage_rows.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow(['row_id', 'url', 'domain', 'headline', 'first_listed', 'first_snapshot', 'cited_snapshot', 'passage', 'drawn'])
        w.writerows(out)
    # the first-listing page must hold the address itself: that is what dates the piece
    raw = {}
    missing = []
    for r in out:
        s_ = r[5]
        if s_ not in raw:
            raw[s_] = b''.join(f.read_bytes() for f in sorted((R / 'primary' / s_).glob('body.*'))).decode('utf-8', 'replace')
        u = r[1]
        if not any(v in raw[s_] for v in (u, u.replace('&', '&amp;'), u.split('?')[0])):
            missing.append(r)
    print('address found in its first-listing page:', len(out) - len(missing), 'of', len(out))
    for r in missing[:20]:
        print('  address not in first-listing page:', r[0], r[5], r[1][:110])
    print('pieces', len(out), '| drawn', sum(r[8] == 'yes' for r in out), '| headline found on the first-listing page', how['first'], '| on another saved page', how['other'], '| unbound', how['unbound'])
    for r in out:
        if not r[6]:
            print('  unbound:', r[4], r[2], '|', r[3][:90], '|', r[5])


if __name__ == '__main__':
    main()
