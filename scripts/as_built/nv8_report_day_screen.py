"""Run: python3 -I scripts/nv8_report_day_screen.py      (written while answering the fourteenth reading, Nov 16, 2026)
A screen of the acts that sit on the day their report was published (a dashed left edge), for two faults found on one act each.
 1 Another saved page gives the act's own day. The Commerce secretary's reply to the president was drawn on Nov 11 from a page that gives no
   day, while another saved page puts it in the Oval Office on Nov 5; it was moved (act MA76). For every other such act the screen takes the
   words the act quotes and the passages it cites, and lists every line of the census readings by the same drawn actor that shares four words
   in a row with them and to which the reader gave another day.
 2 The act's own source gives the day. A representative's remarks to Politico had a dashed edge although the article says the interview was
   "on Wednesday"; the edge is solid now (act MA160). For every other such act the screen lists each sentence with a day word (a weekday,
   "today", "yesterday", "on Nov 9") within 800 characters before and 300 after a passage the act cites, in the act's own cited pages.
 3 The page was changed after the chip's day (added Nov 16, 2026, on a lead from the project's fact-check session: some saved pages carry text about a
   later event than their stamp). A chip dated by its report sits on the day the page was first published; where the page's own header gives a
   later day of modification, or the page was first published later than the chip's day, the passage may come from a later version. The screen
   lists every such act with the two days; the reading says whether the chip's day rests on something else (a day in the text, another page) or
   whether the passage "may be newer" than the chip's day. The figure's note counts the latter.
After the sixteenth reading (Nov 16) part 3 also reads the update line a hand-saved article prints ("Published Nov 6 Updated Nov 7"): the reading
found three acts the screen had missed because it read only the saver's header.
After the fifteenth reading (Nov 16) the day is read from the source's ordinary context too: a remark dated with others like it ("several senators
told the paper on Tuesday"), or an answer to something that happened that day in a report of that day, has its day and a solid edge.
After the nineteenth reading (Nov 16) the screen has a fourth and a fifth part, which read the saved pages themselves and not the census lines.
One article's earlier saved version had shown that a reply sat on the right day for the wrong reason and two others on the wrong footing.
 4 An earlier page holds a cited passage. For every passage of 30 characters or more that an act dated by its report cites, the screen lists
   each page of the figure's table of pages (research/nv8_articles.tsv), dated from Oct 29 on and before the chip's day, whose text holds
   the passage: the act may have been reported earlier than the chip says.
 5 A copy of the same article lacks a cited passage. It lists each other page of the cited page's article (same article id), of the chip's
   day or earlier and with at least half the cited page's length of article text (so that a teaser is not taken for a version), whose text does not hold the passage: the passage may have been added in a
   later version. Honorifics ("Mr.", "Ms.") are dropped on both sides, since licensed copies drop them.
 6 The page's day is an update's. A hand-saved article can print only "Updated <day>", and the table of pages then gives it that day. The
   screen lists each act that sits on such a day: the article may have been first published earlier (the nineteenth reading's point about
   one reply to the Journal).
Each listed act was read by the builder and the reading is in the table; a listed act with no reading stops the script.
Controls: each part is run once more with its corrected act put back as it was, and must list it.
Writes research/nv8_report_day_screen.tsv. Limits: part 1 does not see an act that quotes no words a census line repeats, or a line whose day
the reader left blank; part 2 reads only the pages an act cites and only near the passages cited. A day word near a passage is most often the
day of another event, so every hit is read; where a page implies the day without stating it, the edge stays dashed and the reading says so."""
import csv, datetime, re, sys
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_gaps as G, rows_map, check_rows
MOVED = ('MA76', '2026-11-11')            # part 1's control: the act that was moved, and the day it sat on
SOLID = 'MA160'                           # part 2's control: the act whose edge became solid
OTHER = 'the day word belongs to another event told in the same passage; the page gives this act no day'
READ1 = {'MA179': 'not the same act: other statements of the company, of other days, that share only the words "the U.S. government" with this one',
         'MA164': 'not the same act: the lines of Nov 12 are the company\'s later statement of that day, which has its own chip; the statement to the Times has no day but its report\'s',
         'MA195': 'not the same response: other refusals of the company, on other days, that share only the words of refusal with this one',
         'MA199': 'not the same response: other refusals of the company, on other days, that share only the words of refusal with this one',
         'MA196': 'a similar statement of the day before to another outlet (it is on the chip for Nov 9); the sixteenth reading judged this one a separate answer, to the FT',
         'MA214': 'the two accounts of the extension\'s date, both of which the chip gives (one page: Monday, Nov 9; another: Nov 5)',
         'MA238': 'not the same act: its statements of Oct 29 and Nov 12, which have their own chips, share only the words on cooperating with the government',
         'MA240': 'not the same act: the company\'s reply of Nov 6 to another report of the Times (its chip of that day) says a similar thing of China\'s limits on imports',
         'MA211': 'not the same act: the line of Nov 8 is his acknowledgment to employees, which the cited passage mentions and which has its own chip',
         'MA210': 'the census gives these lines other days; the sixteenth reading compared them with his saved posts of Nov 6 and Nov 8 and found the quotations only in the piece of Nov 10',
         'MA251': 'the same sentence on what customers receive is in the statement the company gave on Nov 5 (its chip of that day), which CNBC says largely mirrored its first; Tom\'s Guide prints it on Oct 29 as told to it',
         'MA258': 'not the same act: lines of other days that share only the words of a request for comment that went unanswered',
         'MA260': 'not the same act: the lines of Nov 12 are the announcement of the interim chief and of the search (the board\'s chips of that day); this act is the reports of the day before',
         'MA266': 'not the same act: the lines of Nov 4 and 5 are the chairmen\'s letter and its release (his chip for Nov 5); this is a comment the FT prints on Nov 9',
         'MA306': 'not the same act: the lines of other days are the chairmen\'s letter and his interviews of Nov 10 and 11 (his chips of those days), which share a few common words with it',
         'MA85': 'not the same act: a line of Nov 8 that shares only the words "an Nvidia spokesperson said" with a passage cited here',
         'MA312': 'the lines of Nov 5 are the company\'s statement of that day and its spokesman\'s words and refusal to the Times (its chip of that day), which say similar things of his security team; this act is what its representative told The National, printed Nov 6, and the chip says the page does not tell whether that was a separate exchange',
         'MA313': 'the same words are in its statement to CNBC of Nov 8 (its chip of that day); The National prints them on Nov 9 as a statement made to it, and the chip says so. The lines of Nov 12 share only the words "said in a statement"',
         'MA316': 'not the same act: lines of Nov 8 and Nov 11 that share only the words "the Nvidia board is" with this one',
         'MA330': 'not the same act: lines of Nov 9 and Nov 10 about his call to Huang, which share only a few common words ("that Alice Huang was", "a spy, according to") with a passage cited here'}
READ2 = dict({k: OTHER for k in ('MA13', 'MA16', 'MA32', 'MA51', 'MA85', 'MA109', 'MA125', 'MA128', 'MA130', 'MA150', 'MA158',
                                 'MA199', 'MA200', 'MA201', 'MA202', 'MA203', 'MA206', 'MA210', 'MA212', 'MA213', 'MA219', 'MA207', 'MA237', 'MA250',
                                 'MA251', 'MA256', 'MA257', 'MA261', 'MA266', 'MA268', 'MA270', 'MA274', 'MA275', 'MA280', 'MA283', 'MA284', 'MA286', 'MA288',
                                 'MA301', 'MA302', 'MA307', 'MA308', 'MA309', 'MA312', 'MA313', 'MA319', 'MA320', 'MA324', 'MA328', 'MA330')},
             MA317='"Sunday" is the day of Huang\'s admission. The page, published on the evening of Wednesday Nov 11, says analysts were "reacting to the news in real time", which suggests the remark is of that day, but it gives the remark itself no day: the edge stays dashed',
             MA316='"today" is Electronics Weekly\'s own word, in a page stamped 06:13 UTC on Nov 12 (01:13 in the eastern United States): the report\'s day, and the chip says the page does not tell whether it means the session of Wednesday night; "Wednesday" is Semafor\'s day for that session (the board\'s chip of Nov 11)',
             MA211='the day word ("today", Nov 9) is that of the Wired report as the relaying page gives it; the hiring itself has no day, and another saved page says he hired the firm "as early as last year"',
             MA214='the page says "On Monday" (Nov 9) and another saved page dates the same extension Nov 5; the accounts conflict, so the act sits on the day of the first report and the chip gives both days',
             MA81='the day is the one on which sources told the broadcaster of an inquiry already under way: the report\'s day, and the inquiry may be earlier',
             MA169='the day words are those of the resignation and of the report itself (Nov 12): the report\'s day',
             MA179='the day word is that of a senator\'s pledge of the Saturday after, which shows the FT page was changed after its first day; another saved page says the FT reported the refusal "on Friday" (Nov 6, the chip\'s day)',
             MA195='the day word is that of the paper\'s phone call to Huang; the page does not say when the company declined',
             MA254='the paper says the general counsel spoke "as recently as last week", and the chip says the week before; the day words near the passage belong to remarks of others',
             MA260='the page says the board "met on Wednesday evening" (its chip for Nov 11); the reports this act relays are of that day',
             MA263='the day word dates the lawmakers\' calls for a briefing; the page gives the interview no day',
             MA271='the day word dates a senator\'s remark printed before his; the page gives his no day')
NEWER = 'may be newer: the page was changed the day after it was first published, and the passage could come from the later version; the chip keeps the day of first publication'
READ3 = {'MA16': 'the chip\'s day is that of the FT report it relays and of the podcast\'s own page (Nov 10); the later page is a second relay that says "yesterday"',
         'MA46': 'the chip\'s day is the one the relaying page gives for the Times article that quotes the post (Nov 8); the page itself is of the next day',
         'MA81': 'the chip\'s day is in the text: sources told the broadcaster "on Monday"; the relaying page is later',
         'MA85': 'the chip\'s day is that of the reporting agency\'s own page, saved by hand and stamped Nov 9; the company\'s answer is in a reprint of the report published at 08:32 on Nov 10 in Singapore, which is still Nov 9 in the eastern United States (the Business Times); the later pages are a relay of it and a timeline',
         'MA120': NEWER, 'MA128': NEWER,
         'MA158': 'the Times page prints an update of Nov 12; the quotation is also in a licensed copy of the article at an address dated Nov 11 (the Boston Globe\'s)',
         'MA179': 'the FT page prints an update of Nov 7; another saved page says the FT reported the refusal "on Friday" (Nov 6), and the statement to the Times is in a page of Nov 6',
         'MA194': 'may be newer, for the FT\'s part only: the FT page prints an update of Nov 7 and no other saved page dates the refusal to it; the refusal to the Times is in a page of Nov 6',
         'MA199': 'may be newer, for Reuters\'s part only: its page prints "Updated November 13"; the Journal\'s and the FT\'s parts are in pages of Nov 12',
         'MA210': 'may be newer: the think tank\'s page was first published Nov 10 and changed Nov 12, and no other saved page carries the quotations',
         'MA211': 'the chip\'s day is that of the Wired report as a page of Nov 9 that was not changed on a later day relays it (TechCrunch); the second relaying page was changed the next day, and the other page\'s line is given in the chip with its own date (Nov 11). (The first page was changed once, within the same day, Eastern time.)',
         'MA217': 'the Journal\'s page prints an update of Oct 31; a licensed copy of an earlier version of the article, timed Oct 30, carries the sentence (found while answering the nineteenth reading; the reading here had said it may be newer)',
         'MA299': 'the Journal\'s page prints an update of Oct 31; a licensed copy of an earlier version of the article, timed Oct 30, carries the embassy\'s answer whole',
         'MA219': 'the chip\'s day is that of the first report (Asia Economy, Nov 10); the other page cited is a later account, of Nov 11',
         'MA207': 'the chip\'s day is that of the first saved report (a page of Nov 11 that relays Axios); the other page cited is a later relay, of Nov 12',
         'MA239': 'may be newer in one word: the Times page prints an update of Nov 8; a relay of Nov 7 (the Jerusalem Post) carries the answer, the penalties and the hiring, without the word "all"',
         'MA240': 'the Times page prints an update of Nov 8; a relay of Nov 7 (the Jerusalem Post) carries both quotations and the sentence on China\'s limits (found by the eighteenth reading)',
         'MA260': 'Semafor\'s page was changed the next morning; its version of 10:27 pm on Nov 11, saved as another page, and Daring Fireball\'s quotation of that version carry every passage cited here (the one clause only the later version has, on a chief operating officer, is on the board\'s chip of Nov 12)',
         'MA275': 'may be newer: the page was changed the day after it was first published, and no other saved page carries the remark',
         'MA313': 'may be newer: the page was changed the day after it was first published, and no other saved page carries the statement as one made to The National; the words themselves are in its statement to CNBC of Nov 8',
         'MA214': 'the chip\'s day is that of the first report (Yahoo Finance, Nov 10); the other page cited is a later account, of Nov 12, and the chip gives its date too'}
WIRE = 'copies of one wire dispatch, all of the chip\'s day: the sentence is in the longest copy only, and no day turns on it'
READ4 = {'MA81': 'the earlier page is one a broadcaster kept updating: it is dated Nov 8 by its first publication and says the sources spoke "on Monday" (Nov 9), the chip\'s day',
         'MA130': 'two findings. The sentence on revenue is in a page of the evening of Nov 11 as told to another outlet (drawn there, act MA317; this chip says so). '
                  'The remark on the next decade is paraphrased in a page first published Nov 11 and changed Nov 12; the earliest unchanged page that carries it is of Nov 12, where the chip sits',
         'MA150': 'not the same act: the passage is the president\'s remark of Nov 9, which the report quotes and earlier pages carry; the act drawn is the magazine\'s own report of Nov 10',
         'MA155': 'the earlier page is a blog post dated Nov 8 that its author extended until Nov 12 (its header gives both days); it quotes the Times article of Nov 9',
         'MA158': 'not the same act: the line "This article originally appeared in The New York Times" stands on every licensed copy of a Times article',
         'MA213': 'the cited page is itself of Nov 10: the chip sits on Nov 12 for its first part and gives Nov 10 in words for this one',
         'MA252': 'the cited page is the earlier version of the article (Oct 30), cited to show where its paragraph ends without the sentence; the chip sits on the day of the version that carries it',
         'MA268': 'the cited page is a live report that began on Nov 11; the entry that carries the remark has its own stamp of Nov 12',
         'MA299': 'not the same act: the page of Oct 29 gives the embassy\'s reply to the Times of that day (its chip of Oct 29) in words that begin alike',
         'MA316': 'the cited page was first published Nov 11 and changed on the morning of Nov 12; the clause is in the changed version only, and the chip says so'}
READ5 = {'MA85': 'the passage is the time stamp the hand-saved page prints, cited for the day; the other copy of the report carries its passages',
         'MA158': 'the passage is an address printed on the licensed copy, cited for its date; the Times\'s own page has no such line',
         'MA169': WIRE, 'MA212': WIRE,
         'MA252': 'the earlier version of the article (a licensed copy timed Oct 30) lacks the sentence, which is why the chip sits on Oct 31, the day of the version that carries it',
         'MA316': 'the earlier version of the article (10:27 pm on Nov 11) lacks the clause, which is why it sits on Nov 12, the day of the version that carries it'}
READ6 = {'MA252': 'an earlier version of the article, timed Oct 30, is saved and lacks the sentence: the chip sits on the day of the version that carries it, which is the update\'s (see part 5)',
         'MA273': 'the page prints only an update line (Nov 9, 2:59 pm); its text speaks of "Monday morning trade" (Nov 9) and of the print edition of Nov 10, so the article was first published that day',
         'MA307': 'the page prints only an update line (Nov 12, 7:44 pm); its text reports what a senator "told reporters Thursday" (Nov 12), so the article was first published that day',
         'MA309': 'the page prints only an update line (Nov 12, 7:44 pm); its text reports what a senator "told reporters Thursday" (Nov 12), so the article was first published that day',
         'MA328': 'the page prints only an update line (Nov 11, 12:56 in India, which is 2:26 am in the eastern United States); its text gives the closing share price of Tuesday, Nov 10, so the article was first published in the ten hours before that stamp, on Nov 10 or Nov 11 Eastern time: the chip keeps the day the page prints'}
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


def stamps(pid):
    """(day first published, day modified), US Eastern, from the header the saver wrote on the page's text; '' where the header has none."""
    for n in ('text.txt', 'text.article.txt', 'text.reextract.txt'):
        f = check_rows.PRIMARY / pid / n
        if f.exists():
            t = f.read_text(errors='replace')[:3000]
            return tuple(eastern((re.search(k + r': *(\S+)', t) or [None, ''])[1]) for k in ('PUBLISHED', 'MODIFIED'))
    return '', ''


def eastern(s):
    m = re.match(r'(\d{4}-\d\d-\d\d)(?:T(\d\d):(\d\d)(?::\d\d(?:\.\d+)?)?(Z|[+-]\d\d:?\d\d)?)?', s or '')
    if not m: return ''
    if not m.group(2): return m.group(1)
    off = m.group(4) or 'Z'; h, mi = (0, 0) if off == 'Z' else (int(off[:3]), int(off[0] + off[-2:]))
    return (datetime.datetime.fromisoformat(f'{m.group(1)}T{m.group(2)}:{m.group(3)}') - datetime.timedelta(hours=h, minutes=mi) - datetime.timedelta(hours=5)).date().isoformat()


MONTH = {'oct': 10, 'nov': 11}


def printed_update(pid):
    """The day a hand-saved article prints as its update ("Published NOV 6 2026 Updated NOV 7 2026"), or ''. The sixteenth reading found that
    the screen read only the saver's MODIFIED header and so missed these."""
    for n in ('text.article.txt', 'text.txt'):
        f = check_rows.PRIMARY / pid / n
        if f.exists():
            m = re.search(r'Updated\s+(?:on\s+)?(Oct|Nov)[a-z]*\.?\s+(\d{1,2}),?\s+2026', f.read_text(errors='replace')[:6000], re.I)
            return f'2026-{MONTH[m.group(1).lower()]:02d}-{int(m.group(2)):02d}' if m else ''
    return ''


def part3(acts):
    """The day of first publication is the one the figure's own table of pages gives (research/nv8_articles.tsv, where every page is dated by
    one rule); for a page outside that table, the header's; the day of modification is the header's."""
    day = {r['page_id']: r['day'] for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')}; out = []
    for rid, a in acts:
        later = [(p, day.get(p) or stamps(p)[0], max(stamps(p)[1], printed_update(p))) for p in sorted(set(a['src']))]; later = [x for x in later if max(x[1], x[2]) > a['date']]
        if later: out.append((rid, a['actor'], a['date'], '; '.join(f'first published {x[1] or "?"}, changed {x[2] or "?"}' for x in later)))
    return out


HON = re.compile(r'\b(?:Mr|Ms|Mrs|Dr)\. ')


def part45(acts):
    """Parts 4 and 5 (see the top). The pages searched are those of the figure's table of pages; a page's day is the one that table gives."""
    tab = {r['page_id']: r for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')}; byart = defaultdict(list)
    for pid, r in tab.items(): byart[r['article_id']].append(pid)
    text = {pid: HON.sub('', check_rows.haystack(pid) or '') for pid in tab}
    out4, out5 = [], []
    for rid, a in acts:
        early, lack = set(), set()
        for s_, q in zip(a['src'], a['q']):
            qq = HON.sub('', check_rows.norm(q))
            if qq.startswith('PUBLISHED') or len(qq) < 30: continue
            early |= {(tab[p]['day'], p) for p, t in text.items() if '2026-10-29' <= tab[p]['day'] < a['date'] and qq in t}
            if s_ in tab:
                n = int(tab[s_]['chars'] or 0); lack |= {(tab[p]['day'], p) for p in byart[tab[s_]['article_id']] if p != s_ and tab[p]['day'] and tab[p]['day'] <= a['date'] and 2 * int(tab[p]['chars'] or 0) >= n and qq not in text[p]}
        if early: out4.append((rid, a['actor'], a['date'], '; '.join(f'{d} {p}' for d, p in sorted(early))))
        if lack: out5.append((rid, a['actor'], a['date'], '; '.join(f'{d} {p}' for d, p in sorted(lack))))
    return out4, out5


def part6(acts):
    tab = {r['page_id']: r for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')}; out = []
    for rid, a in acts:
        up = sorted({p for p in a['src'] if p in tab and tab[p]['day'] == a['date'] and re.match(r'\s*Updated\b', tab[p]['day_read_from'] or '')})
        if up: out.append((rid, a['actor'], a['date'], '; '.join(f"{p}: {tab[p]['day_read_from']}" for p in up)))
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
    p4, p5 = part45(rep)
    for name, out, READ in (('another saved page gives another day', part1(rep, by), READ1), ('a day word near a cited passage in its own source', part2(rep), READ2),
                            ('its page was changed after the chip\'s day', part3(rep), READ3), ('an earlier page holds a cited passage', p4, READ4), ('a copy of the same article lacks a cited passage', p5, READ5), ('the day of its page is an update\'s', part6(rep), READ6)):
        unread = [o[0] for o in out if o[0] not in READ]; assert not unread, (name, 'a listed act with no reading', unread)
        stale = sorted(set(READ) - {o[0] for o in out}); assert not stale, (name, 'a reading for an act no longer listed', stale)
        rows += [[name] + list(o) + [READ[o[0]]] for o in out]
    moved = byid[MOVED[0]]; assert moved['date'] != MOVED[1] and not moved['reported'], moved['date']
    c1 = part1([(MOVED[0], dict(moved, date=MOVED[1]))], by); assert c1 and moved['date'] in c1[0][3], ('control 1: the moved act, put back on its report\'s day, is not listed', c1)
    assert not byid[SOLID]['reported']; c2 = part2([(SOLID, byid[SOLID])]); assert c2 and 'Wednesday' in c2[0][3], ('control 2: the act whose edge became solid is not listed', c2)
    with open(R / 'nv8_report_day_screen.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['screen', 'act', 'actor', 'day_drawn_the_reports_day', 'what_the_screen_saw', 'reading']); w.writerows(rows)
    c3 = part3([('MA128', dict(byid['MA128']))]); assert c3 and 'changed' in c3[0][3], ('control 3: an act whose page is known to have been changed the next day is not listed', c3)
    n3 = sum(1 for r in rows if r[0].startswith('its page')); newer = sum(1 for r in rows if r[0].startswith('its page') and r[5].startswith('may be newer'))
    n1 = sum(1 for r in rows if r[0].startswith('another')); n4 = sum(1 for r in rows if r[0].startswith('an earlier page')); n5 = sum(1 for r in rows if r[0].startswith('a copy')); n6 = sum(1 for r in rows if r[0].startswith('the day of its page'))
    b252 = byid['MA252']; c5 = part45([('MA252', dict(b252, src=[x for x in b252['src'] if x == 'man-923fe8754943'], q=[y for x, y in zip(b252['src'], b252['q']) if x == 'man-923fe8754943' and 'photos' in y]))])[1]
    assert c5 and 'art-fc-itiger-wsj-1030-v1' in c5[0][3], ('control 5: the reply whose sentence an earlier version lacks is not listed', c5)
    emb = byid['MA299']; c4 = part45([('MA299', dict(emb, date='2026-10-31'))])[0]; assert c4 and 'art-fc-itiger-wsj-1030-v1' in c4[0][3], ('control 4: the reply put back on Oct 31 is not listed with the earlier copy that carries it', c4)
    print('acts dated by their report\'s day', len(rep), '| another saved page gives another day:', n1, '| a day word near a cited passage:', len(rows) - n1 - n3 - n4 - n5 - n6, '| page changed later:', n3, 'of which may be newer:', newer,
          '| an earlier page holds a cited passage:', n4, '| a copy of the article lacks one:', n5, '| page dated by an update line:', n6, '(each read) | controls:', c1[0][3], '|', c2[0][3], '| the earlier copy lists the two replies it settled')


if __name__ == '__main__':
    main()
