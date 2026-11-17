"""Run: python3 -I scripts/nv8_take_in_r3.py      (written Nov 17, 2026)
The table behind the third round of taking in the pages another session of this project saved: 89 pages whose saved HTML holds the piece while the text file
given to the first readers was a stub or a fragment. Three further readers of another company's model read them from the HTML against the table of acts as it
stood before the second iteration of the take-in (375 dated acts; each reader's table held 373, two chips being held out); they returned 601 records, 262 of them candidates.
This table has one line for every candidate that its reader placed in the fifteen days or gave no period (95), with what the builder did with it after reading
it on its saved page, in three parallel sessions of its own (one per lane), each record against the actor's chips as they stand now. The builder read every
row written from them once more against its passages before writing it. No independent reader has read these dispositions.
The candidates the readers placed before Oct 29 (167) are not here: they wait for the register. Of the nine records below with the disposition 'earlier act: to the register', five name one act of the register
and are lines of it (list R_OUTSIDE in scripts/nv8_reading_lanes.py); the other four name no single act and wait with the 167.
The dispositions: new act | refusal: new act (drawn; the target column gives the chip) | part of a chip | row error in a chip (the chip named was amended) |
carried (a chip already words it; for most, a chip that the second iteration of the take-in drew from the same page) | relay of a response already drawn |
same act as another record | no reply: not drawn (an unanswered request is not a refusal) | earlier act: to the register (before Oct 29; not drawn) |
not an act | not the actor's | cannot be settled from the saved pages.
Inputs (unpublished: they quote passages and name people who are not drawn): research/reading_lanes/r3_fork_<lane>.disp.tsv and the batch's spec file,
research/scratch_archive_s9a/specs_s9r.py, whose head lists each decision the builder took when it assembled the rows.
Writes research/nv8_take_in_round3.tsv. Limits: the classes are the builder's reading; a record is the first reader's unit, so one act told on two pages
stands twice; the passages themselves are not published; the controls (five of six held-out chips came back as candidates, the sixth was a byline planted on a
subscriber stub, a faulty test) say nothing about what the readers missed elsewhere.
Amendment of Nov 17, 2026, after the twenty-ninth reading, the first independent reading of these dispositions: the last column (AFTER) says what no longer stands, and the builder's disposition beside it is kept as
history. One of the nine 'earlier act' records (k.118) is carried by a chip, so three records, not four, name no single act and wait with the 167; one of the ten 'no reply' records states no request;
five of the ten 'relay' records summarise a position without naming the occasion; two records' responses moved to the chip of their report's day."""
import csv, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; RL = R / 'reading_lanes'; sys.path.insert(0, str(ROOT / 'scripts'))
CLASSES = ('new act', 'refusal: new act', 'part of a chip', 'row error in a chip', 'refusal: added to a chip', 'carried', 'relay of a response already drawn', 'same act as another record', 'no reply: not drawn',
           'earlier act: to the register', 'after the days: not drawn', 'not an act', "not the actor's", 'cannot be settled from the saved pages')
FIRST_NEW = 418
RELAY = ('the page summarises an undated position or repeated denials and names no occasion: that it relays the particular response on the chips named is not shown, and which occurrence it is stays unresolved. '
         'No new act is drawn from it (the twenty-ninth reading)')
MOVED = ('the responses this record holds stood on the company\'s chip of Nov 6 (MA179); their page gives them no day, so they stand now on its chip of Nov 9 (MA421), the day of the account that reports them (the twenty-ninth reading)')
AFTER = {'k.118': 'now carried: MA207 (the chip gives, from the same account, that the under secretary "had also received repeated warnings about Megaspeed in deputy-level meetings"). "Earlier act: to the register" no longer stands (the twenty-ninth reading)',
         'l.17': 'the page says only that the White House did not comment on the measures: it states no request, so "no reply" says more than the page does. Still not drawn: a refusal is not established either (the twenty-ninth reading)',
         'k.76': RELAY, 'k.194': RELAY, 'm.119': RELAY, 'm.188': RELAY, 'm.189': RELAY, 'l.161': MOVED, 'l.162': MOVED}


def main():
    ns = {}; exec((R / 'scratch_archive_s9a' / 'specs_s9r.py').read_text(), ns)
    new = [s for s in ns['SPECS'] if s['do'] == 'new']; chip = {}
    for n, s in enumerate(new, FIRST_NEW):
        for g in s['group'].split(): chip[g] = f'MA{n}'
    rows = []; seen = set(); used = set()
    for k in 'klm':
        for r in csv.DictReader(open(RL / f'r3_fork_{k}.disp.tsv', newline=''), delimiter='\t'):
            r = {a.strip(): (b or '').strip() for a, b in r.items() if a}; g = f"{k}.L{r['line']}"; assert g not in seen, g; seen.add(g)
            d = r['disposition']; assert d in CLASSES, (g, d); act = r['target']
            if d in ('new act', 'refusal: new act'): assert g in chip, ('a new act with no row', g); act = chip[g]
            rows.append(['acts_nv8_added_' + k, r['line'], r['page'], r['actor'], r['reader_verdict'], d, act, r['day'], r['own_or_report'], r['cuts'], AFTER.get(f"{k}.{r['line']}", '')]); used.add(f"{k}.{r['line']}")
    with open(R / 'nv8_take_in_round3.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['reading_lane', 'record', 'page', 'actor', 'the_first_reader_s_verdict', 'the_builder_s_disposition', 'chip_or_other_target', 'day', 'its_own_day_or_its_report_s', 'which_way_the_builder_reads_it', 'changed_after_an_independent_reading']); w.writerows(rows)
    assert set(AFTER) <= used, set(AFTER) - used
    import rows_map; W = {r['row_id']: r for r in rows_map.rows()}; assert 'had also received repeated warnings about Megaspeed in deputy-level meetings' in W['MA207']['what'] and 'In response to the Financial Times report' in ' '.join(W['MA421']['q']) and 'In response to the Financial Times report' not in ' '.join(W['MA179']['q'])
    c = Counter(r[5] for r in rows); from_record = {g for g in chip if g in seen}
    print('records', len(rows), '| by lane', dict(Counter(r[0][-1] for r in rows)), '| by disposition', {k: c[k] for k in CLASSES if c[k]}, '| amended chips in the batch', sum(1 for s in ns['SPECS'] if s['do'] == 'amend'),
          '| new acts', len(new), 'of them from a record', len({chip[g] for g in from_record}), '| which way the undrawn ones cut', dict(Counter(r[9] for r in rows if r[5] in ('no reply: not drawn', 'not an act', "not the actor's", 'cannot be settled from the saved pages'))), '| changed after an independent reading', sum(1 for r in rows if r[10]))


if __name__ == '__main__':
    main()
