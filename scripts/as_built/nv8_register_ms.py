"""The earlier passages on the pages another session saved, prepared for the register of earlier acts.

Run alone (python3 -I scripts/nv8_register_ms.py) it prints what it adds and writes nothing. scripts/nv8_reading_lanes.py calls load() and
adds the groups and lines to the register and the census table (since Nov 17, 2026).

What it reads (research/reading_lanes/, unpublished because the files hold words of pages):
  egroup_nv8_a to _e   five grouping readers (another company's model) who sorted the 671 passages that the first readers of the other session's pages
                       had placed before Oct 29: each line goes to an act the register already holds (its id) or to a new group N001...;
  ms_group.lines_map.tsv, ms_group_i.lines_map.tsv   each line's page, actor and first-reader record (row_in_the_source is a 0-based row of the pool);
                       twenty of the 671 lines are census lines planted as controls and are not added again;
  ms_acts.pool.tsv, ms_acts_i.pool.tsv   the first readers' records (verdict, chip named, row proposed, direction).
Rules:
  - a line counts if its page's own day, read by scripts/nv8_page_dates.py as a U.S. Eastern day, is in the fifteen days (the register holds acts that pages of
    those days recall), or if the page carries no day of its own: such a page is kept, as the count of articles keeps undated pages, and its lines say so in their first column
    (a reader sorted it as coverage of the affair; that it appeared by Nov 12 is not shown). A page dated outside the fifteen days gives a line that is listed and not registered;
  - a new group whose reader set it aside (no occasion named, not the actor's, not on the matter) is listed and not registered;
  - a new group that is the same passage on the same page as an act the builder registered after the twenty-sixth reading (B.10 to B.18) joins that act (SAME, read by the builder);
  - a new group whose reader named a chip, tie line or member's line that exists is carried by it; three groups about Anthropic and OpenAI are carried by rows the builder checked (BUILDER_CARRIED);
  - every other new group is an open act, id E<lane letter>.<its reader's number>, worded by its reader;
  - thirty of the lines stand on eight pages that ARE in the table of counted pages: pages a chip cites, given to the first readers as tests with that chip held out. The census reader of each
    such page had read it already. Where the census holds the same passage on that page (the words of one contain the words of the other; each of the twenty pairs read by the builder on Nov 17,
    list ON_COUNTED_SAME) the line is not added again: the census line stands for it, in the group and with the verdict it has there (seventeen of the twenty went to the same act in both sortings;
    two went to another act and one stands as carried in the census). The other ten are passages the census reader had not listed: they are added, and their first column says the page is counted.
Amendment of Nov 17, 2026, after the twenty-ninth reading (its point P05). The grouping readers did not draw the line of 'no occasion named' alike: three of them set such summaries aside, two kept comparable ones as
unresolved acts (the reading names Ea.N004 against Eb.N019 and Ee.N035; by their own wording about a third of the kept groups are undated or unidentified too). One rule holds now for every actor: a group whose
reader found no identifiable occasion in it is REGISTERED as an open, unresolved record and marked so (KEPT_UNRESOLVED). Only the groups a reader found not to be the actor's, or not on the matter, stay set aside.
Nothing here draws anything."""
import csv, re, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; RL = R / 'reading_lanes'; sys.path.insert(0, str(ROOT / 'scripts'))
csv.field_size_limit(10**9)
# the same passage on the same page as an act the builder registered from that page after the twenty-sixth reading (each pair read by the builder on Nov 17)
SAME = {('b', 'N022'): 'B.10', ('b', 'N008'): 'B.11', ('d', 'N025'): 'B.13', ('b', 'N011'): 'B.14', ('a', 'N013'): 'B.16', ('d', 'N035'): 'B.18'}
# groups about Anthropic and OpenAI that a row carries although their reader named none (the builder's check of every group that names either company)
BUILDER_CARRIED = {('c', 'N042'): ('MT20', "a live page's sentence that he used the company's cash to back dozens of AI companies, 'including OpenAI and Anthropic'; the tie lines between Nvidia and each of the two give its investments in them, and the sentence adds no particular of either"),
                   ('d', 'N019'): ('MA69', "OpenAI's chip of Nov 4 gives the report itself, from the first saved relay of it"), ('d', 'N027'): ('MT66', "the line on Anthropic's row gives the senators' citation of the report")}
KEPT_UNRESOLVED = 'no occasion'        # since the twenty-ninth reading: registered as unresolved, for every actor (the docstring's amendment)
# the thirty-first reading (B-ASIDE-1): one summary its reader set aside as not the actor's rests on acts of the actor named. The page's sentence is "It's possible that smuggling has fallen since mid-2025 because of crackdowns in Malaysia and Taiwan":
# the fall is the author's guess, the crackdowns are those governments' acts, and none is identified. It is registered as an unresolved record like the other summaries with no identifiable occasion (its reader's note says no crackdown can be identified).
REREAD_UNRESOLVED = {('b', 'N021')}
ASIDE = {'no occasion': 'its grouping reader found no identifiable occasion in it', "not the actor's": 'its grouping reader found it is not an act of the actor named', 'not on the matter': 'its grouping reader found it is not on the matter'}
LABEL = 'egroup_nv8_{k} (a grouping reader of the earlier passages on pages another session saved, outside the table of counted pages)'
LABEL_COUNTED = 'egroup_nv8_{k} (a grouping reader of earlier passages; this page is a counted page that a first reader was given as a test, and its census reader had not listed the passage)'
# lines on counted pages whose passage the census reader of that page had listed (lane letter, line): each pair of passages read by the builder on Nov 17, 2026; load() checks the words of each
ON_COUNTED_SAME = {('a', 'L043'), ('a', 'L145'), ('b', 'L024'), ('b', 'L057'), ('b', 'L146'), ('c', 'L032'), ('c', 'L033'), ('c', 'L034'), ('c', 'L035'), ('c', 'L060'), ('c', 'L087'), ('c', 'L088'), ('c', 'L126'),
                   ('d', 'L017'), ('d', 'L018'), ('d', 'L070'), ('e', 'L004'), ('e', 'L005'), ('e', 'L007'), ('e', 'L008')}
_norm = lambda t: ' '.join(re.findall(r'[a-z0-9]+', t.lower().replace('\u2019', '').replace("'", '')))
UNDATED = '; the page carries no day of its own'


def load(reg_ids, all_ids):
    """reg_ids: the ids the register holds already; all_ids: every row id a disposition may name. Returns (groups, lines, stats)."""
    import nv8_page_dates as D
    pools = {f: list(csv.DictReader(open(RL / f, newline='', encoding='utf-8'), delimiter='\t')) for f in ('ms_acts.pool.tsv', 'ms_acts_i.pool.tsv')}
    maps = [r for f in ('ms_group.lines_map.tsv', 'ms_group_i.lines_map.tsv') for r in csv.DictReader(open(RL / f, newline=''), delimiter='\t') if r['lane'].startswith('egroup_nv8_')]
    counted = {r['page_id'] for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')}        # the table of counted pages
    census = defaultdict(list)        # the census readers' passages, by page
    for r in csv.DictReader(open(RL / 'recall_nv8.pool.tsv', newline='', encoding='utf-8'), delimiter='\t'): census[r['page_id']].append(_norm(r['exact_words']))
    same_seen = set()
    day_of = {}
    def day(pid):
        if pid not in day_of: day_of[pid] = D.day_of(pid, *D.meta(pid))[0] or ''
        return day_of[pid]
    groups = {}; lines = []; st = Counter(); used = defaultdict(int)
    for k in 'abcde':
        lane = f'egroup_nv8_{k}'
        G = {r['group']: r for r in csv.DictReader(open(RL / f'{lane}.groups.csv', newline='', encoding='utf-8'))}
        LG = {r['line']: r['group'] for r in csv.DictReader(open(RL / f'{lane}.lines.csv', newline='', encoding='utf-8'))}
        mine = [m for m in maps if m['lane'] == lane]; assert sorted(m['line'] for m in mine) == sorted(LG), ('a line with no group or no map', lane)
        for m in mine:
            if m['control']: st['planted controls (census lines, not added again)'] += 1; continue
            p = pools[m['source']][int(m['row_in_the_source'])]; assert p['page_id'] == m['page_id'] and p['actor'] == m['actor'], (lane, m['line'])
            on_counted = m['page_id'] in counted
            if on_counted:
                assert p['planted_page'].strip() == 'yes', (lane, m['line']); w = _norm(p['exact_words']); held = len(w) >= 20 and any(len(c) >= 20 and (w in c or c in w) for c in census[m['page_id']])
                assert held == ((k, m['line']) in ON_COUNTED_SAME), ('the words do not agree with the pairs the builder read', lane, m['line'])
                if held: same_seen.add((k, m['line'])); st['lines on a counted page whose census reader had listed the same passage (not added again)'] += 1; continue
                st['lines on a counted page whose census reader had not listed the passage (added, and marked)'] += 1
            gid = LG[m['line']]; d = day(m['page_id']); in_days = (not d) or '2026-10-29' <= d <= '2026-11-12'; st['lines on a page with no day of its own (kept, and marked)'] += not d
            base = {'lane': (LABEL_COUNTED if on_counted else LABEL).format(k=k) + ('' if d else UNDATED), 'page': m['page_id'], 'day': d, 'actor': m['actor'], 'verdict': p['verdict'].strip(), 'chip': ' '.join(re.findall(r'M[AT]\d+', p['chip_or_tie'])),
                    'row': p['row_it_belongs_on'].strip(), 'direction': p['direction'].strip(), 'target': '', 'disp': ''}
            assert base['verdict'] in ('CANDIDATE occasion', 'CANDIDATE part'), (lane, m['line'], base['verdict'])
            if not in_days and (k, gid) in BUILDER_CARRIED:        # a record about Anthropic or OpenAI is never left without its row, whatever the page's day
                row, why = BUILDER_CARRIED[(k, gid)]; base['disp'] = f'carried: {row} ({why}); the page is of {d}, outside the fifteen days, so the line is not added to the register'; st['lines about Anthropic or OpenAI on a page outside the days, carried by a row'] += 1
            elif not in_days:
                base['disp'] = f'not registered: the page is of {d}, outside the fifteen days; the register holds acts that pages of the fifteen days recall'
                st['lines on a page dated outside the fifteen days'] += 1
            elif gid in reg_ids:
                base['target'] = gid; st['lines to an act the register holds'] += 1
            else:
                g = G[gid]; aside = g['set_aside'].strip()
                if (k, gid) in REREAD_UNRESOLVED: assert aside == "not the actor's", (k, gid, aside); aside = KEPT_UNRESOLVED
                if (k, gid) in SAME: base['target'] = SAME[(k, gid)]; st['lines to an act the builder registered after the twenty-sixth reading'] += 1
                elif aside and aside != KEPT_UNRESOLVED and (k, gid) not in BUILDER_CARRIED:        # a group about Anthropic or OpenAI that a row carries is marked carried even where its reader found no occasion in it
                    assert aside in ASIDE, (lane, gid, aside); base['disp'] = 'not registered: ' + ASIDE[aside]; st['lines of a group its reader set aside'] += 1
                else:
                    nid = f'E{k}.{gid}'; base['target'] = nid; st['lines to a new act'] += 1
                    if aside == KEPT_UNRESOLVED and (k, gid) not in BUILDER_CARRIED: st['of them, lines of a summary in which its reader found no identifiable occasion (registered as unresolved since the twenty-ninth reading)'] += 1
                    if nid not in groups:
                        named = [x for x in re.findall(r'M[AT]\d+|TY\d+', g['carried_by']) if x in all_ids]
                        assert bool(named) == bool(g['carried_by'].strip()), ('a reader names a row that is not there', lane, gid, g['carried_by'])
                        if (k, gid) in BUILDER_CARRIED:
                            row, why = BUILDER_CARRIED[(k, gid)]; assert row in all_ids and not named; disp = f'carried since Nov 17: {row} ({why}; found by the builder, the grouping reader named no row)'
                        elif named: disp = 'carried: ' + ', '.join(named) + ' (the grouping reader\'s verdict)'
                        else: disp = None        # open: the register script words it
                        groups[nid] = {'actor': g['actor'], 'what': g['what'], 'when': g['when'], 'kind': g['kind'], 'first_reported': g['first_reported'], 'row_it_belongs_on': g['row_it_belongs_on'], 'direction': g['direction'], 'disp': disp, 'lane': lane, 'counted_only': True, 'no_occasion': aside == KEPT_UNRESOLVED and (k, gid) not in BUILDER_CARRIED}
                    used[nid] += 1; groups[nid]['counted_only'] &= on_counted
            lines.append(base)
    for (k_, gid_), (row_, _) in BUILDER_CARRIED.items(): assert row_ in all_ids, row_
    assert all(f'E{k_}.{g_}' in groups for k_, g_ in REREAD_UNRESOLVED), 'a reread summary is not registered'
    assert same_seen == ON_COUNTED_SAME, (same_seen ^ ON_COUNTED_SAME); st['new acts recalled only by a counted page'] = sum(1 for g in groups.values() if g['counted_only'])
    st['new acts'] = len(groups); st['of them carried'] = sum(1 for g in groups.values() if g['disp']); st['of them, summaries with no identifiable occasion (unresolved)'] = sum(1 for g in groups.values() if g['no_occasion']); st['pages of the lines'] = len({l['page'] for l in lines}); st['lines'] = len(lines)
    return groups, lines, st


if __name__ == '__main__':
    reg = {r['earlier_act']: r for r in csv.DictReader(open(R / 'nv8_recall_groups.tsv', newline=''), delimiter='\t')}
    import rows_map
    all_ids = {r['row_id'] for r in rows_map.rows()} | {r['row_id'] for r in csv.DictReader(open(R / 'member_ties.csv'))}
    groups, lines, st = load(set(reg), all_ids)
    for k_, v in st.items(): print(f'{v:5d}  {k_}')
    op = [g for g in groups.values() if not g['disp']]
    print('open new acts by actor:', Counter(g['actor'] for g in op).most_common(12))
    print('open new acts by direction:', Counter(g['direction'] for g in op).most_common(), '| by first report:', Counter(g['first_reported'] for g in op).most_common())
    tg = Counter(l['target'] for l in lines if l['target'] in reg); print('register acts that gain lines:', len(tg), '| of them carried now:', sum(1 for t in tg if not reg[t]['builder_disposition'].startswith('open')), '| lines to carried acts:', sum(v for t, v in tg.items() if not reg[t]['builder_disposition'].startswith('open')))
    print('days of the pages outside the fifteen days:', Counter(l['day'] for l in lines if l['disp'].startswith('not registered: the page')).most_common(8), '| pages with no day:', len({l['page'] for l in lines if not l['day']}))
