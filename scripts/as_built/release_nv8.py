"""Assemble the public copy of the map figure (nv8, "Fifteen days, mapped") in a folder outside the project.
Run: PYTHONDONTWRITEBYTECODE=1 <python with playwright> scripts/release_nv8.py <target folder>
The copy holds the figure, the tables and row files it is drawn from, a link and a passage for every source, copies of the
official records it cites, the audit, and scripts that rebuild and check it. It holds no article text (a news page is a link
and a sentence), no donor's or lobbyist's name, no local path. The script stops if any of those is found, if the figure
rebuilt inside the copy differs from the project's, or if the copy's own checks fail."""
import csv, json, re, shutil, subprocess, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; PRIMARY = R / 'primary'
sys.path.insert(0, str(ROOT / 'scripts'))
import release_nv13 as R13, nv13_public as P, nv8_public as N, member_mentions, rows_map
csv.field_size_limit(10**9)
LANE = Path('lanes/audit_nv8')
RUN = ('fig_map.py', 'fig_common.py', 'rows_map.py', 'rows_people.py', 'rows_context.py', 'rows_coverage.py', 'rows_ties.py', 'rows_events.py', 'story_scope.py', 'nv8_status.py', 'build_nv8.py', 'verify_nv8.py')
AS_BUILT = ('nv8_public.py', 'make_audit_nv8.py', 'release_nv8.py', 'build_lobbying.py', 'build_member_ties.py', 'member_mentions.py', 'harvest_links.py', 'build_coverage.py', 'build_coverage_days.py', 'build_anthropac.py', 'fec_bulk_employer.py', 'fec_sched_a_employer.py', 'nv13_public.py', 'nv8_name_search.py', 'nv8_s6_counts.py', 'nv8_articles.py', 'nv8_page_dates.py', 'fec_lpac_keyed_check.py', 'recover_bodies.py', 'nv8_dense_text.py', 'nv8_at_the_line.py', 'build_lobbyist_gifts_map.py', 'nv8_member_sweep.py', 'recover_bodies_2.py', 'nv8_partial_screen.py', 'recover_bodies_3.py', 'recover_bodies_4.py', 'recover_bodies_5.py', 'recover_bodies_6.py', 'nv8_collapse_screen.py', 'recover_bodies_7.py', 'nv8_live_pages.py', 'recover_bodies_8.py', 'recover_bodies_9.py', 'nv8_actor_days.py', 'nv8_general_news_page.py', 'nv8_report_day_screen.py', 'nv8_remarks_no_chip.py', 'nv8_refusals.py', 'nv8_reading_lanes.py', 'nv8_take_in.py', 'nv8_take_in_r3.py', 'nv8_register_ms.py', 'nv8_blind_spot_population.py')
TABLES = ('harvest.tsv', 'coverage_rows.tsv', 'coverage_day_pages.tsv', 'anthropac_by_recipient.csv', 'anthropac_party.csv', 'member_ties.csv', 'employee_gift_rates.csv', 'committee_keys.csv', 'joint_committees.csv',
          'pacs_by_member.csv', 'chip_bills.csv', 'lobbying_bill_reports.csv', 'lobbying_family_reports.csv', 'employee_gift_negatives.csv', 'coverage_scope_read.tsv', 'nv8_lookup_counts.tsv', 'lobbyist_gifts_map_summary.tsv', 'nv8_remark_verdicts.tsv', 'nv8_name_search_counts.tsv', 'nv8_s6_counts.tsv', 'nv8_s6_items.tsv', 'nv8_articles.tsv', 'nv8_page_days_read.tsv', 'nv8_at_the_line.tsv', 'nv8_recovered_pages.tsv', 'nv8_recovered_pages_2.tsv', 'nv8_pages_added.tsv', 'nv8_member_sweep.tsv', 'nv8_pages_in_part_read.tsv', 'nv8_text_added.tsv', 'nv8_text_trimmed.tsv', 'nv8_collapse_screen.tsv', 'nv8_live_pages.tsv', 'nv8_actor_days.tsv', 'nv8_general_news_page.tsv', 'nv8_report_day_screen.tsv', 'nv8_remarks_no_chip.tsv', 'nv8_refusals.tsv', 'nv8_single_article_remarks.tsv', 'nv8_paraphrased_acts.tsv', 'nv8_earlier_acts.tsv', 'nv8_recalls.tsv', 'nv8_recall_groups.tsv', 'nv8_added_pages_acts.tsv', 'nv8_take_in_groups.tsv', 'nv8_take_in_round3.tsv', 'nv8_blind_spot_population.tsv', 'nv8_population_chips_stage1.tsv', 'nv8_population_chips_stage2.tsv')
SHIM = '''"""Which saved articles name each member of Congress: the counts the figure prints ("named in N of the articles counted").
In the builder's project this module reads the saved pages themselves; they are not in this copy (no article text is), so here
the same answer is read from research/story_pages.tsv, which lists every saved page by address with the article it is a copy of,
whether it is counted, and the members its text names. An article is counted once, whatever the number of its copies."""
import csv
from collections import defaultdict
from pathlib import Path
R = Path(__file__).resolve().parents[1] / 'research'


def count():
    """(articles counted, {surname: [article ids]}, {})"""
    hit = defaultdict(set); arts = set()
    for r in csv.DictReader(open(R / 'story_pages.tsv', newline=''), delimiter='\\t'):
        if r['counted'] != 'yes':
            continue
        arts.add(r['article'])
        for s in (r['names'] or '').split(';'):
            if s:
                hit[s].add(r['article'])
    return len(arts), defaultdict(list, {s: sorted(v) for s, v in hit.items()}), {}
'''
scrub = R13.scrub; put = R13.put; table = R13.table
# the same pattern as the three-chairmen release, except that '/kevin-' inside a news site's address (a writer's page) is not a local path
# (a line of the pattern for local paths; left out of this copy)
# (a line of the pattern for local paths; left out of this copy)
# (a line of the pattern for local paths; left out of this copy)


def main(target):
    Tg = Path(target).resolve(); Tg.mkdir(parents=True, exist_ok=True)
    assert not str(Tg).startswith(str(ROOT)), 'the public copy must not sit inside the project folder'
    # ---------------------------------------------------------------- scripts that run on the copy
    for name in RUN:
        t = (ROOT / 'scripts' / name).read_text()
        if name == 'fig_common.py':
            a = t.index('"""'); b = t.index('"""', a + 3) + 3
            t = ('"""Shared render and tokens for the figure: warm paper background, spaced-caps kicker, bold title, grey subtitle,\n'
                 'legend chips, footnote under a rule. Row ids ride only in an HTML comment.\n'
                 'The page grows to fit its content; the PNG is cut at the measured height."""') + t[b:]
        t = scrub(t); m = PRIVATE.search(t); assert not m, (name, t[max(0, m.start() - 60):m.end() + 40]); put(Tg, f'scripts/{name}', t)
    put(Tg, 'scripts/member_mentions.py', SHIM)
    for name in AS_BUILT:
        if not (ROOT / 'scripts' / name).exists():
            continue
        t = scrub((ROOT / 'scripts' / name).read_text())
        t = re.sub(r"(?m)^.*# local-pattern\n", "# (a line of the pattern for local paths; left out of this copy)\n", t)
        t = re.sub(r"PRIVATE = re\.compile\(.*\n", "PRIVATE = re.compile(r'(a pattern for local paths, a session id and addresses; left out of this copy)')
        t = re.sub(r"(?m)^\s*t = t\.replace\('/mnt.*\n|^\s*t = re\.sub\(r'/home.*\n|^\s*t = re\.sub\(r'Owner: nvidia.*\n", "    # (replacements of local paths; left out of this copy)\n", t)
        m = PRIVATE.search(t); assert not m, (name, t[max(0, m.start() - 60):m.end() + 40])
        put(Tg, f'scripts/as_built/{name}', t)
    # ---------------------------------------------------------------- tables
    for name in TABLES:
        t = (R / name).read_text(); m = PRIVATE.search(t); assert not m, (name, t[max(0, m.start() - 60):m.end() + 40]); put(Tg, f'research/{name}', t)
    # lobbyists' own gifts to the 24 members, all three sides by one rule (slice F1): without the payee and the honoree as written (free text
    # that can name a private person), the pack's row id and the saved page; each gift keeps the address of its official report
    lg = list(csv.DictReader(open(R / 'lobbyist_gifts_map.csv', newline='')))
    lg_cols = [c for c in lg[0] if c not in ('payee', 'honoree_as_written', 'pack_row', 'source')]
    table(Tg, 'research/lobbyist_gifts_map.csv', [{c: r[c] for c in lg_cols} for r in lg], lg_cols, ',')
    # the yearly award rows the figure's grant totals are sums of (rows_map.sums_ok() recomputes each total from them)
    import rows_map as RM
    used = {i for g in RM.GRANTS + RM.GRANTS_V3 + RM.GRANTS_NOTE for i in g[3]}
    ls = open('EVIDENCE_SETS/lineage/research/flows_annual.csv', newline='', errors='replace').read().splitlines(keepends=True)
    while ls[0].startswith('#'):
        ls = ls[1:]
    gr = [r for r in csv.DictReader(ls) if r['row_id'] in used]; assert {r['row_id'] for r in gr} == used and not any(r['person'] for r in gr)
    table(Tg, 'research/grant_rows.csv', gr, ['row_id', 'from_name', 'to_name', 'year', 'amount_usd', 'measure', 'channel', 'url', 'checked_utc'])
    gifts = P.public_gifts()
    for g in gifts:
        g['fec_page_url'] = 'https://docquery.fec.gov/cgi-bin/fecimg/?' + g['image_num']; g['amended_fec_page_url'] = ('https://docquery.fec.gov/cgi-bin/fecimg/?' + g['amended_image_num']) if g['amended_image_num'] else ''
    ck = {r['committee_id']: r for r in csv.DictReader(open(R / 'committee_keys.csv', newline=''))}
    for g in gifts:
        g['member_name'] = ck[g['committee_id']]['member_name']; g['party'] = ck[g['committee_id']]['party']
    table(Tg, 'research/employee_gifts.csv', gifts, P.GIFT_COLS[:3] + ['member_name', 'party'] + P.GIFT_COLS[3:] + ['fec_page_url', 'amended_fec_page_url'])
    rows = N.figure_rows()
    # a row that was published and is no longer drawn stays in the table, with the reason in `withdrawn` (a row id is never reused or dropped)
    for r_ in rows_map.rows():
        if r_.get('withdrawn'):
            role_, names_ = rows_map.WITHDRAWN_PUBLIC.get(r_['actor'], (r_['actor'], {}))
            hide = lambda x: '[a passage that names the person; kept with the project]' if any(n_ in str(x) for n_ in names_) else str(x)
            assert not any(n_ in r_['what'] for n_ in names_)
            rows.append({'row_id': r_['row_id'], 'table': 'dated act of an actor', 'actor': role_, 'date': r_['date'], 'reported_by_others': r_['reported'], 'withdrawn': r_['withdrawn'],
                         'drawn_text': r_['what'], 'src': list(r_['src']), 'q': [hide(x) for x in r_['q']]})
    # the same for the lines of record of a member no longer drawn (the lines are still true of him; they are kept and not drawn)
    import rows_ties
    ty_ = {r['row_id']: r for r in csv.DictReader(open(R / 'member_ties.csv', newline=''))}
    for r_ in rows_ties.rows():
        t_ = ty_.get(r_['row_id'])
        if t_ and t_['member'] in rows_map.WITHDRAWN and t_['draw'] in ('line', 'words'):
            rows.append({'row_id': r_['row_id'], 'table': 'tie of a member of Congress', 'member': t_['member'], 'type': t_['type'], 'side': t_['side'], 'usd': t_['usd'], 'first': t_['first'], 'last': t_['last'],
                         'withdrawn': rows_map.WITHDRAWN[t_['member']], 'drawn_text': t_['words'], 'src': list(r_['src']) if isinstance(r_['src'], (list, tuple)) else [r_['src']],
                         'q': [str(x) for x in (r_['q'] if isinstance(r_['q'], (list, tuple)) else [r_['q']])]})
    # row ids are frozen once published: every id of the last pushed table must still be here, as the same kind of row and, for an act
    # or a tie, about the same actor or the same two ends (a chip added in the middle of a list once shifted three published ids: Nov 15, 2026)
    pushed = ROOT.parent / 'code' / 'huang-fifteen-days-mapped' / 'research' / 'nv8_rows.tsv'      # the builder's clone of the public repository
    if pushed.exists():
        now_ = {r['row_id']: r for r in rows}; moved = []
        for o in csv.DictReader(open(pushed, newline='', encoding='utf-8'), delimiter='\t'):
            if o['table'] == 'piece listed by an aggregator':
                continue
            n_ = now_.get(o['row_id'])
            if n_ is None or n_['table'] != o['table'] or any(str(n_.get(k) or '') != (o.get(k) or '') for k in ('actor', 'a', 'b', 'member', 'type', 'side') if not (k == 'actor' and n_.get('withdrawn'))):
                moved.append(o['row_id'])
        assert not moved, ('a published row id is gone or now names another actor or tie', moved[:12])
    flat = [{k: (' || '.join(v) if isinstance(v, list) else v) for k, v in r.items()} for r in rows]
    cols = ['row_id', 'table', 'drawn_text'] + sorted({k for r in flat for k in r} - {'row_id', 'table', 'drawn_text', 'src', 'q'}) + ['src', 'q']
    table(Tg, 'research/nv8_rows.tsv', flat, cols, '\t')
    # the saved news pages behind "named on N of the saved pages": addresses, and the members each names; no page text
    n_pages, hit, _ = member_mentions.count()                    # since Nov 15, 2026: articles, each counted once
    text_of = {pid: text for copies in member_mentions.articles().values() for pid, text in copies}
    res = {s: member_mentions.member_re(s) for s in member_mentions.FIRST}; nd = {s: member_mentions.not_drawn_re(s) for s in member_mentions.NOT_DRAWN}
    pages = []; nd_art = {s: set() for s in nd}; chk = {s: set() for s in res}
    for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t'):
        pid = r['page_id']; m = json.loads((PRIMARY / pid / 'meta.json').read_text()); names = []
        if r['counted'] == 'yes':
            for s, rx in res.items():
                if rx.search(text_of[pid]):
                    names.append(s); chk[s].add(r['article_id'])
            for s, rx in nd.items():
                if rx.search(text_of[pid]):
                    names.append(s); nd_art[s].add(r['article_id'])
        pages.append({'id': pid, 'url': m.get('url') or '', 'saved_utc': m.get('fetched_utc') or m.get('saved_utc') or '', 'article': r['article_id'], 'counted': r['counted'], 'why_not': r['why_not'], 'names': ';'.join(sorted(names))})
    nd_n = {s: len(v) for s, v in nd_art.items()}
    assert len({p['article'] for p in pages if p['counted'] == 'yes'}) == n_pages and all(len(chk[s]) == len(hit[s]) for s in res), 'the page lines do not give the counts the figure prints'
    table(Tg, 'research/story_pages.tsv', pages, list(pages[0].keys()), '\t')
    # the pairs of pages a reader opened, with the verdict and the kind of relation; the readers' sentences are left out because they name
    # reporters, who are not drawn (the seventh reading's sentences are in audit2/h-counts_check.csv, which names none)
    RELATIONS = ('same article at two addresses', 'syndicated copy', 'licensed copy', 'later version', 'live snapshots', 'same official statement', 'site furniture only', 'shared background',
                 'live page carries the stand-alone report', 'different reports of one event', 'quotes the same document', 'one quotes the other', 'rewrite by another outlet', 'truncated address collision', 'no readable text',
                 'live page carries wire report', 'new lead above an earlier dispatch', 'post promotes the release', 'quotes the same post', 'quotes the same remarks', 'quotes the same report', 'separate daily reports', 'different entries of a series')
    prs = []
    for r in csv.DictReader(open(R / 'nv8_article_pairs.tsv', newline='', encoding='utf-8'), delimiter='\t'):
        rel = r['note'].split(': ', 1)[0] if r['note'].split(': ', 1)[0] in RELATIONS else ''
        assert rel or 'independent reading' in r['read_by'], ('a pair without a relation', r['page_a'], r['page_b'])       # the readings' own sentences are in their published tables
        prs.append({'page_a': r['page_a'], 'page_b': r['page_b'], 'verdict': r['verdict'], 'relation': rel,
                    'used_for_joining': 'yes' if r['scope'] == 'all' else 'no: superseded by a later line for the same pair' if r['scope'] == 'superseded' else 'no', 'read_by': r['read_by']})
    table(Tg, 'research/nv8_article_pairs.tsv', prs, list(prs[0].keys()), '\t')
    # how the members drawn were chosen: every name searched, its count, and whether it is drawn; then every other word met after a title
    # everyone at three or four articles was read for separate reports on the matter (research/nv8_at_the_line.tsv, Nov 15, 2026)
    line = {r['name']: r for r in csv.DictReader(open(R / 'nv8_at_the_line.tsv', newline=''), delimiter='\t')}
    for s in member_mentions.FIRST:
        assert len(hit[s]) not in (3, 4) or (s in line and line[s]['article_ids'].split() == sorted(hit[s])), ('a member at three or four articles has no reading, or the articles changed since it', s)
    out_ = {s for s in member_mentions.FIRST if line.get(s, {}).get('drawn') == 'no'}
    assert out_ == {a[2].split()[-1] for a in rows_map.ACTORS_ALL if a[0] in rows_map.WITHDRAWN and a[1] in ('senate', 'house')}, ('the readings at the line and the withdrawn members differ', out_)
    sel = [{'name': s, 'first_names_searched': ' / '.join(f), 'articles': len(hit[s]), 'drawn': 'yes' if len(hit[s]) >= 3 and s not in out_ else 'no',
            'why_not': line[s]['reading'] if s in out_ else '' if len(hit[s]) >= 3 else 'named in fewer than three articles'}
           for s, f in member_mentions.FIRST.items()]
    sel += [{'name': s, 'first_names_searched': ' / '.join(v[0]), 'articles': nd_n[s], 'drawn': 'no', 'why_not': 'a current member the articles name for other things: ' + v[2]} for s, v in member_mentions.NOT_DRAWN.items()]
    print('members named for other things, articles:', {r['name']: r['articles'] for r in sel if r['why_not'].startswith('a current member')})
    assert all(r['articles'] >= 3 for r in sel if r['why_not'].startswith('a current member'))
    known = set(member_mentions.FIRST) | {f for v in member_mentions.FIRST.values() for f in v} | set(member_mentions.NOT_DRAWN) | {f for v in member_mentions.NOT_DRAWN.values() for f in v[0]}
    for w_, ids_ in sorted(member_mentions.count()[2].items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(ids_) >= 3:
            assert w_ in known or w_ in member_mentions.NOT_A_MEMBER, ('a word after a congressional title in three or more articles is not classified', w_)
            sel.append({'name': w_, 'first_names_searched': '', 'articles': len(ids_), 'drawn': 'not a name searched',
                        'why_not': 'a word found after a congressional title: ' + ('part of a name searched above' + ('; in other articles ' + member_mentions.NOT_A_MEMBER[w_] if w_ in member_mentions.NOT_A_MEMBER else '')
                                                                                  if w_ in known else 'not a current member: ' + member_mentions.NOT_A_MEMBER[w_])})
        elif len(ids_) == 2:                 # under the line: listed with its count so the line itself can be checked (second audit, Nov 15, 2026)
            sel.append({'name': w_, 'first_names_searched': '', 'articles': 2, 'drawn': 'not a name searched',
                        'why_not': 'a word found after a congressional title in two articles, under the three-article line' + ('' if w_ not in known else ': part of a name searched above')})
    table(Tg, 'research/member_selection.tsv', sel, list(sel[0].keys()), '\t')
    # every harvested link with the class the word rule gives it: the figure counts and draws only 'story'
    import story_scope
    sc = [{'url': r['url'], 'domain': r['domain'], 'headline_as_listed': r['anchor_text'], 'class': story_scope.scope(r['url'], r['anchor_text']) or 'other', 'first_listed': r['first_listed']}
          for r in csv.DictReader(open(R / 'harvest.tsv', newline=''), delimiter='\t')]
    table(Tg, 'research/coverage_scope.tsv', sc, list(sc[0].keys()), '\t')
    # ---------------------------------------------------------------- sources that can be copied: official records and the builder's own captures
    cited = {s for r in rows for s in r['src'] if not s.startswith(('pack:', 'table:'))}
    copies = {pid: rel for pid, rel in R13.COPIES.items() if pid in cited}
    for pid, rel in copies.items():
        d = PRIMARY / pid; (Tg / rel).parent.mkdir(parents=True, exist_ok=True)
        if pid.startswith('google-political-ads'):
            shutil.copyfile(d / 'creative-stats.csv', Tg / rel)
        elif pid.startswith('census'):
            ls = (d / 'tab20_cd11920_zcta520_natl.txt').read_text(encoding='utf-8-sig').splitlines()
            z = {l.split('|')[8] for l in ls[1:] if l.split('|')[1] == '1221' and l.split('|')[8]}
            put(Tg, rel, 'SOURCE: U.S. Census Bureau, relationship file of 2020 zip-code tabulation areas by 119th Congress district\n'
                         'URL: https://www2.census.gov/geo/docs/maps-data/data/rel2020/cd-sld/tab20_cd11920_zcta520_natl.txt\n'
                         'ROWS KEPT: every row whose zip-code area has a row in Congressional District 21 of Florida (GEOID 1221)\n\n'
                         + ls[0] + '\n' + '\n'.join(l for l in ls[1:] if l.split('|')[8] in z) + '\n')
        else:
            txt = '\n\n'.join(f.read_text(errors='replace') for f in sorted(d.glob('text*.txt'), key=lambda f: f.name != 'text.reextract.txt'))
            put(Tg, rel, scrub(re.sub(r'ip=[\d.]+', '', txt)))
        if pid.startswith('google-ads-creative'):
            for n_ in ('frames.png', 'page.png'):
                if (d / n_).exists():
                    shutil.copyfile(d / n_, (Tg / rel).with_name(Path(rel).stem + '-' + n_))
    # ---------------------------------------------------------------- evidence: one line per cited source
    ev = N.evidence()
    for e in ev:
        raw = e['source_ref']
        if raw in copies:
            e['copy_in_repo'] = copies[raw]
        elif raw in R13.FEC_REFS:
            e['copy_in_repo'] = 'research/employee_gifts.csv'; e['what'] += ' (the line is in research/employee_gifts.csv by its sub_id, with a link to its FEC page image; the donor is not named)'
        if raw.startswith('evidence-set:congress/hard_money#') and e['kind'] == 'evidence-set row' and e['passage'] == 'BANKS FOR SENATE':
            e['copy_in_repo'] = 'research/employee_gifts.csv'
        if raw.startswith(('techmeme-', 'memeorandum-')):
            e['what'] = 'A saved page of the news aggregator (the piece is listed there under this headline)'
        e['url'] = re.sub(r'([?&])api_key=[^&]+&?', r'\1', e['url'])
        if e['url'].startswith('file:'):   # an evidence-set row whose source is the builder's saved download of a public index
            assert 'openphil-grants-raw' in e['url'], e['row_id']
            e['url'] = 'https://coefficientgiving.org/grants/'; e['what'] += ' (read from a download of the funder\'s public grants index saved on Sep 11, 2026; the link is the index)'
    table(Tg, 'research/evidence.tsv', ev, list(ev[0].keys()), '\t')
    # ---------------------------------------------------------------- the figure
    for e in ('html', 'png', 'jpg'):
        (Tg / 'figures').mkdir(exist_ok=True); shutil.copyfile(ROOT / 'figures' / f'{N.STEM}.{e}', Tg / 'figures' / f'{N.STEM}.{e}')
    # ---------------------------------------------------------------- the audit
    audit_note = 'not finished when this copy was assembled'
    if (LANE / 'done' / 'DONE').exists() and (LANE / 'out' / 'REPORT.md').exists():
        put(Tg, 'audit/BRIEF.md', scrub((LANE / 'PROMPT.md').read_text()).replace('lanes/audit_nv8', 'audit'))
        for name in ('REPORT.md', 'findings.csv', 'figure_findings.csv', 'census.md', 'members.md', 'gaps.csv', 'errata.csv'):
            if (LANE / 'out' / name).exists():
                put(Tg, f'audit/{name}', scrub((LANE / 'out' / name).read_text()).replace('lanes/audit_nv8', 'audit'))
        audit_note = (LANE / 'out' / 'REPORT.md').read_text().strip().splitlines()[-1]
    disp = R / 'audits' / 'DISPOSITIONS-audit_nv8.csv'
    if disp.exists():
        put(Tg, 'audit/DISPOSITIONS.csv', disp.read_text())
    # ---------------------------------------------------------------- the second audit (Nov 15, 2026): three lanes, each read only after its done marker
    A2 = {'a': ('findings.csv', 'figure_findings.csv', 'earlier_dispositions.csv'), 'b': ('money_findings.csv', 'coverage_findings.csv', 'money.md', 'census.md'), 'c': ('selection_findings_final.csv',),
          # the third reading (of the corrections); its two tables that list not-drawn people one by one are held back with the look-up lists
          'd': ('findings.csv', 'figure_findings.csv', 'dispositions_check.csv', 'joint_committees_check.csv', 'money.md', 'remarks_check.csv', 'gaps.csv', 'controls.csv'),
          'e': ('findings.csv', 'figure_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'f': ('findings.csv', 'figure_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'g': ('findings.csv',),
          # the seventh reading (slice S8: the pages saved since the first census, counts on articles); its look-up check, which names people who are not drawn, is held back
          'h': ('findings.csv', 'figure_findings.csv', 'counts_check.csv', 'gaps.csv'),
          # the eighth reading (of the answers to the seventh); its check of three look-up reasons names people who are not drawn and is held back
          'i': ('findings.csv', 'figure_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the ninth reading (of the answers to the eighth and of the 54 pages saved by hand); its look-up check names people who are not drawn and is held back
          'j': ('findings.csv', 'figure_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'k': ('findings.csv', 'figure_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'l': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the twelfth reading (of the answers to the eleventh, and the first of the interactive map); its look-up check, which names people who are not drawn, is held back
          'm': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the thirteenth reading (of the answers to the twelfth); its look-up check is held back
          'n': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the fourteenth reading (of the answers to the thirteenth); its look-up check is held back
          'o': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the fifteenth reading (of the answer to the fourteenth); its look-up check holds a header only and is held back with the others
          'p': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the sixteenth reading (of the answer to the fifteenth); its look-up check holds a header only and is held back with the others
          'q': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the seventeenth reading (of the answer to the sixteenth and of the builder's two rounds after it); its look-up check holds a header only and is held back with the others
          'r': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the eighteenth reading (of the answer to the seventeenth); its look-up check holds a header only and is held back with the others
          's': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the nineteenth reading (of the answer to the eighteenth and to the first three reading lanes); its look-up check holds a header only and is held back with the others
          't': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the twentieth reading (of the six further lanes' rows and of the answer to the nineteenth); its look-up check holds a header only and is held back with the others
          'u': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the twenty-first reading (of the answer to the twentieth, the builder's scan of versions and the answer to the second reading of the set-aside items)
          'v': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the twenty-second reading (of the answer to the twenty-first, the dispositions of the census and the register of earlier acts)
          'w': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          # the twenty-third reading (of the answer to the twenty-second)
          'x': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'y': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'z': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'aa': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'ab': ('findings.csv', 'figure_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),        # the twenty-seventh reading was asked for no map or companion file
          'ac': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'ad': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'ae': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'af': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv'),
          'ag': ('findings.csv', 'findings13.csv', 'figure_findings.csv', 'site_findings.csv', 'counts_check.csv', 'dispositions_check.csv', 'gaps.csv')}
    A2_LANE = {'h': 'audit_nv8_s8a', 'i': 'audit_nv8_s8b', 'j': 'audit_nv8_s8c', 'k': 'audit_nv8_s8d', 'l': 'audit_nv8_s8e', 'm': 'audit_nv8_s8f', 'n': 'audit_nv8_s8g', 'o': 'audit_nv8_s8h', 'p': 'audit_nv8_s8i', 'q': 'audit_nv8_s8j', 'r': 'audit_nv8_s8k', 's': 'audit_nv8_s8l', 't': 'audit_nv8_s8m', 'u': 'audit_nv8_s8n', 'v': 'audit_nv8_s8o', 'w': 'audit_nv8_s8p', 'x': 'audit_nv8_s8q', 'y': 'audit_nv8_s8r', 'z': 'audit_nv8_s8s', 'aa': 'audit_nv8_s8t', 'ab': 'audit_nv8_s8u', 'ac': 'audit_nv8_s8v', 'ad': 'audit_nv8_s8w', 'ae': 'audit_nv8_s8x', 'af': 'audit_nv8_s8y', 'ag': 'audit_nv8_s8z'}
    audit2_notes = {}
    for t, names in A2.items():
        L2 = LANE.parent / A2_LANE.get(t, f'audit_nv8_s7{t}')
        if (L2 / 'done' / 'DONE').exists() and (L2 / 'out' / 'REPORT.md').exists():
            fix = lambda x, n_=L2.name: scrub(x).replace(f'lanes/{n_}', 'audit2')
            put(Tg, f'audit2/BRIEF-{t}.md', fix((L2 / ('PROMPT_v2.md' if t == 'aa' else 'PROMPT.v2.md' if t in ('ad', 'ae', 'af', 'ag') else 'PROMPT.md')).read_text()))        # the twenty-sixth reading ran from its second brief: the first gave a wrong count; the twenty-ninth and thirtieth too: their first briefs carried the report instructions of the reading before
            put(Tg, f'audit2/REPORT-{t}.md', fix((L2 / 'out' / 'REPORT.md').read_text()))
            for name in names:
                if (L2 / 'out' / name).exists():
                    put(Tg, f'audit2/{t}-{name}', fix((L2 / 'out' / name).read_text()))
            audit2_notes[t] = (L2 / 'out' / 'REPORT.md').read_text().strip().splitlines()[-1]
    disp2 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s7.csv'
    if disp2.exists():
        put(Tg, 'audit2/DISPOSITIONS.csv', disp2.read_text())
    disp3 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s7d.csv'
    if disp3.exists():
        put(Tg, 'audit2/DISPOSITIONS-d.csv', disp3.read_text())
    disp4 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s7e.csv'
    if disp4.exists():
        put(Tg, 'audit2/DISPOSITIONS-e.csv', disp4.read_text())
    disp5 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s7f.csv'
    if disp5.exists():
        put(Tg, 'audit2/DISPOSITIONS-f.csv', disp5.read_text())
    disp6 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s7g.csv'
    if disp6.exists():
        put(Tg, 'audit2/DISPOSITIONS-g.csv', disp6.read_text())
    disp7 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8a.csv'
    if disp7.exists():
        put(Tg, 'audit2/DISPOSITIONS-h.csv', disp7.read_text())
    disp8 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8b.csv'
    if disp8.exists():
        put(Tg, 'audit2/DISPOSITIONS-i.csv', disp8.read_text())
    disp9 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8c.csv'
    if disp9.exists():
        put(Tg, 'audit2/DISPOSITIONS-j.csv', disp9.read_text())
    disp10 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8d.csv'
    if disp10.exists():
        put(Tg, 'audit2/DISPOSITIONS-k.csv', disp10.read_text())
    disp11 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8e.csv'
    if disp11.exists():
        put(Tg, 'audit2/DISPOSITIONS-l.csv', disp11.read_text())
    disp12 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8f.csv'
    if disp12.exists():
        put(Tg, 'audit2/DISPOSITIONS-m.csv', disp12.read_text())
    disp13 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8g.csv'
    if disp13.exists():
        put(Tg, 'audit2/DISPOSITIONS-n.csv', disp13.read_text())
    disp14 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8h.csv'
    if disp14.exists():
        put(Tg, 'audit2/DISPOSITIONS-o.csv', disp14.read_text())
    disp15 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8i.csv'
    if disp15.exists():
        put(Tg, 'audit2/DISPOSITIONS-p.csv', disp15.read_text())
    disp16 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8j.csv'
    if disp16.exists():
        put(Tg, 'audit2/DISPOSITIONS-q.csv', disp16.read_text())
    disp17 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8k.csv'
    if disp17.exists():
        put(Tg, 'audit2/DISPOSITIONS-r.csv', disp17.read_text())
    disp18 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8l.csv'
    if disp18.exists():
        put(Tg, 'audit2/DISPOSITIONS-s.csv', disp18.read_text())
    disp19 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8m.csv'
    if disp19.exists():
        put(Tg, 'audit2/DISPOSITIONS-t.csv', disp19.read_text())
    disp20 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8n.csv'
    if disp20.exists():
        put(Tg, 'audit2/DISPOSITIONS-u.csv', disp20.read_text())
    disp21 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8o.csv'
    if disp21.exists():
        put(Tg, 'audit2/DISPOSITIONS-v.csv', disp21.read_text())
    disp22 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8p.csv'
    if disp22.exists():
        put(Tg, 'audit2/DISPOSITIONS-w.csv', disp22.read_text())
    disp23 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8q.csv'
    if disp23.exists():
        put(Tg, 'audit2/DISPOSITIONS-x.csv', disp23.read_text())
    disp24 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8r.csv'
    if disp24.exists():
        put(Tg, 'audit2/DISPOSITIONS-y.csv', disp24.read_text())
    disp25 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8s.csv'
    if disp25.exists():
        put(Tg, 'audit2/DISPOSITIONS-z.csv', disp25.read_text())
    disp26 = R / 'audits' / 'DISPOSITIONS-audit_nv8_s8t.csv'
    if disp26.exists():
        put(Tg, 'audit2/DISPOSITIONS-aa.csv', disp26.read_text())
    for key_, lane_ in (('ab', 'audit_nv8_s8u'), ('ac', 'audit_nv8_s8v'), ('ad', 'audit_nv8_s8w'), ('ae', 'audit_nv8_s8x'), ('af', 'audit_nv8_s8y'), ('ag', 'audit_nv8_s8z')):
        dispn = R / 'audits' / f'DISPOSITIONS-{lane_}.csv'
        if dispn.exists():
            put(Tg, f'audit2/DISPOSITIONS-{key_}.csv', dispn.read_text())
    if (R / 'lpac_keyed_check.csv').exists() and (LANE.parent / 'fec_lpac_keyed' / 'DONE').exists():      # published once the pull has ended
        put(Tg, 'research/lpac_keyed_check.csv', (R / 'lpac_keyed_check.csv').read_text())
    put(Tg, '.gitignore', '__pycache__/\n*.pyc\n')
    put(Tg, 'LICENSE.md', P.LICENSE_MD)
    import nv8_readme
    put(Tg, 'README.md', nv8_readme.readme(Tg, rows, ev, audit_note))
    # a person no longer drawn who holds no public office is described by role in everything published as the current state: the row files,
    # the tables and this README. The files of earlier readings (audit/, audit2/) are records of what was written then and are left as they are.
    for f in sorted(Tg.rglob('*')):
        if f.is_file() and '.git' not in f.parts and not {'audit', 'audit2', '__pycache__'} & set(f.relative_to(Tg).parts) and f.suffix in ('.py', '.tsv', '.csv', '.md', '.html'):
            t0 = f.read_text(encoding='utf-8', errors='replace'); t1 = t0
            for _, (role_, rep_) in rows_map.WITHDRAWN_PUBLIC.items():
                for k_, v_ in rep_.items():
                    t1 = t1.replace(k_, v_)
            if t1 != t0:
                assert f.name != 'nv8-fifteen-days-mapped.html', 'the figure itself names a person no longer drawn'
                f.write_text(t1, encoding='utf-8')
            assert not any(k_ in t1 for _, (_, rep_) in rows_map.WITHDRAWN_PUBLIC.items() for k_ in rep_), f
    # ---------------------------------------------------------------- checks on the copy
    bad = []
    for f in sorted(Tg.rglob('*')):
        if f.is_file() and '.git' not in f.parts and '__pycache__' not in f.parts and f.suffix not in ('.png', '.jpg'):
            m = PRIVATE.search(f.read_text(encoding='utf-8', errors='replace'))
            if m:
                bad.append((str(f.relative_to(Tg)), m.group(0)))
    assert not bad, ('local paths, ids or addresses in the copy', bad[:8])
    pairs, n_head = name_scan(Tg, rows)
    env = {**__import__('os').environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    same = 'NOT REBUILT (trial run without the render; not a release)'
    if not env.get('NV8_TRIAL_NO_REBUILD'):
        r = subprocess.run([sys.executable, str(Tg / 'scripts' / 'build_nv8.py')], capture_output=True, text=True, env=env); assert r.returncode == 0, r.stderr[-1200:]
        same = (Tg / 'figures' / f'{N.STEM}.html').read_bytes() == (ROOT / 'figures' / f'{N.STEM}.html').read_bytes()
        assert same, 'the figure rebuilt inside the copy differs from the project\'s'
    v = subprocess.run(['python3', '-I', '-B', str(Tg / 'scripts' / 'verify_nv8.py')], capture_output=True, text=True)
    print(v.stdout[-2500:]); assert v.returncode == 0, 'the copy\'s own verifier fails'
    files = sorted(str(f.relative_to(Tg)) for f in Tg.rglob('*') if f.is_file() and '.git' not in f.parts and '__pycache__' not in f.parts)
    assert not list(Tg.rglob('__pycache__')), 'bytecode folders in the copy'
    print(f'wrote {len(files)} files to {Tg}; names scanned for: {len(pairs):,}; hits 0 ({n_head} of them are named by listed headlines in a public role, and appear nowhere else); figure rebuilt in the copy equals the project\'s: {same}; audit: {audit_note}')


def private_names(rows):
    """Donors' and lobbyists' names, as (SURNAME, FIRST) pairs, less the people this figure names on purpose: every member of
    Congress, reporter, analyst, official and executive who is an actor or a node in it (scripts/rows_map.py, rows_people.py,
    rows_context.py), or whom its dated events name in a public role (rows_events.py)."""
    pairs = R13.private_names()
    named = set()
    words = ' '.join(r['drawn_text'] for r in rows if r['table'] != 'piece listed by an aggregator') + ' ' + ' '.join(str(v) for r in rows for k, v in r.items() if k in ('a', 'b', 'actor'))
    for n_ in ('rows_map.py', 'rows_people.py', 'rows_context.py', 'rows_events.py'):
        words += ' ' + (ROOT / 'scripts' / n_).read_text()
    up = words.upper()
    for last, first in pairs:
        if re.search(rf"\b{re.escape(first)}\b[\s.A-Z]{{0,12}}\b{re.escape(last)}\b", up):
            named.add((last, first))
    private_names.named = sorted(named)
    return pairs - named


def _found(text, by_last):
    """The (SURNAME, FIRST) pairs of `by_last` that `text` holds as a name: first name then surname within a few words, or surname, first."""
    t = text.upper(); words = set(re.findall(r"[A-Z'-]{2,}", t)); out = set()
    for last in words & set(by_last):
        for first in by_last[last] & words:
            if re.search(rf"\b{re.escape(first)}\b[\s.A-Z]{{0,12}}\b{re.escape(last)}\b|\b{re.escape(last)}\b,?\s+{re.escape(first)}\b", t):
                out.add((last, first))
    return out


def _hits(text, by_last):
    return [f'{first[0]}. {last[0]}.' for last, first in sorted(_found(text, by_last))]


def _index(pairs):
    by_last = {}
    for last, first in pairs:
        by_last.setdefault(last, set()).add(first)
    return by_last


# People the second audit's files name in a public role and the figure does not draw, whose names are also in the lists the scan reads
# (those lists hold everyone in two tables of the evidence sets, not donors and lobbyists only). Each was checked on Nov 15, 2026:
PUBLIC_IN_AUDIT2 = {('MILLER', 'CHRIS'),      # a historian of the chip industry quoted on the saved pages; the audit says the tables hold his name only as a cited author
                    ('BAIR', 'SHEILA'),       # a former chair of the FDIC quoted on the saved pages; the audit states her past trusteeship of RAND
                    ('DELANGUE', 'CLMENT'),   # the reading's spelling of Clément Delangue, who is drawn
                    ('LIU', 'CHANG')}         # the audit names the Chinese embassy's spokesperson, whose surname and given name are this pair's two words the other way round; the lists hold someone else


def name_scan(Tg, rows):
    """Three scans, each of which must find nothing.
    1. The tables of gifts, PACs, lobbying and committees, and the copied sources: no name from the donors' and lobbyists'
       lists at all (sitting members and the few public figures the three-chairmen figure names are not in those lists).
    2. Every file, with the listed headlines taken out (the headline columns of the coverage tables, the rows and evidence
       lines of listed pieces, the dots' captions in the figure): no such name except the people the figure names on purpose.
    3. Every file as it stands: no such name except those and the people a listed headline names. A headline is quoted as the
       aggregator listed it; the people it names (Nvidia's executives and directors, in those roles) are named nowhere else,
       and nothing here says who gave what."""
    every = R13.private_names(); pairs = private_names(rows)
    # A political committee's name that the lists hold as if it were a person's, because lobbyists' reports give it in the field for the
    # contributor: "Road to Freedom PAC". The gifts table names committees in its contributor column since Nov 16, 2026 (never a person).
    committees = {('FREEDOM', 'ROAD')}
    assert any(r['contributor'] == 'ROAD TO FREEDOM PAC' for r in csv.DictReader(open(R / 'lobbyist_gifts_map.csv', newline=''))), 'the committee this exception is for is no longer in the table'
    every = every - committees; pairs = pairs - committees
    files = [f for f in sorted(Tg.rglob('*')) if f.is_file() and '.git' not in f.parts and '__pycache__' not in f.parts and f.suffix not in ('.png', '.jpg')]
    rel = lambda f: str(f.relative_to(Tg))
    HEADLINE_FILES = ('research/coverage_rows.tsv', 'research/harvest.tsv', 'research/coverage_scope.tsv', 'research/nv8_rows.tsv', 'research/evidence.tsv', f'figures/{N.STEM}.html')
    # the items table names the actors drawn, as the figure does; checks 2 and 3 still read it
    # the table of the second reading of the set-aside items quotes first words too (added Nov 16)
    # the two tables of the reading lanes quote the first words of remarks and the readers' descriptions, which name drawn actors (the board's chairman among them); checks 2 and 3 still read them
    NAMING = HEADLINE_FILES + ('research/member_ties.csv', 'research/member_selection.tsv', 'research/nv8_s6_items.tsv', 'research/nv8_single_article_remarks.tsv', 'research/nv8_paraphrased_acts.tsv', 'research/nv8_earlier_acts.tsv', 'research/nv8_recall_groups.tsv', 'research/nv8_added_pages_acts.tsv', 'research/nv8_population_chips_stage1.tsv', 'research/nv8_population_chips_stage2.tsv', 'README.md') + tuple(rel(f) for f in files if rel(f).startswith(('scripts/', 'audit/', 'audit2/')))
    assert PUBLIC_IN_AUDIT2 <= every, 'a name excused for the second audit\'s files is no longer in the lists: take it off PUBLIC_IN_AUDIT2'
    # 1
    ix = _index(every); bad = [(rel(f), h) for f in files if rel(f) not in NAMING for h in _hits(f.read_text(encoding='utf-8', errors='replace'), ix)]
    assert not bad, ('a name from the donors\' and lobbyists\' lists is in a table of gifts or a copied source (file, initials)', Counter(bad).most_common(12))
    # 2
    def without_headlines(f):
        r = rel(f); t = f.read_text(encoding='utf-8', errors='replace')
        if r in ('research/coverage_rows.tsv', 'research/harvest.tsv', 'research/coverage_scope.tsv'):
            rd = list(csv.DictReader(t.splitlines(), delimiter='\t')); drop = {'headline', 'passage', 'anchor_text', 'text', 'headline_as_listed'} & set(rd[0]); assert drop, r
            return '\n'.join('\t'.join(v for k, v in x.items() if k not in drop) for x in rd)
        if r in ('research/nv8_rows.tsv', 'research/evidence.tsv'):
            ls = t.splitlines(); return '\n'.join(l for l in ls if not l.startswith('CV'))
        if r == f'figures/{N.STEM}.html':
            return re.sub(r'<title>.*?</title>', ' ', t, flags=re.S)
        return t
    ix = _index(pairs); ix2 = _index(pairs - PUBLIC_IN_AUDIT2)
    bad = [(rel(f), h) for f in files for h in _hits(without_headlines(f), ix2 if rel(f).startswith('audit2/') else ix)]
    assert not bad, ('a donor\'s or lobbyist\'s name is in the copy outside a listed headline (file, initials)', Counter(bad).most_common(12))
    # 3
    heads = ' '.join((r.get('headline') or '') + ' ' + (r.get('passage') or '') for r in csv.DictReader(open(Tg / 'research' / 'coverage_rows.tsv', newline=''), delimiter='\t'))
    heads += ' ' + ' '.join(' '.join(v or '' for v in r.values()) for r in csv.DictReader(open(Tg / 'research' / 'harvest.tsv', newline=''), delimiter='\t'))
    in_head = _found(heads, _index(pairs))
    ix = _index(pairs - in_head); ix2 = _index(pairs - in_head - PUBLIC_IN_AUDIT2)
    bad = [(rel(f), h) for f in files for h in _hits(f.read_text(encoding='utf-8', errors='replace'), ix2 if rel(f).startswith('audit2/') else ix)]
    assert not bad, ('a donor\'s or lobbyist\'s name is in the copy (file, initials)', Counter(bad).most_common(12))
    name_scan.in_headlines = len(in_head)
    return pairs, len(in_head)


if __name__ == '__main__':
    main(sys.argv[1])
