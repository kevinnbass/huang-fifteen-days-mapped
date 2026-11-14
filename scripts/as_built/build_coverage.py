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
import check_rows as cr, story_scope
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
    ids = {r['url']: r['row_id'] for r in csv.DictReader(open(REG, newline=''))}; new_ids = []
    for r in csv.DictReader(open(R / 'harvest.tsv', newline=''), delimiter='\t'):
        if story_scope.scope(r['url'], r['anchor_text']) != 'story':
            continue
        cite, q = '', ''
        for s in [r['first_snapshot']] + [x for x in snaps if x != r['first_snapshot']]:
            h = cr.haystack(s)
            q = find(h, r['anchor_text']) if h else ''
            if q:
                cite = s; break
        how['first' if cite == r['first_snapshot'] else ('other' if cite else 'unbound')] += 1
        if r['url'] not in ids:                      # a new address takes the next id; an id once given is never reused or moved
            ids[r['url']] = f'CV{max(int(v[2:]) for v in ids.values()) + 1:04d}'; new_ids.append(r['url'])
        out.append([ids[r['url']], r['url'], r['domain'], r['anchor_text'], r['first_listed'], r['first_snapshot'], cite, q,
                    'yes' if FIRST <= r['first_listed'] <= LAST else 'no'])
    assert len({o[0] for o in out}) == len(out)
    with open(REG, 'a', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows([u, ids[u]] for u in new_ids)
    print('row ids: kept', len(out) - len(new_ids), '| new', len(new_ids), [ids[u] for u in new_ids][:8])
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
