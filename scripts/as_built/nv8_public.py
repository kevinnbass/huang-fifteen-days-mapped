"""The rows behind the map figure (nv8, "Fifteen days, mapped"), as a reader or an auditor needs them: for each row the words
the figure draws, the sources it cites and the passage a script has found in each. Used by the audit lane and the public copy.
Run: python3 -I scripts/nv8_public.py     (prints counts)
Donors and lobbyists are never named here: a gift is cited by its FEC identifiers or by a table row."""
import csv, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import nv13_public as P
import rows_context, rows_coverage, rows_events, rows_map, rows_people, rows_ties

STEM = 'nv8-fifteen-days-mapped'


def drawn_ids():
    """The row ids the figure rests on: it carries them in an HTML comment at its head."""
    h = (ROOT / 'figures' / (STEM + '.html')).read_text(encoding='utf-8')
    return set(re.search(r'<!-- rows: (.*?) -->', h).group(1).split())


def _l(x):
    return list(x) if isinstance(x, (list, tuple)) else [x]


def figure_rows():
    ids = drawn_ids(); out = []
    ty = {r['row_id']: r for r in csv.DictReader(open(R / 'member_ties.csv', newline=''))}
    def add(r, table, text, **more):
        out.append({'row_id': r['row_id'], 'table': table, **more, 'drawn_text': text, 'src': _l(r['src']), 'q': [str(x) for x in _l(r['q'])]})
    drawn = lambda mod: [r for r in mod.rows() if r['row_id'] in ids]
    for r in drawn(rows_coverage):
        add(r, 'piece listed by an aggregator', f"{r['headline']} ({r['domain']})", url=r['url'], first_listed=r['first_listed'])
    for r in drawn(rows_map):
        if r['row_id'].startswith('MA'):
            add(r, 'dated act of an actor', r['what'], actor=r['actor'], date=r['date'], reported_by_others=r['reported'])
        else:
            add(r, 'tie between two actors', f"{r['a']} and {r['b']}: {r['label']}", a=r['a'], b=r['b'], kind=r['kind'])
    for r in drawn(rows_people):
        add(r, 'tie in the network at left', f"{r['a']} and {r['b']}: {r['label']}", a=r['a'], b=r['b'], kind=r['kind'])
    for r in drawn(rows_context):
        if r['row_id'].startswith('ST'):
            add(r, 'background of a group of actors', f"{r['group']}. Background: {r['before']} During the fortnight: {r['during']} No document here shows: {r['gap']}")
        elif r['row_id'].startswith('RU'):
            add(r, 'dated event before the fortnight', r['text'], date=r['date'])
        else:
            add(r, 'note', r['note'])
    for r in drawn(rows_events):
        add(r, 'dated event', f"{r['who']}: {r['text']}", date=r['date'])
    for r in drawn(rows_ties):
        t = ty.get(r['row_id'])
        if t:
            add(r, 'tie of a member of Congress', t['words'], member=t['member'], type=t['type'], side=t['side'], usd=t['usd'], first=t['first'], last=t['last'])
        else:
            add(r, 'count across Congress', f"{r.get('side', '')}: gifts from the company's employees across the 535 sitting members", side=r.get('side', ''))
    assert {r['row_id'] for r in out} == ids, (len(out), len(ids), sorted(ids - {r['row_id'] for r in out})[:5])
    return out


def evidence():
    return P.evidence(figure_rows())


if __name__ == '__main__':
    from collections import Counter
    rows = figure_rows(); print('rows', len(rows), dict(Counter(r['table'] for r in rows)))
    ev = evidence(); print('evidence lines', len(ev), dict(Counter(e['kind'] for e in ev)))
    print('without a url (not a repository table):', sum(1 for e in ev if not e['url'] and e['kind'] != 'table in this repository'))
    for e in ev:
        if not e['url'] and e['kind'] != 'table in this repository':
            print('  no url:', e['row_id'], e['source_ref'])
