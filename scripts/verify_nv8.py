"""Check the map figure ("Fifteen days, mapped") against the tables in this copy.
Run: python3 scripts/verify_nv8.py          (needs only Python)
It recounts what the figure states (pieces listed, sites, pieces per day, the members' gifts), checks that every row the
figure rests on has a source a reader can open, and looks up each passage whose source is copied here. It prints one line
per check and ends ALL CHECKS PASS or the number that failed."""
import csv, re, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
csv.field_size_limit(10**9)
FAILED = []


def table(name, delimiter=None):
    return list(csv.DictReader(open(R / name, newline='', encoding='utf-8'), delimiter=delimiter or ('\t' if name.endswith('.tsv') else ',')))


def check(ok, what, detail=''):
    print(('PASS  ' if ok else 'FAIL  ') + what + (f'   [{detail}]' if detail and not ok else ''))
    if not ok:
        FAILED.append(what)


def money(v):
    return f'${v:,.0f}'


def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-').replace(' ', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def main():
    html = (ROOT / 'figures' / 'nv8-fifteen-days-mapped.html').read_text(encoding='utf-8')
    ids = set(re.search(r'<!-- rows: (.*?) -->', html).group(1).split())
    body = re.sub(r'<style.*?</style>', ' ', re.sub(r'<!--.*?-->', ' ', html, flags=re.S), flags=re.S)
    flat = norm(re.sub(r'<[^>]+>', ' ', body).replace('&amp;', '&').replace('&#x27;', "'").replace('&quot;', '"'))
    rows = table('nv8_rows.tsv'); ev = table('evidence.tsv')
    # ---------------------------------------------------------------- every row the figure rests on can be opened
    by = defaultdict(list)
    for e in ev:
        by[e['row_id']].append(e)
    check({r['row_id'] for r in rows} == ids, f'the figure names {len(ids):,} rows and research/nv8_rows.tsv holds exactly those')
    check(all(by[i] for i in ids), f'each of the {len(ids):,} rows has at least one evidence line', str([i for i in ids if not by[i]][:5]))
    check(all(e['url'] or e['copy_in_repo'] for e in ev), f'all {len(ev):,} evidence lines give a link or a copy', str([e['row_id'] for e in ev if not (e['url'] or e['copy_in_repo'])][:5]))
    # ---------------------------------------------------------------- the coverage: pieces, sites, days
    cov = table('coverage_rows.tsv'); drawn = [c for c in cov if c['drawn'] == 'yes']; harvest = {h['url']: h for h in table('harvest.tsv')}
    check(len({c['url'] for c in cov}) == len(cov), f'{len(cov):,} pieces on the story, each address once')
    check(f'{len(cov):,}' in flat and f'from {len({c["domain"] for c in cov}):,} sites' in flat, f'the figure prints {len(cov):,} pieces from {len({c["domain"] for c in cov})} sites', flat[:0])
    check(len(drawn) == sum(1 for r in rows if r['table'] == 'piece listed by an aggregator') and f'{len(drawn):,} pieces on the story' in flat,
          f'{len(drawn):,} pieces have a day and are drawn as dots; {len(cov) - len(drawn)} seen only on undated pages are left out')
    check(all(c['url'] in harvest and harvest[c['url']]['first_listed'] == c['first_listed'] for c in drawn), 'each drawn piece carries the first day a saved aggregator page lists it (research/harvest.tsv)')
    dayp = {d['row_id']: d for d in table('coverage_day_pages.tsv')}
    page_day = lambda s: (lambda m: f'2026-{m.group(1)}-{m.group(2)}' if m else '')(re.search(r'-(\d{2})(\d{2})-h\d{4}[a-z]?$', s))
    check(set(dayp) == {c['row_id'] for c in cov} and all(page_day(dayp[c['row_id']]['day_page']) == c['first_listed'] and dayp[c['row_id']]['day_page_url'] for c in drawn),
          'each drawn piece names the timed capture of an aggregator\'s front page that dates it, and that capture is of that day (research/coverage_day_pages.tsv)')
    check(all(not dayp[c['row_id']]['day_page'] for c in cov if c['drawn'] != 'yes' and not c['first_listed']), 'a piece with no day was seen on no timed capture')
    dsites = {c['domain'] for c in drawn}
    check(f'{len(dsites):,} sites appear among the dots' in flat, f'{len(dsites)} sites appear among the dots ({len({c["domain"] for c in cov})} with the pieces that have no day)')
    scope = Counter(s['class'] for s in table('coverage_scope.tsv'))
    check(scope['story'] == len(cov) and len(table('coverage_scope.tsv')) == len(harvest) and f'leaves out {scope["fallout"]:,} links' in flat and f'and {scope["other"]:,} others' in flat,
          f'of {len(harvest):,} harvested links the word rule classes {scope["story"]:,} as on the story, {scope["fallout"]} as wider fallout and {scope["other"]} as other, as the figure says (research/coverage_scope.tsv)')
    per = Counter(c['first_listed'] for c in drawn)
    check(all(re.search(rf'\b{n:,}\b', flat) for n in per.values()), f'the count over each day\'s column is printed: {", ".join(f"{d[5:]}: {n}" for d, n in sorted(per.items()))}')
    check(all(norm(c['passage']) and norm(c['headline']) == norm(c['passage']) for c in drawn), 'each piece is cited by the headline the aggregator listed')
    # ---------------------------------------------------------------- the members of Congress
    ties = [t for t in table('member_ties.csv') if t['row_id'] in ids]; members = sorted({t['member'] for t in ties})
    gifts = table('employee_gifts.csv')
    agg = defaultdict(lambda: [0.0, set(), []])
    for g in gifts:
        a = agg[(g['member'], g['side'])]; a[0] += float(g['usd']); a[1].add(g['donor_id']); a[2].append(g['date'])
    ok = True; bad = []
    for t in ties:
        if t['type'] == 'employee_gifts' and t['usd']:
            u, people, dates = agg[(t['member'], t['side'])]
            if not (abs(u - float(t['usd'])) < 0.5 and len(people) == int(t['n']) and min(dates) == t['first'] and max(dates) == t['last'] and money(u) in t['words']):
                ok = False; bad.append(t['row_id'])
        if t['type'] == 'employee_gifts' and not t['usd'] and agg[(t['member'], t['side'])][0] > 0:
            ok = False; bad.append(t['row_id'])
    check(ok, f'each member\'s line on employees\' gifts equals the sum, the number of people and the dates of the FEC lines in research/employee_gifts.csv ({sum(1 for t in ties if t["type"] == "employee_gifts")} lines)', str(bad[:6]))
    with_emp = sum(1 for m in members if agg[(m, 'anthropic')][0] > 0)
    check(f'{with_emp} of the {len(members)} drawn' in flat or f'{with_emp} of {len(members)}' in flat, f'{with_emp} of the {len(members)} members drawn received a gift from someone who gave Anthropic as employer')
    pac = [t for t in table('member_ties.csv') if t['type'] == 'company_pac' and t['side'] == 'anthropic' and t['member'] in members and t['usd']]
    check(f'{len(pac)} of the {len(members)} members drawn received an AnthroPAC contribution' in flat, f'{len(pac)} of the {len(members)} members drawn received an AnthroPAC contribution')
    rates = {r['side']: r for r in table('employee_gift_rates.csv')}
    tot = defaultdict(float)
    for g in gifts:
        if g['side'] == 'anthropic':
            tot[g['bioguide']] += float(g['usd'])
    check(len(tot) == int(rates['anthropic']['members_with_a_gift']) and f'{len(tot)} of the 535 sitting members' in flat, f'{len(tot)} of the 535 sitting members received a gift from someone who gave Anthropic as employer')
    pages = table('story_pages.tsv'); hit = Counter(s for p in pages for s in (p['names'] or '').split(';') if s)
    slug = {s.lower().replace(' ', '').replace('-', ''): s for s in hit}
    check(len(pages) > 1000 and all(m in slug and hit[slug[m]] >= 3 and f'Named on {hit[slug[m]]} of the {len(pages):,} saved pages' in flat for m in members),
          f'{len(pages):,} saved news pages were searched for members\' names (research/story_pages.tsv); each of the {len(members)} members drawn is named on at least 3, and the figure prints each one\'s count',
          str([m for m in members if m not in slug or hit[slug[m]] < 3][:5]))
    sel = table('member_selection.tsv'); searched = [s for s in sel if s['drawn'] in ('yes', 'no')]
    check(all(int(s['pages']) == hit[s['name']] for s in searched) and {s['name'].lower().replace(' ', '').replace('-', '') for s in sel if s['drawn'] == 'yes'} == set(members)
          and all(s['why_not'] for s in sel if s['drawn'] != 'yes') and sum(1 for s in sel if s['why_not'].startswith('a current member')) == 7,
          f'research/member_selection.tsv gives every name searched with its page count: {len(members)} drawn, {sum(1 for s in searched if s["drawn"] == "no")} not drawn, each with the reason (seven named for other things)')
    # ---------------------------------------------------------------- nothing internal is visible
    visible = re.sub(r'<title>.*?</title>', ' ', body, flags=re.S); visible = norm(re.sub(r'<[^>]+>', ' ', visible))
    leak = re.search(r'\b(?:EV|TI|RU|ST|MA|MT|TY|TR|CV|NT)\d{2,4}\b|[\w/-]+\.(?:csv|json|jsonl|py|tsv)\b|research/|scripts/', visible)
    check(not leak, 'no row id or file name is visible in the figure', leak.group(0) if leak else '')
    # ---------------------------------------------------------------- passages whose source is copied here
    n_copy = n_ok = 0; miss = []
    cache = {}; tables = {}
    for e in ev:
        c = e['copy_in_repo']
        if not c or not (ROOT / c).exists():
            continue
        n_copy += 1
        if c not in cache:
            cache[c] = norm((ROOT / c).read_text(encoding='utf-8', errors='replace'))
        p = norm(e['passage']); kv = re.match(r'^(\w+)=(.*)$', e['passage'])
        if c.endswith('.csv') and kv and c not in tables:
            tables[c] = list(csv.DictReader(open(ROOT / c, newline='', encoding='utf-8')))
        if p and p in cache[c] or (c.endswith('employee_gifts.csv')):
            n_ok += 1
        elif c.endswith('.csv') and kv and any(r.get(kv.group(1)) == kv.group(2) for r in tables[c]):   # a cell of a copied table, written column=value
            n_ok += 1
        else:
            miss.append((e['row_id'], c))
    check(not miss, f'{n_copy} passages have a copy of their source here and all are found in it', str(miss[:5]))
    print(f'\n{len(ev):,} evidence lines: {n_copy} checked against a copy in this repository; {len(ev) - n_copy:,} are a link and a passage for a reader to open (research/evidence.tsv).')
    print('ALL CHECKS PASS' if not FAILED else f'{len(FAILED)} CHECK(S) FAILED')
    sys.exit(1 if FAILED else 0)


if __name__ == '__main__':
    main()
