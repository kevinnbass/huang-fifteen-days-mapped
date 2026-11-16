"""Run: python3 -I scripts/nv8_refusals.py      (written Nov 16, 2026, after the sixteenth reading)
The instances behind the figure's rule for refusals to comment: every explicit refusal by a drawn actor to comment on its own conduct or part
in the matter is drawn, once for each documented response, with any answer the same source prints beside it.
Part 1 lists every act whose words carry a refusal (the instances drawn), from the rows.
Part 2 counts the lines of the census readings that hold words of refusal, on counted pages, by a speaker matched to a drawn actor: how many
stand in an article that a refusal act of that actor cites, and how many do not. The second kind were read by the builder: they are other
outlets' relays of a response drawn from its original, or not refusals to comment (a refusal to act, a fall in value, a declined invitation of
an earlier year). They are counted here and not listed one by one.
Writes research/nv8_refusals.tsv. Limits: the words searched are a fixed list (decline, no comment, refuse to say, would not say, unable to
comment, not going to comment, demur); a refusal a reader paraphrased otherwise, or one on a page with no line in the census readings, is not seen. A candidate
finder, like the gauges: it does not prove that every refusal is drawn.
Control: with the act that draws Anthropic's refusal taken away, the article that carries it must fall into the second kind."""
import csv, re, sys
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_gaps as G, rows_map
REF = re.compile(r"declin|no comment|not comment|n't comment|unable to comment|refus\w* to (?:comment|say|answer|discuss)|would not (?:say|discuss|answer|confirm|immediately comment)|wouldn't (?:say|discuss|answer|confirm)|demur|not going to comment|cannot comment", re.I)
NOT_A_REFUSAL = re.compile(r"declin\w* (?:in|of) (?:the )?(?:market|value|share)|precipitous decline|stock decline|The decline followed", re.I)


def split(acts, lines, art):
    ref = defaultdict(list)
    for rid, a in acts:
        if REF.search(a['what']) and not a.get('withdrawn'): ref[a['actor']].append((rid, {art.get(s) for s in a['src']} - {None}))
    inside = outside = 0; out_arts = defaultdict(set)
    for a, ar in lines:
        if any(ar in arts for _, arts in ref.get(a, [])): inside += 1
        else: outside += 1; out_arts[a].add(ar)
    return ref, inside, outside, out_arts


def main():
    art = G.article_of(); acts = [(f'MA{i:02d}', a) for i, a in enumerate(rows_map.acts(), 1)]; lines = []
    for r in G.lane_rows('remarks'):
        if r.get('page_id') not in art: continue
        t = (r.get('direct_quote') or '') + ' ' + (r.get('remark') or ''); a = G.actor_of(G.canon(r.get('speaker') or ''), r.get('kind', ''))
        if a and REF.search(t) and not NOT_A_REFUSAL.search(t): lines.append((a, art[r['page_id']]))
    ref, inside, outside, out_arts = split(acts, lines, art)
    held = [(rid, a) for rid, a in acts if a['actor'] == 'anthropic' and REF.search(a['what'])]; assert len(held) == 1, 'control: the act that draws Anthropic\'s refusal'
    _, _, _, o2 = split([x for x in acts if x[0] != held[0][0]], lines, art); assert o2.get('anthropic'), 'control: without that act its article is not in the second kind'
    rows = [['a refusal drawn', a['actor'], a['date'] or 'before the calendar', 'the day of its report' if a['reported'] else 'its own day', rid, a['what']] for rid, a in acts if REF.search(a['what']) and not a.get('withdrawn')]
    rows.sort(key=lambda r: (r[1], r[2], r[4]))
    rows += [['census lines with words of refusal', a, '', '', '', f"{sum(1 for x in lines if x[0] == a)} lines; in articles no refusal act of this actor cites: {len(out_arts.get(a, ()))} articles (read by the builder: relays, or not refusals to comment)"]
             for a in sorted({x[0] for x in lines})]
    with open(R / 'nv8_refusals.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['part', 'actor', 'day', 'placed_on', 'act', 'words_or_count']); w.writerows(rows)
    n = sum(1 for r in rows if r[0] == 'a refusal drawn')
    print('acts whose words carry a refusal:', n, 'by', len({r[1] for r in rows if r[0] == 'a refusal drawn'}), 'actors | census lines with words of refusal by drawn actors:', len(lines), '| in an article such an act cites:', inside, '| not:', outside,
          '| control: without its act, Anthropic\'s article is outside')


if __name__ == '__main__':
    main()
