"""Run: python3 -I scripts/nv8_actor_days.py      (written after the fourteenth reading, Nov 16, 2026)
A second gauge of the chips, beside the register of remarks (scripts/nv8_gaps.py). That register lists a QUOTED remark of a drawn actor only when two
pages give it in the same words; the fourteenth reading found two acts that two articles report in different words and no chip carried. This gauge
takes every line of the census readings whose speaker is a drawn actor and whose day the reader could tell, inside the fifteen days, and lists each
actor and day that two or more counted articles carry and on which the actor has no chip. Each such actor-day was read by the builder: it is either
the same act as a chip of another day or another row (and why the days differ), or answered in the register, or it got a chip (those added
on Nov 16 are no longer listed, because the actor now has a chip that day). An actor-day with no reading stops the script.
Since the same day the actor-days that only ONE counted article carries are listed and read too (READ1; counted_articles is 1 in the table).
Writes research/nv8_actor_days.tsv. Limits: a line whose day the reader left blank is not seen; a second act on a day that already has a chip
is not seen by this gauge (scripts/nv8_remarks_no_chip.py looks for the quoted ones that two articles carry)."""
import csv, re, sys
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_gaps as G, rows_map
LETTER = 'the three chairmen\'s letter is dated Nov 4 and was released on Nov 5; the chip is on the day of release and says both'
READ = {
        ('mast', '2026-11-04'): LETTER, ('moolenaar', '2026-11-04'): LETTER, ('crawford', '2026-11-04'): LETTER,
        ('nvidia', '2026-11-10'): 'the hiring of outside counsel, announced that day: on the board\'s chip for Nov 10',
        
        
        ('mast', '2026-11-06'): 'one news service\'s three reports give the chairmen\'s request of Nov 5 as made "on Friday": the same letter as the chip for Nov 5',
        ('cramer', '2026-11-10'): 'his "I just think he\'s got to go", said on Nov 9 and reported over the following days: on his chip for Nov 9',
        ('singapore', '2026-10-31'): 'the ministry\'s statement is timed Oct 30, 11:13 PM in Singapore and its newsroom page dates it Oct 31: the chip for Oct 30 says both',
        ('trump', '2026-11-10'): 'his words of Nov 9 on what Huang told him, quoted in pieces of the next day: on his chip for Nov 9',
        ('nvidia', '2026-11-03'): 'reports of a rule the company set for its data-centre clients, from a report of Nov 2 that does not mention the affair: answered in the register of remarks (not printed)',
        }
# The actor-days that only one counted article carries (read on Nov 16, 2026, after the fourteenth reading; twelve of them held an act with no chip and
# are no longer listed, because the actor now has a chip that day).
NOC = 'no act: the page says only that no reply to a request for comment had come'
READ1 = {('bessent', '2026-11-10'): 'not on the matter: a remark on relations with China in general',
         ('blumenthal', '2026-11-05'): 'one page says he "re-upped his warning" that Thursday and another dates to the Wednesday a notice to those who had not answered his inquiry into donations to the White House ballroom; neither gives words of his on the Huang matter, and the two days differ; recorded here and not drawn',
         
         ('commerce', '2026-11-11'): NOC, ('megaspeed', '2026-11-05'): NOC, ('megaspeed', '2026-11-10'): NOC, ('whitehouse', '2026-11-11'): NOC,
         ('himes', '2026-11-12'): 'his remarks to Politico, which that page dates to Thursday and the article itself to Wednesday: on his chip for Nov 11',
         ('huang', '2026-10-30'): 'one page dates to Oct 30 what he said of Megaspeed\'s deployments; it is the interview on his chip for Oct 29 (the interviewer\'s own page is dated Oct 29)',
         ('huang', '2026-11-10'): 'not an act on the matter: a staff meeting about a product keynote, in one paper\'s account',
         ('kudlow', '2026-11-11'): 'his call of Nov 10 for Huang to step down, mentioned the next day: on his chip for Nov 10',
         ('mast', '2026-11-09'): 'the page reports as issued "today" the chairmen\'s letter dated Nov 4, which the committee posted again on Nov 9: on the chips for Nov 5',
         ('moolenaar', '2026-11-09'): 'the page reports as issued "today" the chairmen\'s letter dated Nov 4, which the committee posted again on Nov 9: on the chips for Nov 5',
         ('mcguire', '2026-11-07'): 'his thread of Nov 6, on a copy stamped the next day: on his chip for Nov 6',
         ('mcguire', '2026-11-09'): 'remarks to CNBC that Commerce took no action and should tighten controls: the position his chips of Nov 6 and Nov 10 carry, in other words; not drawn',
         ('nvidia', '2026-11-02'): 'not on the matter: a statement on data-centre policy in a report that does not mention the affair',
         ('nvidia', '2026-11-07'): 'its statement of Nov 5, reported two days later: on its chip for Nov 5',
         
         ('rubio', '2026-11-10'): 'the exchange on his chip for Nov 9: the republished transcript is titled 10 November and stamped the evening of Nov 9, Eastern time',
         ('suit', '2026-11-10'): 'the complaint filed on Nov 9, reported the next day: on its chip for Nov 9',
         ('trump', '2026-11-11'): 'that he spoke to Huang on Wednesday, said in the interview released on Nov 12: on his chip for Nov 12'}


def main():
    rem = G.lane_rows('remarks'); art = G.article_of()
    chips = defaultdict(set)
    for r in rows_map.rows():
        if r['row_id'].startswith('MA') and not r.get('withdrawn'): chips[r['actor']].add(r['date'])
    days = defaultdict(lambda: defaultdict(lambda: [set(), 0])); mapped = dated = 0
    for r in rem:
        if r.get('page_id') not in art: continue
        a = G.actor_of(G.canon(r.get('speaker') or ''), r.get('kind', ''))
        if not a or a not in chips: continue
        mapped += 1; d = (r.get('day') or '').strip()
        if not re.fullmatch(r'2026-1[01]-\d\d', d) or not '2026-10-29' <= d <= '2026-11-12': continue
        dated += 1; x = days[a][d]; x[0].add(art[r['page_id']]); x[1] += 1
    out = [(a, d, len(x[0]), x[1]) for a, dd in days.items() for d, x in dd.items() if d not in chips[a] and len(x[0]) >= 2]
    one = [(a, d, 1, x[1]) for a, dd in days.items() for d, x in dd.items() if d not in chips[a] and len(x[0]) == 1]
    unread1 = sorted(o[:2] for o in one if o[:2] not in READ1); assert not unread1, ('an actor and day in one article with no chip and no reading', unread1)
    stale1 = sorted(set(READ1) - {o[:2] for o in one}); assert not stale1, ('a reading for a single-article actor-day that is no longer listed', stale1)
    unread = [o[:3] for o in out if o[:2] not in READ]; assert not unread, ('an actor and day in two or more articles with no chip and no reading', unread)
    stale = sorted(set(READ) - {o[:2] for o in out}); assert not stale, ('a reading for an actor-day that is no longer listed', stale)
    assert ('meeks', '2026-11-12') not in {o[:2] for o in out} and '2026-11-12' in chips['meeks'], 'control: the act the reading found has its chip'
    with open(R / 'nv8_actor_days.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['actor', 'day_the_census_gives', 'counted_articles', 'census_lines', 'no_chip_that_day_because'])
        w.writerows([a, d, n, l, READ[(a, d)]] for a, d, n, l in sorted(out, key=lambda o: (-o[2], o[0], o[1])))
        w.writerows([a, d, n, l, READ1[(a, d)]] for a, d, n, l in sorted(one))
    print('census lines of drawn actors', mapped, '| with a day in the fifteen days', dated, '| actor-days in two or more articles with no chip that day:', len(out), '(each read) | in one article only:', len(one), '(each read)')


if __name__ == '__main__':
    main()
