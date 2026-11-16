"""Run: python3 -I scripts/nv8_refusals.py      (written Nov 16, 2026, after the sixteenth reading)
The instances behind the figure's rule for refusals to comment: every explicit refusal by a drawn actor to comment on its own conduct or part
in the matter is drawn, once for each documented response, with any answer the same source prints beside it.
Part 1 lists every act whose words carry a refusal (the instances drawn), from the rows.
Part 2 takes the lines of the census readings that hold words of refusal, on counted pages, by a speaker matched to a drawn actor. A line is
"inside" when its article is one that a refusal act of that actor cites (the acts' final sources, as published). Every other line is listed
with the builder's classification of it: another outlet's relay of a response that an act draws from its original (the act is named), or not
a refusal to comment (a refusal to act, a declined invitation or meeting told in a report, a fall in value). The classification is made by
written rules over the line's words and checked by reading; a line no rule classifies stops the script. The lines' words are not published.
(The seventeenth reading, Nov 16: the first version used the acts before their added original sources and gave 52 and 79 where the
published sources give 54 and 77; and it gave only totals.)
Writes research/nv8_refusals.tsv. Limits: the words searched are a fixed list (decline, no comment, refuse to say, would not say, unable to
comment, not going to comment, demur); a refusal a reader paraphrased otherwise, or one on a page with no line in the census readings, is not
seen. A relay is matched to the response it repeats by what it says was asked, not by proof that no second request was made. A candidate
finder, like the gauges: it does not prove that every refusal is drawn.
Control: with the act that draws Anthropic's refusal taken away, the article that carries it must fall into the second kind."""
import csv, re, sys
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_gaps as G, rows_map
REF = re.compile(r"declin|no comment|not comment|n't comment|unable to comment|refus\w* to (?:comment|say|answer|discuss)|would not (?:say|discuss|answer|confirm|immediately comment)|wouldn't (?:say|discuss|answer|confirm)|demur|not going to comment|cannot comment", re.I)
NOT_A_REFUSAL = re.compile(r"declin\w* (?:in|of) (?:the )?(?:market|value|share)|precipitous decline|stock decline|The decline followed|declining to impose", re.I)


# The builder's classification of a line that stands outside the cited articles: (actor, words in the line, classification). First match wins.
NOTC = 'not a refusal to comment: '
RULES = [
    ('huang', r"Warren|Senate|Banking", NOTC + 'an invitation to testify declined before these days, told in a report'),
    ('huang', r"declined to comment", 'relay of the Times report of Nov 11, in which his answer by phone is on his own chip (MA107) and the company\'s refusal is MA195'),
    ('trump', r"declin\w* to (impose|act)|declined to act", NOTC + 'a decision not to act, told in a report'),
    ('moolenaar', r"continued to decline", NOTC + 'his words about Huang declining a request'),
    ('banks', r"declining to impose", NOTC + 'his words about a decision not to act'),
    ('commerce', r"declined (a meeting|Nvidia's request|the request)|agents declined", NOTC + 'a meeting declined in 2025, told in a report'),
    ('nvidia', r"agents declined|declined Nvidia's request", NOTC + 'a meeting declined in 2025, told in a report'),
    ('commerce', r"internal discussions|entity list", 'relay of the refusal to the FT for its report on the entity list (MA196)'),
    ('commerce', r"other allegations", 'relay of the refusal Axios reported (MA207)'),
    ('bessent', r"Treasury", 'relay of the refusal to the FT for its report on the entity list (MA204)'),
    ('nvidia', r"appear|testif|brief|Congress", 'relay of the refusal to say whether Huang would appear before the committees (MA57)'),
    ('nvidia', r"Korea", 'relay of the refusal at the event in Seoul (MA197)'),
    ('nvidia', r"classified|booked|sales", 'relay of the refusal to say how the customer\'s sales were classified (MA199)'),
    ('nvidia', r"memo|intimate|alleged relationship|relationship with Alice", 'relay of the refusal to the FT on the memo (MA179)'),
    ('nvidia', r"has not commented", NOTC + 'the page says only that no comment had been made'),
    ('nvidia', r"Powell|statement|allegation|second|newspaper|declined to comment", 'relay of one of the company\'s refusals of Nov 5 to Nov 11 (MA57, MA179, MA195), by the report the page relays'),
    ('rubio', r"State Department", 'relay of the State Department\'s refusals to the Times (MA201, MA203)'),
    ('rubio', r"comment", 'relay of his exchanges with reporters of Nov 8 and Nov 9 (MA74, MA189)'),
    ('whitehouse', r"NSA|National Security Agency", 'relay of the refusal to the Times for its first report (MA193)'),
    ('whitehouse', r"State Department", 'relay of the refusal to the Times for its report on the secretary of state\'s memo (MA200)'),
    ('whitehouse', r"CIA|Central Intelligence|did not comment|declined to comment", 'relay of the refusals to the Times and the FT on the memo (MA194) or, for the entity-list report, to the FT (MA202)'),
    ('justice', r"Manhattan", 'relay of the refusal on the report of an inquiry led from Manhattan (MA169)'),
    ('justice', r"continuing investigations|Justice|DOJ", 'relay of the department\'s answers of Nov 9 (MA205)'),
    ('justice', r"FBI", 'relay of the FBI\'s refusals of Nov 9 and Nov 10 (MA205, MA206)'),
    ('singapore', r"specifics|further details|unable to comment", 'relay of the police\'s reply of Oct 30 (MA70)'),
    ('megaspeed', r"declined to comment", 'relay of the refusal to the Times for its profile (MA208)'),
    ('taiwan', r"comment|declin", 'relay of a refusal on one of its chips (MA217 to MA221)'),
    ('anthropic', r"declined to comment", 'relay of the refusal Quartz reports (MA86)'),
    ('suit', r"declin", NOTC + 'a fall in value'),
    ('board', r"decline", NOTC + 'a fall in the share price'),
]


def split(acts, lines, art):
    ref = defaultdict(list)
    for rid, a in acts:
        if REF.search(a['what']) and not a.get('withdrawn'): ref[a['actor']].append((rid, {art.get(s) for s in a['src']} - {None}))
    inside = outside = 0; out_arts = defaultdict(set)
    for a, ar, *_ in lines:
        if any(ar in arts for _, arts in ref.get(a, [])): inside += 1
        else: outside += 1; out_arts[a].add(ar)
    return ref, inside, outside, out_arts


def main():
    art = G.article_of(); acts = [(r['row_id'], r) for r in rows_map.rows() if r['row_id'].startswith('MA')]; lines = []          # the rows as published: sources found later are attached
    for r in G.lane_rows('remarks'):
        if r.get('page_id') not in art: continue
        t = (r.get('direct_quote') or '') + ' ' + (r.get('remark') or ''); a = G.actor_of(G.canon(r.get('speaker') or ''), r.get('kind', ''))
        if a and REF.search(t) and not NOT_A_REFUSAL.search(t): lines.append((a, art[r['page_id']], r['page_id'], (r.get('day') or '').strip(), ' '.join(t.split())))
    ref, inside, outside, out_arts = split(acts, lines, art)
    held = [(rid, a) for rid, a in acts if a['actor'] == 'anthropic' and REF.search(a['what'])]; assert len(held) == 1, 'control: the act that draws Anthropic\'s refusal'
    _, _, _, o2 = split([x for x in acts if x[0] != held[0][0]], lines, art); assert o2.get('anthropic'), 'control: without that act its article is not in the second kind'
    rows = [['a refusal drawn', a['actor'], a['date'] or 'before the calendar', 'the day of its report' if a['reported'] else 'its own day', rid, a['what']] for rid, a in acts if REF.search(a['what']) and not a.get('withdrawn')]
    rows.sort(key=lambda r: (r[1], r[2], r[4]))
    cited = {a: [(rid, arts) for rid, arts in v] for a, v in ref.items()}; have = {rid for v in ref.values() for rid, _ in v}; out_rows = []; unread = []
    for a, ar, page, d, t in lines:
        if any(ar in arts for _, arts in cited.get(a, [])): continue
        c = next((c for act, pat, c in RULES if act == a and re.search(pat, t, re.I)), None)
        if c is None: unread.append((a, ar, page, t[:160])); continue
        ids = re.findall(r'MA\d+', c); assert not ids or any(x in have for x in ids), ('a relay points at no refusal act', c)
        out_rows.append(['a line outside the cited articles', a, d, '', ar, c])
    assert not unread, ('a line with words of refusal that no rule classifies', unread)
    rows += sorted(out_rows, key=lambda r: (r[1], r[4]))
    pairs = len({(r[1], r[4]) for r in out_rows})
    with open(R / 'nv8_refusals.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['part', 'actor', 'day', 'placed_on', 'act', 'words_or_count']); w.writerows(rows)
    n = sum(1 for r in rows if r[0] == 'a refusal drawn')
    print('acts whose words carry a refusal:', n, 'by', len({r[1] for r in rows if r[0] == 'a refusal drawn'}), 'actors | census lines with words of refusal by drawn actors:', len(lines), '| in an article such an act cites:', inside, '| outside:', outside,
          'lines in', pairs, 'actor-article pairs, of which relays', sum(1 for r in out_rows if r[5].startswith('relay')), 'and not refusals to comment', sum(1 for r in out_rows if r[5].startswith('not a refusal')),
          '| control: without its act, Anthropic\'s article is outside')


if __name__ == '__main__':
    main()
