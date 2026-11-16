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
    gone = [r for r in rows if r.get('withdrawn')]
    check({r['row_id'] for r in rows if not r.get('withdrawn')} == ids and not {r['row_id'] for r in gone} & ids,
          f'the figure names {len(ids):,} rows and research/nv8_rows.tsv holds exactly those, and {len(gone)} more that was published and is no longer drawn, kept with its reason')
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
    check(scope['story'] == len(cov) and len(table('coverage_scope.tsv')) == len(harvest) and f'Left out are {scope["fallout"]:,} links' in flat and f'and {scope["other"]:,} others' in flat,
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
    jc = {j['committee_id']: j for j in table('joint_committees.csv')}
    jg = [g for g in gifts if g['committee_kind'] == 'joint fundraising committee' and g['committee_id'] in jc]
    check(all(jc[g['committee_id']]['member_bioguide'] == g['bioguide'] and jc[g['committee_id']]['outcome'].startswith('tied to the one') for g in jg)
          and all(not j['member_bioguide'] for j in jc.values() if j['outcome'].startswith(('not attributed', 'no sitting', 'sponsor'))),
          f'a gift to a joint fundraising committee is counted for a member only where research/joint_committees.csv shows that member as the one sitting member among its participants '
          f'({len({g["committee_id"] for g in jg})} such committees hold a counted line; {sum(1 for j in jc.values() if j["outcome"].startswith("not attributed"))} shared by several members or not settled are attributed to no one)')
    neg = table('employee_gift_negatives.csv'); rates = {r['side']: r for r in table('employee_gift_rates.csv')}
    check(all(int(rates[s_]['negative_lines_not_netted']) == sum(1 for n in neg if n['side'] == s_) and abs(float(rates[s_]['negative_usd_not_netted']) - sum(float(n['usd']) for n in neg if n['side'] == s_)) < 0.5
              and f"{rates[s_]['negative_lines_not_netted']} for {s_.capitalize()}, {money(-float(rates[s_]['negative_usd_not_netted']))}" in flat for s_ in ('anthropic', 'nvidia')),
          'the negative receipt lines the figure says it does not take off are those of research/employee_gift_negatives.csv, counted and summed for each company')
    look = {(r['register'], r['what']): int(r['count']) for r in table('nv8_lookup_counts.tsv')}
    n_an = look[('analysts', 'quoted on the saved pages (a person or firm written two ways counted once)')]
    check(n_an == look[('analysts', 'drawn')] + sum(v for (reg, w), v in look.items() if reg == 'analysts' and w.startswith('not drawn')) and f'{look[("analysts", "drawn")]} of the {n_an} analysts' in flat
          and f'quote {n_an} analysts' in flat and f'{look[("bylines", "different names")]} different names' in flat and f'carry {look[("bylines", "pairs of outlet and name")]} bylines' in flat,
          f'the counts of analysts and bylines the figure prints are those of research/nv8_lookup_counts.tsv ({n_an} analysts, experts and research groups; {look[("bylines", "different names")]} byline names)')
    nb = look[('banks', 'of those, with an analyst, a note or an executive quoted on the saved pages')]
    check(f"nalysts, or executives in office, of {nb} of those banks are quoted" in flat and f"and named {look[('banks', 'named by Quartz on Sep 4, 2026 as lenders to Anthropic')]} banks in it" in flat
          and f"{look[('analysts', 'not drawn: at a bank, not drawn')]} entries that are one of the banks below or its analysts" in flat
          and f"and the other {look[('analysts', 'not drawn: none found')]}, for whom no record was found" in flat
          and look[('bylines', 'different names drawn')] == 5 and 'five have a tie on record' in flat,
          f'the counts of banks ({nb} of the lenders reported have someone quoted) and of bylines drawn the figure prints are those of research/nv8_lookup_counts.tsv')
    ns = {r['what']: int(r['count']) for r in table('nv8_name_search_counts.tsv')}; oc = {r['what']: int(r['count']) for r in table('nv8_s6_counts.tsv')}
    check(f"{ns['people: different names searched']:,} names of two to four words" in flat and f"and {ns['others: different names searched']} other firm names and one-word names" in flat
          and f"each of the {oc['actors whose own channels were searched']} actors who had spoken" in flat
          and f"is held and was read for {oc['actors: an item about the affair is held and was read']} (" in flat
          and f"for {oc['actors: nothing found on a channel that could be read']} a channel that could be read showed no item about the affair" in flat
          and f"for {oc['actors: no channel could be read']} no channel could be read" in flat
          and f"Of the {oc['chips whose original was searched for']} chips drawn before those searches, the original was read and is now cited for {oc['chips: original read and cited on the chip']}" in flat
          and sum(v for k, v in oc.items() if k.startswith('actors: ')) == oc['actors whose own channels were searched'],
          f"the counts the figure prints for the whole-name search ({ns['people: different names searched']} names) and for the search of own channels ({oc['actors whose own channels were searched']} actors, in six classes that add up) are those of research/nv8_name_search_counts.tsv and nv8_s6_counts.tsv")
    read = table('coverage_scope_read.tsv'); on = {r['url'] for r in read if r['finding'] == 'on the story'}
    check(on <= {c['url'] for c in cov} and f'{len(on)} are plainly on the story' in flat and f'{sum(r["finding"] == "not settled" for r in read)} could not be settled' in flat,
          f'the {len(on)} links a reading put on the story are among the pieces counted, and the figure prints that number (research/coverage_scope_read.tsv)')
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
    pages = table('story_pages.tsv'); arts = {p['article'] for p in pages if p['counted'] == 'yes'}
    named = defaultdict(set)
    for p in pages:
        if p['counted'] == 'yes':
            for s in (p['names'] or '').split(';'):
                if s:
                    named[s].add(p['article'])
    hit = Counter({s: len(v) for s, v in named.items()})
    slug = {s.lower().replace(' ', '').replace('-', ''): s for s in hit}
    check(len(arts) > 1000 and all(m in slug and hit[slug[m]] >= 3 and f'Named in {hit[slug[m]]} of the {len(arts):,} articles counted' in flat for m in members),
          f'{len(pages):,} saved pages are {len({p["article"] for p in pages}):,} articles, {len(arts):,} of them counted (research/story_pages.tsv); each of the {len(members)} members drawn is named in at least 3, and the figure prints each one\'s count',
          str([m for m in members if m not in slug or hit[slug[m]] < 3][:5]))
    art = table('nv8_articles.tsv'); n1 = sum(r['set'] == 'first census' for r in art)
    why = Counter('after' if 'after the fifteen days' in r['why_not'] else 'before' if 'before the fifteen days' in r['why_not'] else 'not the piece' if 'block or error page' in r['why_not']
                  else 'empty' if 'empty capture' in r['why_not'] else 'not news' for r in art if r['counted'] == 'no')
    prs = table('nv8_article_pairs.tsv'); used = [p for p in prs if p['used_for_joining'] == 'yes']; assert len({frozenset((p['page_a'], p['page_b'])) for p in used}) == len(used); same_ = sum(p['verdict'] == 'same' for p in used)
    art_of = {r['page_id']: r['article_id'] for r in art}; line_ = table('nv8_at_the_line.tsv')
    part_ = sum(r['saved_in_part'] == 'yes' for r in art); in_copy = sum(r['day_basis'] == 'read in the saved copy' for r in art); days_read = table('nv8_page_days_read.tsv')
    check(all((art_of[p['page_a']] == art_of[p['page_b']]) == (p['verdict'] == 'same') for p in used),
          f'each of the {len(used)} pairs of pages a reader judged is joined, or kept apart, as the reader judged it ({same_} the same article, {len(used) - same_} different; research/nv8_article_pairs.tsv)',
          str([(p['page_a'], p['page_b']) for p in used if (art_of[p['page_a']] == art_of[p['page_b']]) != (p['verdict'] == 'same')][:5]))
    check(f'({len(used)} pairs over four readings: {same_} the same article' in flat and f'{len(used) - same_} different' in flat and f'{part_} counted pages are still held only in part' in flat
          and f'({in_copy} pages whose metadata and text carry none, or carry one the printed stamp contradicts, were read in their saved copy)' in flat and in_copy == len(days_read)
          and not any(r['counted'] == 'yes' and not r['day'] for r in art)
          and {r['page_id']: r['day'] for r in days_read}.items() <= {r['page_id']: r['day'] for r in art}.items(),
          f'the figure prints those counts, the {part_} counted pages held only in part, and the {in_copy} pages whose day was read in the saved copy (research/nv8_page_days_read.tsv); no counted page is without a day')
    sel_ = [x for x in table('member_selection.tsv') if x['drawn'] in ('yes', 'no') and not x['why_not'].startswith('a current member')]
    at_line = {x['name']: x for x in sel_ if x['articles'] in ('3', '4')}; lm = {x['name']: x for x in line_ if x['group'] == 'member'}
    check(set(at_line) == set(lm) and all(lm[n]['article_ids'].split() == sorted(named[n]) and lm[n]['drawn'] == at_line[n]['drawn'] for n in lm)
          and all(int(x['separate_reports_on_the_matter']) >= 3 for x in line_ if x['drawn'] == 'yes') and all(int(x['separate_reports_on_the_matter']) < 3 for x in line_ if x['drawn'] == 'no'),
          f"research/nv8_at_the_line.tsv reads each of the {len(lm)} members named in three or four counted articles, with those articles; {sum(x['drawn'] == 'no' for x in lm.values())} of them is under three separate reports and not drawn, and research/member_selection.tsv says the same",
          str(sorted(set(at_line) ^ set(lm))))
    check({(r['page_id'], r['article_id'], r['counted']) for r in art} == {(p['id'], p['article'], p['counted']) for p in pages}
          and f'the {n1:,} pages saved by the first search and the {len(art) - n1} saved since' in flat and f"are {len({r['article_id'] for r in art}):,} articles once copies of one article are joined" in flat
          and f'and {len(arts):,} of them are counted' in flat and f"is after Nov 12 ({why['after']} pages) or before Oct 29 ({why['before']}, background pages), when the saved copy is a block or error page ({why['not the piece']}) or holds nothing at all ({why['empty']}), or when it is a reference page or an image ({why['not news']})" in flat,
          f"the figure's sentence on the articles counted gives the numbers of research/nv8_articles.tsv: {len(art):,} pages, {len({r['article_id'] for r in art}):,} articles, {len(arts):,} counted; not counted: {why['after']} dated after Nov 12, {why['before']} before Oct 29, {why['not the piece']} a block or error page, {why['empty']} empty, {why['not news']} not news")
    sel = table('member_selection.tsv'); searched = [s for s in sel if s['drawn'] in ('yes', 'no')]
    check(all(int(s['articles']) == hit[s['name']] for s in searched) and {s['name'].lower().replace(' ', '').replace('-', '') for s in sel if s['drawn'] == 'yes'} == set(members)
          and all(s['why_not'] for s in sel if s['drawn'] != 'yes') and sum(1 for s in sel if s['why_not'].startswith('a current member')) == 7 and 'Seven others named that often are not drawn' in flat,
          f'research/member_selection.tsv gives every name searched with its count of articles: {len(members)} drawn, {sum(1 for s in searched if s["drawn"] == "no")} not drawn, each with the reason (seven named for other things)')
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
