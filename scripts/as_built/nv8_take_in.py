"""Run: python3 -I scripts/nv8_take_in.py      (written Nov 17, 2026)
The table behind the second iteration of taking in the pages another session of this project saved: one line for every group of passages, placed in the fifteen
days, that a grouping reader called new, a part of a chip, or unclear (193 groups of five lanes), four more groups on Anthropic and OpenAI read with them, and
the 32 records of a second-round reader of three articles saved later, each with what the builder did with it after reading it on its page.
Who read: ten grouping readers of another company's model sorted the first readers' passages into groups and judged each against the chips; the builder then
read each group on its saved page, in six parallel sessions of its own (one per lane), and wrote the disposition; it read every row written from them once more
against its passages before writing it. No independent reader has read these dispositions.
The dispositions: new act (drawn; the act column gives the chip) | part of a chip (the chip named was amended) | row error in a chip (amended) |
refusal: new act | refusal: added to a chip | carried (a chip already words it) | relay of a response already drawn | same act as another group |
no reply: not drawn (an unanswered request is not a refusal) | earlier act: to the register (before Oct 29; not drawn) | not an act | not the actor's |
cannot be settled from the saved pages | not on the matter: not drawn (the builder's decision at assembly).
Inputs (unpublished: they quote passages and name people who are not drawn): research/reading_lanes/dgroup_fork_<lane>.disp.tsv and the batch's spec file,
research/scratch_archive_s9a/specs_s9o.py, which also lists each decision the builder took when it assembled the rows.
Writes research/nv8_take_in_groups.tsv. Limits: the classes are the builder's reading; a group is the grouping reader's unit, so one act told by two lanes stands
twice (marked 'same act as another group'); the passages themselves are not published."""
import csv, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; RL = R / 'reading_lanes'
LANES = (('c', 'the administration'), ('a', 'Nvidia, Huang and the lawsuits'), ('d', 'members of Congress and others'), ('b', 'Megaspeed and actors abroad'), ('e', 'the residue'), ('j', 'second round: three articles saved later'))
CLASSES = ('new act', 'part of a chip', 'row error in a chip', 'refusal: new act', 'refusal: added to a chip', 'carried', 'relay of a response already drawn', 'same act as another group', 'no reply: not drawn',
           'earlier act: to the register', 'not an act', "not the actor's", 'cannot be settled from the saved pages', 'not on the matter: not drawn')
FIRST_NEW = 379
PLAIN = {'spec dropped': 'no row written', 'specs merged': 'two of the six sessions amended one chip, and the builder wrote one text', 'spec changed': 'the row was changed'}


def main():
    ns = {}; exec((R / 'scratch_archive_s9a' / 'specs_s9o.py').read_text(), ns)
    new = [s for s in ns['SPECS'] if s['do'] == 'new']; chip = {}
    for n, s in enumerate(new, FIRST_NEW):
        for g in s['group'].split(): chip[g] = f'MA{n}'
    amended = {}
    for s in ns['SPECS']:
        if s['do'] == 'amend':
            for g in s['group'].split(): amended.setdefault(g, []).append(f"MA{s['id']:02d}")
    dec = {}
    for what, lane, groups, why in ns['DECISIONS']:
        for g in groups.split(): dec.setdefault(g, []).append(f'{PLAIN[what]}: {why}')
    rows = []; seen = set()
    for k, name in LANES:
        for r in csv.DictReader(open(RL / f'dgroup_fork_{k}.disp.tsv', newline=''), delimiter='\t'):
            r = {a.strip(): (b or '').strip() for a, b in r.items() if a}; g = f"{k}.{r['group']}"; assert g not in seen, g; seen.add(g)
            d = r['disposition']; act = r['target']; day = r['day']
            if g in chip and d in ('new act', 'refusal: new act'): act = chip[g]
            elif d in ('new act', 'refusal: new act'):
                assert any(x.startswith('no row written') for x in dec.get(g, [])), ('a new act with no row', g); d = 'not on the matter: not drawn'; act = ''; day = ''
            if g == 'b.D048': day = '2026-11-12'        # the chip was not moved (the builder's decision; the column on the right says why)
            assert d in CLASSES, (g, d)
            rows.append([name, g, r['actor'], r['reader_verdict'], d, act, day, r['own_or_report'] if d != 'not on the matter: not drawn' else '', r['cuts'], ' | '.join(dec.get(g, []))])
    assert all(g in seen for g in chip if not g.endswith('.none') and not g.startswith('x.')), [g for g in chip if g not in seen]
    with open(R / 'nv8_take_in_groups.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['reading', 'group', 'actor', 'the_grouping_reader_s_verdict', 'the_builder_s_disposition', 'chip_or_other_target', 'day', 'its_own_day_or_its_report_s', 'which_way_the_builder_reads_it', 'what_the_builder_changed_at_assembly']); w.writerows(rows)
    c = Counter(r[4] for r in rows); extra = [g for g in chip if g.endswith('.none') or g.startswith('x.')]
    print('groups and records', len(rows), '| by lane', dict(Counter(r[0] for r in rows)), '| by disposition', {k: c[k] for k in CLASSES if c[k]}, '| chips amended', len({x for v in amended.values() for x in v}), '| new acts', len(new),
          '| new acts from no group (found on a page by the builder)', len(extra), '| decisions at assembly', len(ns['DECISIONS']))


if __name__ == '__main__':
    main()
