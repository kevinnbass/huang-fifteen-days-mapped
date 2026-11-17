"""Run: python3 -I scripts/nv8_blind_spot_population.py      (written while answering the nineteenth reading, Nov 16, 2026)
The population the paraphrase reading lanes were drawn from, with a list of its lines, so that its numbers can be recounted. The nineteenth
reading could not reproduce two numbers the status gave (4,803 lines, about 2,850 of them of "the other actors"): the count had been made
by a one-off script and no list was kept.

The rule, as the lane builder applied it. A line of the census readings is in the population when
  - its speaker is a drawn actor and its page is a counted page;
  - it is not a direct quotation of seven words or more (those are the business of the third gauge and of the single-article lane);
  - no chip of that actor carries it by its words: it shares no run of five words with the words of any act of the actor or the passages
    that act cites, and fewer than three fifths of its words (words of three letters or more, a line of four or more such words) stand in
    any one act of the actor.
Words are compared as the third gauge compares them (lower case, letters and digits). "By its words" is all the rule sees: a line in the
population may still be carried by a chip in other words, which is what the readers were asked to judge.

The population depends on the chips, so it is counted at three stages:
  stage 1  the acts as they stood before the first three lanes (249 acts that are not withdrawn; frozen in research/nv8_population_chips_stage1.tsv);
  stage 2  the acts after the answer to those lanes and to the eighteenth reading, before lanes c to h (290; ..._stage2.tsv);
  now      the acts as they stand.
A lane's input was the population of its actors at its stage, plus the lines that only an act held out as a control carried.
Lines on pages added to the table after the lanes had run (nine pages, Nov 17, 2026) are counted only in the present column: no paraphrase lane
read them; a later reader read those pages whole against the chips, and the table names that lane for them.

Writes research/nv8_blind_spot_population.tsv: one row for every line that was in the population at any stage or in a lane's input, with
its number in the census readings (the line ids the lanes used), its actor, page and article, the stages at which it was in the population,
and the lane that read it. It holds no words of the line.
Checks: every line of a lane's input is in the population of its stage or is a line only a held-out act carried; every line of the
population at a lane's stage, by an actor of that lane, is in the lane's input. Control: with one act taken away the population grows.
  python3 -I scripts/nv8_blind_spot_population.py --freeze <stage 1 rows file> <stage 2 rows file>
      writes the two frozen tables of acts from earlier copies of scripts/rows_map.py; refuses if they exist. Run once, on Nov 16, 2026."""
import csv, importlib.machinery, importlib.util, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; L = R / 'reading_lanes'; sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_gaps as G, rows_map, nv8_remarks_no_chip as T
STAGE = {'1': R / 'nv8_population_chips_stage1.tsv', '2': R / 'nv8_population_chips_stage2.tsv'}
LANE_STAGE = dict({k: '1' for k in 'ab'}, **{k: '2' for k in 'cdefgh'})
FIRST = ('nvidia', 'board', 'jones', 'kress')          # the actors of lanes a and b: the company, its board, its chairman and its interim chief
SEP = ' || '


def freeze(paths):
    for (k, out), src in zip(STAGE.items(), paths):
        assert not out.exists(), f'{out} exists'
        ld = importlib.machinery.SourceFileLoader('rows_map_stage' + k, src); m = importlib.util.module_from_spec(importlib.util.spec_from_loader(ld.name, ld)); ld.exec_module(m)
        rows = [r for r in m.rows() if r['row_id'].startswith('MA') and not r.get('withdrawn')]
        with open(out, 'w', newline='') as f:
            w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['act', 'actor', 'words_on_the_chip', 'passages_cited'])
            w.writerows([r['row_id'], r['actor'], r['what'], SEP.join(r['q'])] for r in rows)
        print('froze', out.name, len(rows), 'acts')


def census():
    art = G.article_of(); actors = {a[0] for a in rows_map.ACTORS}; out = []
    for n, r in enumerate(G.lane_rows('remarks'), 1):
        if r.get('page_id') not in art: continue
        a = G.actor_of(G.canon(r.get('speaker') or ''), r.get('kind', ''))
        if a not in actors: continue
        w = T.nw(r.get('remark') or '')
        if (r.get('direct_quote') or '').strip().lower() == 'yes' and len(w) >= 7: continue
        out.append({'n': n, 'actor': a, 'page': r['page_id'], 'art': art[r['page_id']], 'sh': T.sh(w), 'w': G.words(r.get('remark') or '')})
    return out


def uncarried(lines, acts):
    """acts: (actor, text of the chip's words and its cited passages)."""
    chip_sh = defaultdict(set); chip_words = defaultdict(list)
    for actor, t in acts:
        chip_sh[actor] |= T.sh(T.nw(t)); chip_words[actor].append(G.words(t))
    return {l['n'] for l in lines if not (l['sh'] & chip_sh[l['actor']]) and not any(len(l['w']) >= 4 and len(l['w'] & cw) / len(l['w']) >= 0.6 for cw in chip_words[l['actor']])}


def main():
    lines = census(); byn = {l['n']: l for l in lines}
    acts = {k: [(r['actor'], r['words_on_the_chip'] + ' ' + ' '.join(r['passages_cited'].split(SEP))) for r in csv.DictReader(open(p, newline=''), delimiter='\t')] for k, p in STAGE.items()}
    now = [r for r in rows_map.rows() if r['row_id'].startswith('MA') and not r.get('withdrawn')]
    acts['now'] = [(r['actor'], r['what'] + ' ' + ' '.join(r['q'])) for r in now]
    pop = {k: uncarried(lines, v) for k, v in acts.items()}
    # Pages added to the table after the paraphrase lanes had run (nine, on Nov 17, 2026): their lines were in no lane's population, so they
    # are counted only in the present column; a reader read those pages whole against the chips (lane acts_nv8_added_a), which the table says.
    late_pages = {r['page_id'] for r in csv.DictReader(open(R / 'nv8_pages_added.tsv', newline=''), delimiter='\t') if 'found outside this table on Nov 17' in r['why_saved']}
    late = {l['n'] for l in lines if l['page'] in late_pages}; assert len(late_pages) == 9 and late and min(late) > max(l['n'] for l in lines if l['n'] not in late), 'the lines of the pages added later must come after every other line'
    pop['1'] -= late; pop['2'] -= late
    lane_of = {}; held = set(); lane_actors = defaultdict(set)
    for k in LANE_STAGE:
        ctl = {int(r['line_id'][1:]) for r in csv.DictReader(open(L / f'para_nv8_{k}.controls.tsv'), delimiter='\t') if r['only_a_held_out_act_carried_it'] == 'yes'}
        for r in csv.DictReader(open(L / f'para_nv8_{k}.lines_in.tsv'), delimiter='\t'):
            n = int(r['line_id'][1:]); assert n in byn and n not in lane_of, ('a lane line that is not a census line of the rule, or is in two lanes', k, n)
            lane_of[n] = k; lane_actors[k].add(byn[n]['actor'])
            assert (n in pop[LANE_STAGE[k]]) != (n in ctl), ('a lane line that is neither in the population of its stage nor a line only a held-out act carried', k, n)
        held |= ctl
    for k, st in LANE_STAGE.items():                    # nothing of a lane's actors in the population of its stage was left out of its input
        miss = [n for n in pop[st] if byn[n]['actor'] in lane_actors[k] and lane_of.get(n) != k and not (st == '2' and byn[n]['actor'] in FIRST)]
        assert not miss, ('population lines of a lane\'s actors that the lane did not get', k, len(miss))
    keep = sorted(pop['1'] | pop['2'] | pop['now'] | set(lane_of))
    with open(R / 'nv8_blind_spot_population.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['census_line', 'actor', 'page', 'article', 'in_population_stage_1', 'in_population_stage_2', 'in_population_now', 'lane_that_read_it', 'only_a_held_out_act_carried_it'])
        for n in keep:
            l = byn[n]; w.writerow([f'L{n:05d}', l['actor'], l['page'], l['art']] + ['yes' if n in pop[k] else '' for k in ('1', '2', 'now')] + ['para_nv8_' + lane_of[n] if n in lane_of else ('acts_nv8_added_a (its page was added on Nov 17 and read whole against the chips)' if n in late else ''), 'yes' if n in held else ''])
    c = lambda s: (len(s), sum(1 for n in s if byn[n]['actor'] in FIRST), sum(1 for n in s if byn[n]['actor'] not in FIRST))
    ab = {n for n, k in lane_of.items() if k in 'ab'}; rest = set(lane_of) - ab
    drop = next(i for i, (a, _) in enumerate(acts['now']) if a == 'nvidia'); ctl_n = len(uncarried(lines, acts['now'][:drop] + acts['now'][drop + 1:]))
    assert ctl_n > len(pop['now']), 'control: taking an act away did not enlarge the population'
    print('lines of drawn actors on counted pages that are not a direct quotation of seven words or more:', len(lines), '| of them on the nine pages added on Nov 17:', len(late), 'in the present population:', len(late & pop['now']))
    for k, name in (('1', 'stage 1 (before the first lanes)'), ('2', 'stage 2 (before lanes c to h)'), ('now', 'now')):
        t, a, b = c(pop[k]); print(f'{name}: acts {len(acts[k])} | lines no chip carries by its words {t} | of the company, its board, chairman and interim chief {a} | of the other actors {b}')
    print('lane inputs: a and b', len(ab), '=', len(ab - held), 'of the stage 1 population +', len(ab & held), 'that only a held-out act carried | c to h', len(rest), '=', len(rest - held), 'of the stage 2 population +',
          len(rest & held), 'that only a held-out act carried | all', len(lane_of), '| by lane', dict(sorted(Counter(lane_of.values()).items())))
    print('of the population now:', len(pop['now'] & set(lane_of)), 'were read by a lane |', len(pop['now'] - set(lane_of)), 'were not:', len((pop['now'] - set(lane_of)) & late), 'on the nine pages added on Nov 17 (read whole by a later reader) and', len(pop['now'] - set(lane_of) - late), 'carried by words at their lane\'s stage and not now | rows written', len(keep), '| control: without one act', ctl_n)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--freeze': freeze(sys.argv[2:4])
    else: main()
