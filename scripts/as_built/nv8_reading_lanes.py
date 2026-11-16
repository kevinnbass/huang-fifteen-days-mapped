"""Run: python3 -I scripts/nv8_reading_lanes.py      (written Nov 16, 2026, with the answer to the eighteenth reading)
What the gauges do not see, read by independent readers (another company's model, one lane each, files in research/reading_lanes/):
  single_nv8_a  every direct quotation of a drawn actor on a counted page that no chip carried by its words and that only ONE counted article
                gives (the third gauge lists such a remark only from two articles up): 294 groups and 7 planted controls;
  para_nv8_a    every census line by Nvidia that is not a direct quotation of seven words or more and that no chip of the company carried by
                its words (1,162 lines; two acts held out as controls), sorted by the reader into the acts they describe;
  para_nv8_b    the same for the board, its chairman and the interim chief (865 lines; two acts held out).
The controls: acts taken out of the table of chips the reader was given, so that the lines only they carried stood among the lines. A reader
that does not call them missing is not relied on. The reader gave each group or act one verdict; the builder then checked every CANDIDATE
against its saved page and wrote one disposition for each below (an act it is drawn on, or the reason it is not drawn). The other verdicts
(carried, reason, not on the matter, outside the days, not the actor's) are the reader's and were not read again by the builder.
Writes research/nv8_single_article_remarks.tsv and research/nv8_paraphrased_acts.tsv. Stops on a candidate with no disposition.
Limits: these are the lines of the census readings, so a remark no census reader recorded is not here; the paraphrased lines of the other
actors (about 2,850) have not been read this way; and the reader was told to set aside what was said before Oct 29, so a report of these days
about an earlier act (the figure draws some on their report's day) is not looked for."""
import csv, re, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; L = R / 'reading_lanes'; sys.path.insert(0, str(ROOT / 'scripts'))
import rows_map
OLD = 'not of these days: the page says the spokesperson said it "at the time" of an earlier claim'
SUMMARY = 'not an act of these days: the page sums up the company\'s standing position ("says", "has said") and names no occasion'
D = lambda *ids: 'drawn: ' + ', '.join(ids)
# single_nv8_a: the reader's candidates, each with the builder's disposition
ONE = {
 'G002': D('MA261'), 'G022': D('MA261'), 'G008-b': D('MA12'), 'G008-c': D('MA12'), 'G013': D('MA272'), 'G181': D('MA272'), 'G208': D('MA272'), 'G014': D('MA13'), 'G271': D('MA13'),
 'G016': D('MA264'), 'G250': D('MA264'), 'G199': D('MA264'), 'G282-b': D('MA264'), 'G282-c': D('MA264'), 'G017': D('MA42'), 'G123': D('MA42'), 'G213': D('MA42'), 'G219': D('MA42'), 'G244': D('MA42'), 'G297': D('MA42'),
 'G025': D('MA243'), 'G029': D('MA275'), 'G033': D('MA63'), 'G035': D('MA278'), 'G047': D('MA262'), 'G130': D('MA262'),
 'G285': 'drawn with the sentence the page prints just before it, that it would not hurt to hear from the Commerce Department (MA262)',
 'G051': D('MA132'), 'G156': D('MA132'), 'G276': D('MA132'), 'G299': D('MA132'),
 'G107': 'not drawn: a step in the newsletter\'s argument (that his lobbying needs no such explanation), not a hedge on its call; the reader was unsure of its test',
 'G053': D('MA255'), 'G057': D('MA266'), 'G060': D('MA280'), 'G067': D('MA276'), 'G068': D('MA172'), 'G068-b': D('MA172'), 'G069': D('MA277'), 'G141': D('MA277'), 'G070': D('MA282'), 'G071': D('MA284'),
 'G072': D('MA265'), 'G255': D('MA265'), 'G079': D('MA285'), 'G088': D('MA281'), 'G287': D('MA281'), 'G089': D('MA287'), 'G090': D('MA286'), 'G092': D('MA283'), 'G280': D('MA283'), 'G093': D('MA267'), 'G117': D('MA267'),
 'G094': D('MA279'), 'G102': D('MA279'), 'G097': D('MA19'), 'G104': D('MA45'), 'G104-b': D('MA268'), 'G111': D('MA270'), 'G113': D('MA269'), 'G291': D('MA269'),
 'G121-b': D('MA111'), 'G136': D('MA111'), 'G186': D('MA111'), 'G248': D('MA111'), 'G249': D('MA111'), 'G128': D('MA289'), 'G135': D('MA151'), 'G137': D('MA106'), 'G137-b': D('MA106'), 'G142': D('MA274'),
 'G157': 'not drawn: a staff meeting about a product keynote; that it answered the scandal is the paper\'s characterisation, which the figure does not draw (the reader called it borderline)',
 'G159': D('MA273'), 'G218': D('MA273'), 'G171': D('MA210'), 'G173': D('MA263'), 'G193': D('MA288'), 'G194': D('MA256'), 'G196': D('MA259'), 'G203': OLD, 'G229': OLD,
 'G214': D('MA52'), 'G223': D('MA52'), 'G275': D('MA52'), 'G215': 'drawn on his chip of Oct 31 (MA123): the pool report of that evening prints the answer, so it is part of that exchange and not of the later page\'s day',
 'G220': D('MA115'), 'G221': 'not drawn: the ministry on relations between the two countries, in the same answer; read the same way as its sibling sentence in the third gauge',
 'G224': D('MA251'), 'G224-b': D('MA251'), 'G224-c': D('MA251'), 'G232': D('MA35'), 'G266': D('MA78'), 'G269': D('MA290'), 'G269-b': D('MA290'), 'G273': D('MA291'), 'G288': D('MA157'), 'G292': D('MA271'),
 'G294': 'not drawn: a translated account of the Times\'s report; the board\'s own statement does not hold the clause, and what the company said of his staying is on its chip of that day (MA105)',
 'G296': D('MA257'), 'G296-b': D('MA257'), 'G298': D('MA70'),
}
PARA = {
 ('a', 'A002'): D('MA226'), ('a', 'A008'): 'carried by MA57, which was held out of the reader\'s table as a control', ('a', 'A009'): 'carried by MA57, which was held out of the reader\'s table as a control',
 ('a', 'A011'): D('MA60'), ('a', 'A012'): D('MA105'), ('a', 'A023'): D('MA63'), ('a', 'A024'): D('MA63'), ('a', 'A025'): D('MA243'), ('a', 'A027'): D('MA60'), ('a', 'A037'): D('MA179'), ('a', 'A039'): D('MA260'),
 ('a', 'A044'): SUMMARY, ('a', 'A046'): D('MA253'), ('a', 'A056'): D('MA257'), ('a', 'A057'): SUMMARY, ('a', 'A058'): SUMMARY, ('a', 'A061'): D('MA252'), ('a', 'A063'): D('MA256'), ('a', 'A066'): SUMMARY,
 ('a', 'A071'): D('MA85'), ('a', 'A085'): D('MA63'), ('a', 'A095'): SUMMARY, ('a', 'A099'): SUMMARY, ('a', 'A104'): 'carried: a relay of its reply of Nov 6 that it does not share classified information with customers (MA179)',
 ('a', 'A106'): D('MA256'), ('a', 'A107'): D('MA256'), ('a', 'A111'): D('MA256'), ('a', 'A112'): D('MA254'), ('a', 'A116'): D('MA258'), ('a', 'A119'): D('MA255'),
 ('a', 'A120'): 'carried: a relay of its statements of that day that the block on sales stands (MA255, MA256)',
 ('a', 'A121'): 'carried: the same statement given to another outlet a day later, one sentence word for word (MA57, MA241)',
 ('b', 'A002'): D('MA60'), ('b', 'A003'): 'carried by MA61, which was held out of the reader\'s table as a control', ('b', 'A005'): D('MA260'), ('b', 'A006'): D('MA260'), ('b', 'A007'): D('MA62'), ('b', 'A011'): D('MA243'),
 ('b', 'A012'): D('MA260'), ('b', 'A013'): D('MA260'), ('b', 'A014'): D('MA260'), ('b', 'A023'): 'carried by MA215, which was held out of the reader\'s table as a control',
 ('b', 'A025'): 'not drawn: her signature on the company\'s filing; the filing is on the board\'s chip of that day (MA63)', ('b', 'A032'): 'carried: a relay of the board\'s meeting and decision (MA62)', ('b', 'A033'): D('MA260'),
}


# People who are not drawn and hold no public office are named by role, in the lines' first words and in the readers' own words too.
# The names and their roles are in a file that is not published (research/reading_lanes/roles.private.tsv: pattern, role, one per line).
SCRUB = [tuple(x.split('\t')) for x in (L / 'roles.private.tsv').read_text().split('\n') if x.strip() and not x.startswith('#')]


def scrub(t):
    for pat, role in SCRUB:
        t = re.sub(pat, role, t)
    assert not any(re.search(pat, t) for pat, _ in SCRUB), t
    return t


def main():
    ids = {r['row_id'] for r in rows_map.rows()}
    for v in list(ONE.values()) + list(PARA.values()):
        for i in re.findall(r'MA\d+', v): assert i in ids, ('a disposition names an act that is not there', i)
    grp = {r['group_id']: r for r in csv.DictReader(open(L / 'single_nv8_a.groups.tsv'), delimiter='\t')}
    ctl = {r['group_id']: r for r in csv.DictReader(open(L / 'single_nv8_a.controls.tsv'), delimiter='\t')}
    out = []; c = Counter(); found = 0
    for r in csv.DictReader(open(L / 'single_nv8_a.out.csv')):
        b = r['group_id'].split('-')[0]; cand = r['verdict'].startswith('CANDIDATE'); isc = ctl[b]['is_control'] == 'yes'
        if isc:
            disp = 'a planted control: the act was held out of the reader\'s table (' + ctl[b]['control_for'] + ')'; found += cand
        elif cand:
            assert r['group_id'] in ONE, ('a candidate with no disposition', r['group_id'], r['actor']); disp = ONE[r['group_id']]
        else:
            assert r['group_id'] not in ONE, ('a disposition for a group the reader did not call a candidate', r['group_id']); disp = ''
        c[(r['verdict'], 'control' if isc else ('drawn' if disp.startswith('drawn') else ('not drawn' if cand else '')))] += 1
        first = scrub(' '.join(grp[b]['quoted_lines'].split()[:14])) if r['group_id'] == b else '(a passage beside the group\'s line)'
        out.append([r['group_id'], r['actor'], grp[b]['page_id'].split()[0], first, r['verdict'], r['act'], r['test'], 'yes' if isc else '', disp])
    n_ctl = sum(1 for x in ctl.values() if x['is_control'] == 'yes'); assert found == n_ctl, ('a planted control the reader did not call a candidate', found, n_ctl)
    with open(R / 'nv8_single_article_remarks.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['group', 'actor', 'page', 'first_words_of_the_quoted_line', 'reader_verdict', 'act_the_reader_named', 'test_the_reader_named', 'planted_control', 'builder_disposition_of_a_candidate']); w.writerows(out)
    base = [o for o in out if '-' not in o[0]]; cands = [o for o in out if o[4].startswith('CANDIDATE') and not o[7]]
    print('single-article quotations: groups', len(base), '| planted controls', n_ctl, 'found', found, '| passages beside a group', len(out) - len(base),
          '| reader verdicts', dict(Counter(o[4] for o in out)), '| candidates that are not controls', len(cands), '| drawn', sum(o[8].startswith('drawn') for o in cands), '| not drawn or already carried', sum(not o[8].startswith('drawn') for o in cands))
    pout = []; tot = Counter()
    for lane in ('a', 'b'):
        acts = list(csv.DictReader(open(L / f'para_nv8_{lane}.acts.csv'))); lines = {r['line_id']: r['act_no'] for r in csv.DictReader(open(L / f'para_nv8_{lane}.lines.csv'))}
        n_in = sum(1 for _ in open(L / f'para_nv8_{lane}.lines_in.tsv')) - 1; assert len(lines) == n_in, ('a line the reader did not place', lane, len(lines), n_in)
        held = Counter(lines[r['line_id']] for r in csv.DictReader(open(L / f'para_nv8_{lane}.controls.tsv'), delimiter='\t') if r['only_a_held_out_act_carried_it'] == 'yes')
        for a in acts:
            cand = a['verdict'].startswith('CANDIDATE'); k = (lane, a['act_no'])
            if cand: assert k in PARA, ('a candidate with no disposition', k)
            else: assert k not in PARA, ('a disposition for an act the reader did not call a candidate', k)
            tot[(lane, 'acts')] += 1; tot[(lane, 'candidates')] += cand; tot[(lane, 'drawn')] += cand and PARA[k].startswith('drawn')
            pout.append(['para_nv8_' + lane, a['act_no'], a['actor'], a['lines'], held.get(a['act_no'], 0) or '', a['verdict'], a['chip'], scrub((a['chip_wording'] or a['note'])[:240]), PARA.get(k, '')])
        tot[(lane, 'lines')] = n_in
    with open(R / 'nv8_paraphrased_acts.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['lane', 'act_as_the_reader_numbered_it', 'actor', 'census_lines_sorted_into_it', 'of_them_lines_only_a_held_out_act_carried', 'reader_verdict', 'chip_the_reader_named', 'what_it_is_in_the_reader_s_words', 'builder_disposition_of_a_candidate']); w.writerows(pout)
    print('paraphrased lines: ' + ' | '.join(f"para_nv8_{l}: lines {tot[(l, 'lines')]}, acts {tot[(l, 'acts')]}, candidates {tot[(l, 'candidates')]}, drawn {tot[(l, 'drawn')]}" for l in ('a', 'b')))


if __name__ == '__main__':
    main()
