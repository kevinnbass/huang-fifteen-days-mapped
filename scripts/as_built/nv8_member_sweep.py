"""Every sitting member of Congress, searched by whole name over the counted articles and over the headlines of the pieces the aggregators
listed (Nov 16, 2026, after the eighth reading: the names searched for the figure came from the readings of the pages, and the saved pages are
about half of the listed pieces). Writes research/nv8_member_sweep.tsv: each member found in at least one counted article or in a listed
headline that is not a saved page, with both counts and whether the name is among those the figure's selection searches.
Stops if a sitting member outside those names reaches three reports.     Run: python3 -I scripts/nv8_member_sweep.py
The roster is the evidence set's table of the 535 members sitting when it was built; two names on it now hold other posts or none (the
Secretary of State, drawn in the figure under that office; a former representative named for another affair) and are marked."""
import sys, csv, json, re, io
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M
R = str(ROOT / 'research') + '/'; P = R + 'primary/'
NOT_SITTING_NOW = {'Marco Rubio': 'Secretary of State since 2025; drawn in the figure under that office', 'Eric Swalwell': 'a former representative; the articles name him for another affair'}
lines = open('EVIDENCE_SETS/congress/research/members_network.csv', encoding='utf-8', errors='replace').read().splitlines(keepends=True)
i = 0
while lines[i].startswith('#'): i += 1
mem = [m for m in csv.DictReader(io.StringIO(''.join(lines[i:]))) if m['cohort'] == 'sitting']
arts = M.articles()
key = lambda u: re.sub(r'^https?://(www\.)?', '', (u or '').split('?')[0].split('#')[0]).rstrip('/').lower()
saved = set()
for r in csv.DictReader(open(R + 'nv8_articles.tsv'), delimiter='\t'):
    try: saved.add(key(json.load(open(P + r['page_id'] + '/meta.json')).get('url')))
    except Exception: pass
cov = [r for r in csv.DictReader(open(R + 'coverage_rows.tsv'), delimiter='\t') if r['drawn'] == 'yes']
known = {s.lower() for s in M.FIRST} | {s.lower() for s in M.NOT_DRAWN}
TITLE = r'(?:Sen(?:ator|\.)?|Rep(?:resentative|\.)?|Congress(?:man|woman)|Speaker|Leader|Chair(?:man|woman)?|Whip)'
out = []
for m in mem:
    name = re.sub(r'\s+(Jr\.?|Sr\.?|II|III|IV)$', '', m['member_name'].strip()); parts = name.replace(',', '').split()
    first, last = parts[0], parts[-1]
    nick = {'Richard': 'Rick|Dick|Rich', 'William': 'Bill|Will', 'Robert': 'Bob|Rob', 'James': 'Jim|Jamie', 'Thomas': 'Tom', 'Michael': 'Mike', 'Daniel': 'Dan', 'Joseph': 'Joe', 'Christopher': 'Chris', 'Charles': 'Chuck|Charlie',
            'Edward': 'Ed', 'Timothy': 'Tim', 'Stephen': 'Steve', 'Steven': 'Steve', 'Benjamin': 'Ben', 'Elizabeth': 'Liz', 'Katherine': 'Katie|Kat', 'Andrew': 'Andy', 'Gregory': 'Greg', 'Donald': 'Don', 'Ronald': 'Ron',
            'Samuel': 'Sam', 'Patrick': 'Pat', 'Peter': 'Pete', 'Raphael': 'Ted', 'Rafael': 'Ted', 'Bernard': 'Bernie', 'Nicholas': 'Nick', 'Matthew': 'Matt', 'Anthony': 'Tony', 'Jeffrey': 'Jeff', 'Kenneth': 'Ken', 'Lawrence': 'Larry',
            'Alexander': 'Alex', 'Jonathan': 'Jon', 'Zachary': 'Zach', 'Frederick': 'Fred', 'Douglas': 'Doug', 'Russell': 'Russ', 'Randall': 'Randy', 'Theodore': 'Ted', 'Margaret': 'Maggie', 'Deborah': 'Debbie', 'Suzanne': 'Suzan'}.get(first, '')
    f = re.escape(first) + ('|' + nick if nick else '')
    rx = re.compile(rf"(?<![A-Za-z])(?:(?:{f})\s+(?:[A-Z]\.\s+|\"[^\"]+\"\s+|[A-Z][a-z]+\s+)?{re.escape(last)}|{TITLE}\s+{re.escape(last)})(?![A-Za-z])")
    a = {aid for aid, copies in arts.items() if any(rx.search(t) for _, t in copies)}
    h = [r for r in cov if rx.search(r['headline']) and key(r['url']) not in saved]
    out.append((m['member_name'], m['chamber'], m['party'], len(a), len(h), last.lower() in known, sorted(a)[:6], [x['domain'] for x in h][:4]))
rows = []
for o in sorted(out, key=lambda x: (-(x[3] + x[4]), x[0])):
    if o[3] + o[4] == 0:
        continue
    note = NOT_SITTING_NOW.get(o[0], '')
    rows.append([o[0], o[1], o[2], o[3], o[4], 'yes' if o[5] else 'no', note])
    assert o[5] or note or o[3] + o[4] < 3, ('a sitting member outside the names searched is in three or more reports', o[:5])
with open(R + 'nv8_member_sweep.tsv', 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['member', 'chamber', 'party', 'counted_articles_naming', 'listed_headlines_naming_not_saved', 'among_names_searched', 'note']); w.writerows(rows)
print(len(out), 'sitting members searched;', len(rows), 'found in an article or a headline;', sum(1 for r in rows if r[5] == 'no' and not r[6]), 'outside the names searched, none at three:',
      max((r[3] + r[4] for r in rows if r[5] == 'no' and not r[6]), default=0), 'at most')
