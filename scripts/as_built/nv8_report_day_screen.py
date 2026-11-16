"""Run: python3 -I scripts/nv8_report_day_screen.py      (written while answering the fourteenth reading, Nov 16, 2026)
A screen of the acts that sit on the day their report was published (a dashed left edge), for two faults found on one act each.
 1 Another saved page gives the act's own day. The Commerce secretary's reply to the president was drawn on Nov 11 from a page that gives no
   day, while another saved page puts it in the Oval Office on Nov 5; it was moved (act MA76). For every other such act the screen takes the
   words the act quotes and the passages it cites, and lists every line of the census readings by the same drawn actor that shares four words
   in a row with them and to which the reader gave another day.
 2 The act's own source gives the day. A representative's remarks to Politico had a dashed edge although the article says the interview was
   "on Wednesday"; the edge is solid now (act MA160). For every other such act the screen lists each sentence with a day word (a weekday,
   "today", "yesterday", "on Nov 9") within 800 characters before and 300 after a passage the act cites, in the act's own cited pages.
Each listed act was read by the builder and the reading is in the table; a listed act with no reading stops the script.
Controls: each part is run once more with its corrected act put back as it was, and must list it.
Writes research/nv8_report_day_screen.tsv. Limits: part 1 does not see an act that quotes no words a census line repeats, or a line whose day
the reader left blank; part 2 reads only the pages an act cites and only near the passages cited. A day word near a passage is most often the
day of another event, so every hit is read; where a page implies the day without stating it, the edge stays dashed and the reading says so."""
import csv, re, sys
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_gaps as G, rows_map, check_rows
MOVED = ('MA76', '2026-11-11')            # part 1's control: the act that was moved, and the day it sat on
SOLID = 'MA160'                           # part 2's control: the act whose edge became solid
OTHER = 'the day word belongs to another event told in the same passage; the page gives this act no day'
READ1 = {'MA164': 'not the same act: the lines of Nov 12 are the company\'s later statement of that day, which has its own chip; the statement to the Times has no day but its report\'s'}
READ2 = dict({k: OTHER for k in ('MA13', 'MA16', 'MA32', 'MA36', 'MA51', 'MA85', 'MA102', 'MA109', 'MA125', 'MA128', 'MA130', 'MA150', 'MA153', 'MA154', 'MA158')},
             MA29='the page was published on the day of the briefing (Nov 9) and the quoted words say "today"; it does not state the day of the remark, so the edge stays dashed; the chip sits on the same day either way',
             MA30='the day word is that of the briefing; the page gives the remark no day',
             MA45='the day words belong to other events and to a photo caption; the page gives the remark no day (it answers the resignation announced that day)',
             MA129='the section that prints his emailed words opens "tech analysts said on Monday" (Nov 9, the chip\'s day); the page does not say when the email was sent, so the edge stays dashed; the chip sits on the same day either way',
             MA81='the day is the one on which sources told the broadcaster of an inquiry already under way: the report\'s day, and the inquiry may be earlier',
             MA156='the page dates the legislators\' calls of that Thursday, the report\'s day, and gives this remark no day of its own',
             MA165='the page dates the closed briefing (Nov 9), not the remark made after it; the chip says so',
             MA169='the day words are those of the resignation and of the report itself (Nov 12): the report\'s day')
DAY = re.compile(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|yesterday|today|on (?:Oct|Nov)\w*\.? \d+)\b")


def norm(s):
    return re.sub(r'[^a-z0-9 ]+', ' ', s.lower().replace('’', "'").replace("'", '')).split()


def shingles(words, n=4):
    return {' '.join(words[i:i + n]) for i in range(len(words) - n + 1)}


def part1(acts, by):
    out = []
    for rid, a in acts:
        want = set()
        for q in re.findall(r'"([^"]+)"', a['what']) + list(a['q']): want |= shingles(norm(q))
        days = defaultdict(set)
        for r, art in by.get(a['actor'], []):
            d = (r.get('day') or '').strip()
            if re.fullmatch(r'2026-1[01]-\d\d', d) and d != a['date'] and want & shingles(norm((r.get('direct_quote') or '') + ' ' + (r.get('remark') or ''))): days[d].add(art)
        if days: out.append((rid, a['actor'], a['date'], '; '.join(f'{d} ({len(days[d])})' for d in sorted(days))))
    return out


def part2(acts):
    out = []
    for rid, a in acts:
        words = set()
        for s, q in zip(a['src'], a['q']):
            t = check_rows.haystack(s) or ''; qq = check_rows.norm(q); k = t.find(qq)
            if k < 0 or qq.startswith('PUBLISHED'): continue
            words |= {m.group(0) for m in DAY.finditer(t[max(0, k - 800):k + len(qq) + 300])}
        if words: out.append((rid, a['actor'], a['date'], ', '.join(sorted(words))))
    return out


def main():
    art = G.article_of(); by = defaultdict(list)
    for r in G.lane_rows('remarks'):
        if r.get('page_id') not in art: continue
        a = G.actor_of(G.canon(r.get('speaker') or ''), r.get('kind', ''))
        if a: by[a].append((r, art[r['page_id']]))
    acts = [(f'MA{i:02d}', a) for i, a in enumerate(rows_map.acts(), 1)]; byid = dict(acts)
    rep = [(rid, a) for rid, a in acts if a['reported'] and a['date'] and not a.get('withdrawn')]
    rows = []
    for name, out, READ in (('another saved page gives another day', part1(rep, by), READ1), ('a day word near a cited passage in its own source', part2(rep), READ2)):
        unread = [o[0] for o in out if o[0] not in READ]; assert not unread, (name, 'a listed act with no reading', unread)
        stale = sorted(set(READ) - {o[0] for o in out}); assert not stale, (name, 'a reading for an act no longer listed', stale)
        rows += [[name] + list(o) + [READ[o[0]]] for o in out]
    moved = byid[MOVED[0]]; assert moved['date'] != MOVED[1] and not moved['reported'], moved['date']
    c1 = part1([(MOVED[0], dict(moved, date=MOVED[1]))], by); assert c1 and moved['date'] in c1[0][3], ('control 1: the moved act, put back on its report\'s day, is not listed', c1)
    assert not byid[SOLID]['reported']; c2 = part2([(SOLID, byid[SOLID])]); assert c2 and 'Wednesday' in c2[0][3], ('control 2: the act whose edge became solid is not listed', c2)
    with open(R / 'nv8_report_day_screen.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['screen', 'act', 'actor', 'day_drawn_the_reports_day', 'what_the_screen_saw', 'reading']); w.writerows(rows)
    n1 = sum(1 for r in rows if r[0].startswith('another')); print('acts dated by their report\'s day', len(rep), '| another saved page gives another day:', n1, '| a day word near a cited passage:', len(rows) - n1,
                                                                    '(each read) | controls:', c1[0][3], '|', c2[0][3])


if __name__ == '__main__':
    main()
