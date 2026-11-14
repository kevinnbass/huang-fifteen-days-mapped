"""For each piece on the story, the saved aggregator page that dates it.
Run: python3 -I scripts/build_coverage_days.py -> research/coverage_day_pages.tsv
A piece's day in the figure is the earliest day on which a timed capture of an aggregator's front page lists its address
(research/harvest.tsv, column first_listed; scripts/harvest_links.py). A permalink page of one story can grow after its
date, so it never dates a piece. This table names, for each piece, the earliest timed capture that lists it, so the day
can be checked against one page. It reads the same saved pages with the harvest's own rules and stops if any day it
finds differs from the harvest's."""
import csv, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import harvest_links as H


def main():
    first = {}                                  # address key -> (day, capture id): the earliest timed capture that lists it
    snaps = [d for d in H.snapshots() if H.day(d.name)]
    for d in sorted(snaps, key=lambda d: (H.day(d.name), H.TIMED.search(d.name).group(3), d.name)):
        for k, dom, h, t in H.links(d):
            first.setdefault(k, (H.day(d.name), d.name))
    meta = {d.name: json.loads((d / 'meta.json').read_text()) for d in snaps}
    out = []; bad = []
    for r in csv.DictReader(open(R / 'coverage_rows.tsv', newline=''), delimiter='\t'):
        w = first.get(H.key(r['url']))
        if (w[0] if w else '') != r['first_listed']:
            bad.append((r['row_id'], r['first_listed'], w))
            continue
        m = meta[w[1]] if w else {}
        out.append({'row_id': r['row_id'], 'url': r['url'], 'first_listed': r['first_listed'], 'day_page': w[1] if w else '', 'day_page_url': m.get('url', ''),
                    'day_page_saved_utc': m.get('fetched_utc') or m.get('saved_utc') or ''})
    assert not bad, ('the day found here differs from the harvest\'s', len(bad), bad[:5])
    with open(R / 'coverage_day_pages.tsv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
    dated = [o for o in out if o['day_page']]
    print(f'{len(out):,} pieces; {len(dated):,} dated by a timed capture ({len({o["day_page"] for o in dated})} captures of {len(snaps)} read); {len(out) - len(dated)} seen on no timed capture')


if __name__ == '__main__':
    main()
