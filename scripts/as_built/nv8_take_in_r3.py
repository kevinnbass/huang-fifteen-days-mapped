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
subscriber stub, a faulty test) say nothing about what the readers missed elsewhere."""
import csv
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; RL = R / 'reading_lanes'
CLASSES = ('new act', 'refusal: new act', 'part of a chip', 'row error in a chip', 'refusal: added to a chip', 'carried', 'relay of a response already drawn', 'same act as another record', 'no reply: not drawn',
           'earlier act: to the register', 'after the days: not drawn', 'not an act', "not the actor's", 'cannot be settled from the saved pages')
FIRST_NEW = 418


def main():
    ns = {}; exec((R / 'scratch_archive_s9a' / 'specs_s9r.py').read_text(), ns)
    new = [s for s in ns['SPECS'] if s['do'] == 'new']; chip = {}
    for n, s in enumerate(new, FIRST_NEW):
        for g in s['group'].split(): chip[g] = f'MA{n}'
    rows = []; seen = set()
    for k in 'klm':
        for r in csv.DictReader(open(RL / f'r3_fork_{k}.disp.tsv', newline=''), delimiter='\t'):
            r = {a.strip(): (b or '').strip() for a, b in r.items() if a}; g = f"{k}.L{r['line']}"; assert g not in seen, g; seen.add(g)
            d = r['disposition']; assert d in CLASSES, (g, d); act = r['target']
            if d in ('new act', 'refusal: new act'): assert g in chip, ('a new act with no row', g); act = chip[g]
            rows.append(['acts_nv8_added_' + k, r['line'], r['page'], r['actor'], r['reader_verdict'], d, act, r['day'], r['own_or_report'], r['cuts']])
    with open(R / 'nv8_take_in_round3.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['reading_lane', 'record', 'page', 'actor', 'the_first_reader_s_verdict', 'the_builder_s_disposition', 'chip_or_other_target', 'day', 'its_own_day_or_its_report_s', 'which_way_the_builder_reads_it']); w.writerows(rows)
    c = Counter(r[5] for r in rows); from_record = {g for g in chip if g in seen}
    print('records', len(rows), '| by lane', dict(Counter(r[0][-1] for r in rows)), '| by disposition', {k: c[k] for k in CLASSES if c[k]}, '| amended chips in the batch', sum(1 for s in ns['SPECS'] if s['do'] == 'amend'),
          '| new acts', len(new), 'of them from a record', len({chip[g] for g in from_record}), '| which way the undrawn ones cut', dict(Counter(r[9] for r in rows if r[5] in ('no reply: not drawn', 'not an act', "not the actor's", 'cannot be settled from the saved pages'))))


if __name__ == '__main__':
    main()
