"""The records five readers of another company's model listed on pages about Anthropic and OpenAI that the builder fetched on Nov 17, 2026 by following links on pages the two companies' rows cite
(lanes own_read_nv8_a to _d, 84 pages; and, with the answer to the thirty-third reading, lane own_read_nv8_e: 13 linked pages that reading had listed as not saved and three later reports that one of them lists.
Their own files are in research/reading_lanes as own_read_nv8_<k>.records.csv and .pages_read.csv, copied here on first run; the pages' words are not published).
Writes research/nv8_company_records.tsv: one line per record with its reader, page, the page's own day, company, kind, whether the act is inside the fifteen days, the reader's sentence, the way it cuts,
the row its reader named, and the builder's disposition, which is mechanical: `worded on <rows>` where a row of the figure cites that page with a passage that shares at least 40 letters and digits with the
record's passage; else `its reader found it on <row>` (in full or in part); else `listed, not drawn`. Run: python3 -I scripts/nv8_company_records.py

Batch s11f (Nov 18, 2026): six more readers (lanes own_read_nv8_f to _k) read the pages ANOTHER session of the project saved after 21:46 UTC on Nov 17, 2026 for other questions, where the page's text names either company
(180 pages read, 25 of them long pages read as windows around every mention; research/reading_lanes/own_read_s11f.population.tsv and .left_out.tsv hold the population, 23 folders without readable text and 32 snapshots of
aggregators' front pages that were left out; those two tables are not published). Each of those lanes also read two pages that earlier readers had read, as controls: a record of a control page is taken into the table
only when no earlier reader's record of that page shares 40 letters and digits with its passage (a second reader's additions); the rest are the same records listed twice and are counted in the last line this script prints.
One reader's sentences name an analyst firm by its founder's surname; the firm's name is written out. Sentences of those readers that name Nvidia's finance chief give the office instead (twelve sentences: three with the full name, nine with the surname), by the release's rule for names in this table; nothing else of a sentence changes.

Batch s11g (Nov 19, 2026, the answer to the forty-fourth reading, which found the builder's cut applied by impression): the last column, `why_it_is_not_drawn`, gives the builder's written reason for every record of the six
later readers that is still `listed, not drawn` (scripts/nv8_cut_decisions.py holds the cut as applied and the reasons). This script stops if such a record has no reason, or if a reason matches no listed record. The column is
empty for the records of the first five readers: those were weighed in earlier rounds, without a written reason for each.

Batch s11h (Nov 19, 2026): a twelfth reader (lane own_read_nv8_l) read the eight pages, among twenty folders another session saved after the builder's count of Nov 18, whose text names either company, and two control
pages (research/reading_lanes/own_read_s11h.population.tsv and .controls.tsv; not published). Its records are taken in by the same rules, and each one left listed has a written reason.
Batch s11k (Nov 20, 2026): a thirteenth reader (lane own_read_nv8_m) read the five pages, among thirteen folders another session saved on Nov 19, 2026 after the builder's last count, whose text names either company,
and two control pages (research/reading_lanes/own_read_s11k.population.tsv, .left_out.tsv and .controls.tsv; not published). One of the five, a list page of OpenAI's, was saved with five entries of its list as its text:
the reader was given the whole visible text of its saved HTML. Its records are taken in by the same rules, and each one left listed has a written reason. The five pages stand in the table under the ids of the
builder's own copies of the same addresses (see ALIAS below).
Batch s11m (Nov 21, 2026): three further readers (lanes own_read_nv8_n, _o, _p) read 85 pages that session saved after the thirteenth reader's, with six control pages
(research/reading_lanes/own_read_s11l.population.tsv, .left_out.tsv and .controls.tsv; not published); reader n closed incomplete over one hand-saved page with missing characters."""
import csv, re, shutil, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; RL = R / 'reading_lanes'; LANES = Path('lanes'); sys.path.insert(0, str(ROOT / 'scripts'))
import rows_map
import nv8_cut_decisions as CD
csv.field_size_limit(10**9)
LETTERS = 'abcdefghijklmnop'; SECOND = 'fghijklmnop'
for k in LETTERS:
    for n in ('records.csv', 'pages_read.csv', 'REPORT.md'):
        dst = RL / f'own_read_nv8_{k}.{n}'
        if not dst.exists():
            assert (LANES / f'own_read_nv8_{k}' / 'done' / 'DONE').exists(); shutil.copyfile(LANES / f'own_read_nv8_{k}' / 'out' / n, dst)
key = lambda s: re.sub(r'[^a-z0-9\u3400-\u9fff]', '', s.lower())        # batch s11m: Chinese characters are kept (until then a passage in Chinese was compared by its Latin letters alone, and two passages that
#   both name a company looked alike)
cited = {}
for r in rows_map.rows():
    if r.get('withdrawn'): continue
    for page, q in zip(r.get('src') or [], r.get('q') or []):
        cited.setdefault(page, []).append((r['row_id'], key(q)))
def worded(page, words):
    w = key(words); out = []
    if len(w) < 12: return out        # batch s11m: a record whose copied words hold fewer than twelve letters, digits or Chinese characters cannot be compared by this rule (an empty key stood 'in' every passage)
    for row, q in cited.get(page, []):
        if len(q) >= 12 and (q in w or w in q or any(w[i:i + 40] in q for i in range(0, max(1, len(w) - 39), 8))): out.append(row)
    return sorted(set(out), key=lambda x: (x[:2], int(x[2:])))
# Marked by hand (the thirty-fourth reading, F-COMPANY-DISPOSITION): a record that a row words from another passage of the page than the one its reader copied; the rule above compares passages and cannot see it.
# batch s10w (the thirty-fifth reading, A013): the line on the call to slow the pace now also gives the pilot stage and the plan of longer embedded work, and the rule that fills the column sees the record of the four
# agreements as worded on it. The hand mark of batch s10t is taken away, as its own check asks; the dictionary stays for a later need.
# batch s10x (the thirty-sixth reading, F002, which found one record labelled listed though a line had come to word it): the builder then read the 117 records still labelled listed on the pages from which batches s10w and s10x took
# passages, and marks here the eight that a row now words, whole or in part. The rule that fills the column compares passages and cannot see a record that a row gives in other words.
BY_HAND = {
    ('a', 'art-own-anthropic-alignment-assessment-cybersecurity-incidents', 'Newer models improved in incident replications'):
        'worded on MT76 (marked by hand: the line gives the test of the newer models with both of its halves)',
    # hand mark taken away in batch s10y (the rule sees the record since the line gained the page's passage): 'Anthropic says live blocking monitors and Fable cyber classifiers'
    # hand mark taken away in batch s10z (the rule sees the record since the line gained the page's passage): 'Biased simulation reasoning fooled the offline monitor'
    # hand mark taken away in batch s10y (the rule sees the record since the line gained the page's passage): 'Anthropic’s pre-release auditing failed to anticipate'
    ('a', 'art-own-anthropic-investigating-incidents-cybersecurity-evals', 'Anthropic says several missing operational safeguards'):
        'worded on MT76 (marked by hand, in part: the line says that the evaluations ran without the standard safeguards and that those would have blocked the behaviors)',
    ('a', 'art-own-anthropic-claude-fable-and-mythos-5-2', 'Anthropic assesses high-stakes misalignment risk as low'):
        "worded on MA428 (marked by hand: the chip gives the assessment as the company's own, beside the limits of its testing)",
    ('a', 'art-own-openai-introducing-gpt-6-cyber-wayback', 'OpenAI reports distillation and malicious-use attempts'):
        'worded on MA435 (marked by hand, in part: the protections it says it added are on the chip; the attempts it reports are not)',
    # batch s10y: nine records the thirty-seventh reading found worded on a row (its Part T), each read by the builder against the row
    ('a', 'art-own-anthropic-investigating-incidents-cybersecurity-evals', 'Anthropic publishes its initial account of three unauthorized intrusions'):
        'worded on MT76 (marked by hand, in part: the line gives the post of July 30 with its three models and what two of them did; not every detail of that account)',
    ('a', 'art-own-anthropic-investigating-incidents-cybersecurity-evals', 'Anthropic found no self-exfiltration or deliberate escape'):
        "worded on MT76 (marked by hand, in part: the line quotes the same finding, no goals beyond the assigned task and no attempts to evade oversight, from the company's assessment of September; the July post's own sentence and its words on self-exfiltration are not on it)",
    ('a', 'art-own-anthropic-investigating-incidents-cybersecurity-evals', 'Anthropic found no model pursuing a goal of its own'):
        "worded on MT76 (marked by hand, in part: the line quotes the finding of no goals beyond the assigned task from the company's assessment of September, not from the July post)",
    ('a', 'art-own-anthropic-improving-alignment-security-efforts', 'Anthropic publishes further security and alignment changes after the incidents'):
        'worded on MT76 (marked by hand, in part: the line gives, from the post of Aug 31, the blocking classifier, the stronger isolation and the wider offline monitoring; not every change the post lists)',
    ('a', 'art-own-anthropic-alignment-assessment-cybersecurity-incidents', 'Mythos 5 uploaded three malicious package versions'):
        'worded on MT76 (marked by hand, in part: the line gives the package that was downloaded and run on 15 real systems; the three versions, the leaked credentials and the database are not on it)',
    ('a', 'art-own-anthropic-claude-fable-and-mythos-5-2', 'The UK AI Security Institute tested the models before release'):
        "worded on MA428 (marked by hand, in part: the chip gives the outside organizations that tested the models and the company's sentence that they do not necessarily agree with its claims; it does not name the institute)",
    ('a', 'art-own-openai-hugging-face-incident-road-ahead-wayback', 'OpenAI publishes its Hugging Face investigation with CrowdStrike assistance'):
        "worded on MT77 (marked by hand, in part: the line quotes the company's account of Aug 26 at length; the outside firm's help and the separate independent investigations are not on it)",
    ('a', 'art-own-openai-hugging-face-incident-road-ahead-wayback', 'An agent obtained unintended internet access through Artifactory'):
        'worded on MT77 (marked by hand, in part: the line quotes that the agents gained internet access; the way they did is not on it)',
    ('b', 'art-own-amodei-on-deepseek-and-export-controls', 'Its chief executive argues that DeepSeek makes chip-export controls more important'):
        "worded on MT65 (marked by hand, in part: the line quotes the post's position on export controls and on that laboratory's chips; its argument about keeping democracies ahead is not on it)",
    ('c', 'art-own-techcrunch-261013-fbi-arrests-openai-employee', 'OpenAI said internal models analyzed a recorder'):
        "worded on MT67 (marked by hand, in part: the company's use of its models on the device is on the line; the outlet's doubt about the device is not)",
    # batch s11f: records of the six later lanes that a line words from ANOTHER page than the one its reader read (the rule compares passages of the same page and cannot see them)
    ('i', 'ms-g17-x9-tbsnews-271e10', 'Bessent said the US government was consulting Anthropic'):
        "worded on MT81 (marked by hand: the line gives his words from CNBC's own transcript of the interview that this Reuters copy relays)",
    ('i', 'ms-g17-x9-tbsnews-271e10', 'Bessent said the US government was consulting OpenAI'):
        "worded on MT82 (marked by hand: the line gives his words from CNBC's own transcript of the interview that this Reuters copy relays)",
    ('i', 'ms-p3-nvda-8k-20261117-pdf', 'Nvidia says OpenAI is among the companies building'):
        "worded on MT29 (marked by hand: the line quotes the same sentence from Nvidia's release of that day)",
    ('i', 'ms-p3-nvda-8k-20261117-pdf', 'Nvidia says it expanded Anthropic'):
        "worded on MT20 (marked by hand: the line quotes the same sentence from Nvidia's release of that day)",
    ('i', 'ms-sgp-20250417-claimsjournal-house', 'OpenAI told the House China panel'):
        "worded on MT64 (marked by hand: the line quotes the statement from the committee's report itself)",
    # batch s11g (the forty-fourth reading, T-HAND-COVERAGE and T-LISTED-COVERAGE): the mark on the report's record about grading and training data is taken away (the line now quotes that sentence, and the rule sees it);
    # records that a line words from ANOTHER page, which the reading found labelled listed, and four more the builder found for the occasions this answer adds
    ('f', 'ms-n18-political-cab0e1', 'Political.org says the company bars rivals'):
        'worded on MT81, MT82 (marked by hand, in part: both lines say, from another relay of the same Reuters report, that each company limits the use of its output to train rival models and that the technique is not in itself illegal)',
    ('f', 'ms-n18-political-cab0e1', 'Political.org reports U.S. accusations'):
        "worded on MT83, MT84 (marked by hand, in part: the talks of July in Chengdu and the Chinese officials' answer are on both lines from another relay of the same Reuters report; the accusation of September is on neither)",
    ('g', 'ms-sg2-apraug2025-c32ffc', 'The page says the House China committee'):
        "worded on MT64 (marked by hand: the line quotes the statement from the committee's report itself)",
    ('h', 'ms-sgp-20250417-taipeitimes-house', 'Taipei Times says OpenAI supported'):
        "worded on MT64 (marked by hand: the line quotes the statement from the committee's report itself)",
    ('k', 'ms-sg2-nov2026-076fdd', 'The blog says the guarantee requires'):
        "worded on MT29 (marked by hand: the line gives the exclusivity and the option from Nvidia's own filing)",
    ('g', 'ms-sg2-change-aeb715', 'AMD announced a six-gigawatt OpenAI purchase'):
        "worded on MT68 (marked by hand: the line gives the agreement and the conditional shares from an analyst firm's letter)",
    ('g', 'ms-sg2-analysts-c058a2', 'The CSIS author relays OpenAI'):
        "worded on MT68 (marked by hand: the line quotes the same sentence from the author's written testimony to a House committee)",
    ('j', 'ms-sgp-nvda-q2fy26-call-transcript-pdf', 'Nvidia partnered with OpenAI to optimize'):
        "worded on MT29 (marked by hand: the line quotes Nvidia's release for the same quarter)",
    # batch s11g, the cut applied record by record: two records that a line now gives from ANOTHER page
    # hand mark taken away in batch s11i (the rule sees the record since the line gained the report's own sentence): 'OpenAI added Amazon in February'
    ('i', 'ms-n18-yahoo-d1dd28', 'Yahoo Finance relays Nvidia'):
        "worded on MT29 (marked by hand: the line gives the same from Nvidia's release of that day)",
    # batch s11i (the answer to the forty-fifth reading; the builder's pass over the listed records under the cut's two newer kinds): one record that a line gives from another sentence of the page
    ('l', 'ms-xpost-transformer-anthropic-philanthropy-20260312', 'A Stanford philosophy professor warns'):
        "worded on MT70 (marked by hand, in part: the line gives the report's sentence that paying people to hold you accountable carries risks; his own sentence on competitive pressure is not on it)",
    # batch s11m (the forty-eighth reading, T-stale-owed): two records of the pass that were marked OWED and that a line has worded since batch s11k from another page or passage
    ('a', 'art-own-openai-hugging-face-incident-road-ahead-wayback', 'High-volume agent activity caused an Artifactory outage'):
        "worded on MT77 (marked by hand: the line gives the outage of July 4 from the evaluator's report)",
    ('d', 'art-own-chinatalk-amodei-on-ai-competition', 'Anthropic’s chief executive says controls cannot prevent tens of thousands of chips or smuggling'):
        'worded on MT65 (marked by hand: the line quotes his words that the controls were never designed to prevent tens of thousands of chips and that smuggling is to be expected)',
    # batch s11m: a sentence on the page with the closed chapter that the forty-eighth reading found partly worded
    # (a hand mark for a record in Chinese, on the line with a competitor's founder's claim, was taken away in the same batch: the rule compares Chinese characters now and sees it)
    ('a', 'art-own-anthropic-threat-intelligence-report-0926', 'Chinese public/state-security actors overcame refusals'):
        "worded on MT66 (marked by hand, in part: the line quotes the report's own sentences that a refusal was overcome on further prompting and that the model complied across many sessions; the case's other particulars are not on it)",
}
HAND_SEEN = set(); WHY_SEEN = set(); why_n = Counter()
out = []; st = Counter()
CTL = {(r['lane'][-1], r['page_id']) for n_ in ('own_read_s11f.controls.tsv', 'own_read_s11h.controls.tsv', 'own_read_s11k.controls.tsv', 'own_read_s11l.controls.tsv') for r in csv.DictReader(open(RL / n_, newline=''), delimiter='\t')}; FIRST = {}; twice = Counter()
def same(a, b):
    return bool(a and b) and (a in b or b in a or any(a[i:i + 40] in b for i in range(0, max(1, len(a) - 39), 8)))
# batch s11k: the thirteenth reader read five pages in the copies another session of the project had saved; that session's folder names hold a string the release does not publish. The table gives each of the five
# under the id of the builder's own copy of the same address (saved Nov 20 and 21, 2026; the saved texts are equal, character for character: research/reading_lanes/own_read_s11k.page_alias.tsv, not published).
ALIAS = {r['page_as_the_reader_read_it']: r['page_in_the_table'] for r in csv.DictReader(open(RL / 'own_read_s11k.page_alias.tsv', newline=''), delimiter='\t')}; assert len(ALIAS) == 5
for k in LETTERS:
    pages = {ALIAS.get(r['page_id'], r['page_id']): r for r in csv.DictReader(open(RL / f'own_read_nv8_{k}.pages_read.csv', newline=''))}
    for r in csv.DictReader(open(RL / f'own_read_nv8_{k}.records.csv', newline='')):
        if k == 'm': r['page_id'] = ALIAS.get(r['page_id'], r['page_id'])
        if k not in SECOND: FIRST.setdefault(r['page_id'], []).append(key(r['exact_words']))
        elif (k, r['page_id']) in CTL:
            if any(same(key(r['exact_words']), x) for x in FIRST.get(r['page_id'], [])): twice[k] += 1; continue
        if k in SECOND: r['what'] = re.sub(r"\bYardeni\b(?! Research)", "Yardeni Research's letter", r['what'])
        if k in SECOND: r['what'] = re.sub(r"\b(?:Colette )?Kress\b", "Nvidia's finance chief", r['what'])        # the office, not the name: the release's rule for names in this table
        if k in 'nop': r['what'] = re.sub(r"\bRyan Fedasiuk\b", "The author of a post on X", re.sub(r"\bJordan Schneider\b", "ChinaTalk's host", r['what']))        # batch s11m: two people the figure does not draw, by role
        w = worded(r['page_id'], r['exact_words']); named = r['already_on_row'].strip()
        d = ('worded on ' + ', '.join(w)) if w else (('its reader found it on ' + named) if named and named != 'none' else 'listed, not drawn')
        for (k_, p_, s_), v_ in BY_HAND.items():
            if (k_, p_) == (k, r['page_id']) and r['what'].startswith(s_): assert not w, ('the rule now sees it: take the hand mark away', s_); d = v_; HAND_SEEN.add((k_, p_, s_))
        st[(r['company'], d.split(' on ')[0].split(',')[0])] += 1
        what = re.sub(r'\s+', ' ', r['what']).strip(); ck = (k, r['page_id'], r['company'], what[:90]); why = ''
        if d == 'listed, not drawn':        # batch s11k: every reader's listed record needs a written decision (until then only the later readers' did)
            assert ck in CD.DEC, ('a listed record has no written decision', ck); assert ck not in WHY_SEEN, ('two records share a reason key', ck); WHY_SEEN.add(ck); why = CD.why(ck); why_n[(r['company'], CD.code(ck))] += 1
        else: assert ck not in CD.DEC, ('a reason is written for a record that is no longer listed: take it away', ck)
        out.append({'reader': k, 'page': r['page_id'], 'page_day_as_its_reader_read_it': pages.get(r['page_id'], {}).get('page_day', ''), 'company': r['company'], 'kind': r['kind'], 'act_inside_the_fifteen_days': r['in_the_fifteen_days'],
                    'what_in_its_reader_s_words': re.sub(r'\s+', ' ', r['what']).strip(), 'which_way_its_reader_says_it_cuts': r['cuts'], 'under_the_test_by_its_reader': r['under_the_test'], 'row_its_reader_named': '' if named == 'none' else named,
                    'the_builder_s_disposition': d, 'why_it_is_not_drawn': why})
with open(R / 'nv8_company_records.tsv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
assert HAND_SEEN == set(BY_HAND), 'a hand mark matches no record'
assert WHY_SEEN == set(CD.DEC), ('a written reason matches no listed record', sorted(set(CD.DEC) - WHY_SEEN)[:3])
c = Counter(o['company'] for o in out); cc = Counter((o['company'], o['which_way_its_reader_says_it_cuts']) for o in out if o['the_builder_s_disposition'] == 'listed, not drawn')
print('control pages of lanes f to k: records that an earlier reader had listed, left out as listed twice', dict(twice), sum(twice.values()))
print('records', len(out), dict(c), '| pages', len({o['page'] for o in out}), '| by disposition', dict(Counter(o['the_builder_s_disposition'].split(' on ')[0] for o in out)), '| listed, not drawn, by company and direction', dict(cc))
owed = Counter((o['company'], CD.code((o['reader'], o['page'], o['company'], o['what_in_its_reader_s_words'][:90]))) for o in out if o['the_builder_s_disposition'] == 'listed, not drawn')
print('every listed record has a written decision:', sum(owed.values()), '| OWED states by company', {k: v for k, v in sorted(owed.items()) if k[1].startswith('OWED')}, '| adopted sentences', sum(v for k, v in owed.items() if k[1] == 'NEW'))
sl = [o for o in out if o['reader'] in SECOND and o['the_builder_s_disposition'] == 'listed, not drawn']
print('the later readers (f to l): records', sum(1 for o in out if o['reader'] in SECOND), '| listed, each with a written reason', len(sl), dict(sorted(Counter((o['company'], o['which_way_its_reader_says_it_cuts']) for o in sl).items())), '| by company and reason', dict(sorted(why_n.items())))
