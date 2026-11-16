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
# A title before the surname counts as the member's when the words between them are none or the member's own given name, and a bare
# "Sen. X" or "Rep. X" only when one sitting member of that chamber has the surname (the ninth reading, Nov 16, 2026: the first sweep
# searched the roster's legal given name, so it found Rep. Crawford, whom the pages call Rick, in 5 articles where the figure counts 65).
SEN = r"(?:Sens?\.|Senators?)"; REP = r"(?:Reps?\.|Representatives?|Congress(?:man|woman))"; OTHER = r"(?:(?:Majority|Minority|Democratic|Republican)\s+Leader|Leader|Whip|Speaker|Chair(?:man|woman)?|Ranking\s+Member)"
clean = lambda n: re.sub(r',?\s+(Jr\.?|Sr\.?|II|III|IV)$', '', re.sub(r'\s*["“][^"”]+["”]\s*', ' ', n.strip())).replace(',', '').split()
by_last = {}
for m in mem:
    by_last.setdefault(clean(m['member_name'])[-1], []).append(m['chamber'])
out = []; drawn_sets = {}
for m in mem:
    parts = clean(m['member_name']); quoted = re.findall(r'["“]([^"”]+)["”]', m['member_name'])
    first, last = parts[0], parts[-1]
    nick = {'Richard': 'Rick|Dick|Rich', 'William': 'Bill|Will', 'Robert': 'Bob|Rob', 'James': 'Jim|Jamie', 'Thomas': 'Tom', 'Michael': 'Mike', 'Daniel': 'Dan', 'Joseph': 'Joe', 'Christopher': 'Chris', 'Charles': 'Chuck|Charlie',
            'Edward': 'Ed', 'Timothy': 'Tim', 'Stephen': 'Steve', 'Steven': 'Steve', 'Benjamin': 'Ben', 'Elizabeth': 'Liz', 'Katherine': 'Katie|Kat', 'Andrew': 'Andy', 'Gregory': 'Greg', 'Donald': 'Don', 'Ronald': 'Ron',
            'Samuel': 'Sam', 'Patrick': 'Pat', 'Peter': 'Pete', 'Raphael': 'Ted', 'Rafael': 'Ted', 'Bernard': 'Bernie', 'Nicholas': 'Nick', 'Matthew': 'Matt', 'Anthony': 'Tony', 'Jeffrey': 'Jeff', 'Kenneth': 'Ken', 'Lawrence': 'Larry',
            'Alexander': 'Alex', 'Jonathan': 'Jon', 'Zachary': 'Zach', 'Frederick': 'Fred', 'Douglas': 'Doug', 'Russell': 'Russ', 'Randall': 'Randy', 'Theodore': 'Ted', 'Margaret': 'Maggie', 'Deborah': 'Debbie', 'Suzanne': 'Suzan'}.get(first, '')
    f = '|'.join([re.escape(first)] + ([nick] if nick else []) + [re.escape(q) for q in quoted])
    L_ = re.escape(last); same = by_last[last]
    bare = [OTHER] if len(same) == 1 else []                                    # a bare office title, only for a surname no other sitting member has
    bare += [SEN] if same.count('Senate') == 1 and m['chamber'] == 'Senate' else []
    bare += [REP] if same.count('House') == 1 and m['chamber'] == 'House' else []
    forms = [rf"(?:{f})\s+(?:[A-Z]\.\s+|\"[^\"]+\"\s+|[A-Z][a-z]+\s+)?{L_}", rf"(?:{SEN}|{REP}|{OTHER})\s+(?:{f})\s+(?:[A-Z]\.\s+)?{L_}"] + [rf"{t}\s+{L_}" for t in bare]
    rx = re.compile(r"(?<![A-Za-z])(?:" + '|'.join(forms) + r")(?![A-Za-z])")
    a = {aid for aid, copies in arts.items() if any(rx.search(t) for _, t in copies)}
    h = [r for r in cov if rx.search(r['headline']) and key(r['url']) not in saved]
    out.append((m['member_name'], m['chamber'], m['party'], len(a), len(h), last.lower() in known, sorted(a)[:6], [x['domain'] for x in h][:4]))
    if last in M.FIRST and (first in M.FIRST[last] or set(quoted) & set(M.FIRST[last]) or set(nick.split('|')) & set(M.FIRST[last])):
        drawn_sets[last] = a
# control added after the tenth reading (Nov 16, 2026): the figure's own matcher (member_mentions) and these wider forms must find the same
# articles for every member drawn; the reading found two articles that give a representative's legal given name, which the matcher did not hold
_, fig_hit, _ = M.count()
assert set(drawn_sets) == set(M.FIRST), ('a drawn member is not found on the roster under the names the figure searches', sorted(set(M.FIRST) ^ set(drawn_sets)))
apart = {s: (sorted(drawn_sets[s] - set(fig_hit[s]))[:5], sorted(set(fig_hit[s]) - drawn_sets[s])[:5]) for s in M.FIRST if drawn_sets[s] != set(fig_hit[s])}
assert not apart, ('the figure\'s matcher and the sweep find different articles for a drawn member (sweep only, matcher only)', apart)
print('drawn members:', len(drawn_sets), 'the figure\'s matcher and the sweep find the same articles for each')
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
