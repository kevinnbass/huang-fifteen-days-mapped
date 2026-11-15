"""nv8, the fortnight mapped: all the coverage two aggregators listed, who acted on which day, and every documented
tie between an actor and a party with something at stake, on one sheet.

Layout, all in one coordinate system (HTML boxes placed over one SVG layer):
  top right   one dot per piece listed on the story, stacked by the day it was first listed (research/harvest.tsv)
  below       one row per actor (scripts/rows_map.py), one chip per dated act, on the same day axis
  left        the tie network: Anthropic, its people and vehicles, institutions, with a line into each actor's row
  beside rows arcs for ties between two actors who both have rows
A tie ends at a person or body, never at an act: the figure shows records side by side and claims no motive.
Tie colours were checked with the dataviz palette script (orange, blue, aqua pass together; purple beside blue fails).

fig_web(..., panels=N) cuts that sheet into N slices set side by side, at the same scale and type sizes. The groups of rows
keep their order and are shared out so that the slices come out as equal in height as whole groups allow. Each slice has its
own day axis and its own copy of the network, holding only the boxes with a line into its rows, so no line runs from one
slice to another. The dots sit over the last slice's calendar (top right of the page, as the subtitle says) with the boxed
note beside them; the three numbers and the tie legend move up beside the title; the footnote is set in N columns.
panels=1 draws the one tall sheet exactly as before."""
import csv, datetime, itertools, math, re
def CONDUIT(gr):
    """The footnote's sentence on gifts given through ActBlue or WinRed after the last candidate-committee line on file."""
    a, n = gr['anthropic'], gr['nvidia']
    who = []
    for side, label in (('anthropic', 'Anthropic'), ('nvidia', 'Nvidia')):
        for x in gr[side]['conduit_after_drawn'].split():
            k, c, v = x.split(':'); who.append(f"{int(c)} {label} line{'s' if int(c) != 1 else ''} (${float(v):,.0f}) for the committee of {next(a_[2] for a_ in rows_map.ACTORS if a_[0] == k)}")
    return (f"No line of a sitting member's campaign committee dated after {MON(a['last_candidate_committee_line'])} is on file yet from either company's employees. Gifts made through the conduits ActBlue and WinRed after that day are on file only as the conduits' own lines "
            f"({int(a['conduit_lines_after'])} from people who gave Anthropic as employer, ${float(a['conduit_usd_after']):,.0f}; {int(n['conduit_lines_after'])} for Nvidia, ${float(n['conduit_usd_after']):,.0f}) and are not counted until the recipient's own report shows them; "
            + ('among the members drawn they name only ' + ' and '.join(who) + '. ' if who else 'none of them names a committee of a member drawn. '))



def NEGATIVES(gift_rate, key2name):
    """The footnote's sentence on what the sums are: positive receipt lines, with the negative lines listed and not netted."""
    neg = list(csv.DictReader(open(R / 'employee_gift_negatives.csv', newline='')))
    drawn = [n for n in neg if n['member']]
    words = '; among the members drawn, ' + ' and '.join(f"${-float(n['usd']):,.0f} returned by a committee of {key2name[n['member']]}" for n in drawn) if drawn else ''
    a, n = gift_rate['anthropic'], gift_rate['nvidia']
    return (f"Sums are of positive receipt lines, in whole dollars as the FEC's bulk file gives them. Negative lines on the same committees (refunds and chargebacks: "
            f"{a['negative_lines_not_netted']} for Anthropic, ${-float(a['negative_usd_not_netted']):,.0f}; {n['negative_lines_not_netted']} for Nvidia, ${-float(n['negative_usd_not_netted']):,.0f}) "
            f"are listed with the tables and not taken off{words}. A person is counted by surname and first given name; in six of the counts a name occurs with a second spelling or ZIP code, "
            "which shows neither two people nor one, and the count stays as the rule gives it. ")


def LOOKUP_WORDS(n_pages):
    """The footnote's sentences on the look-ups of analysts and bylines, with every number from research/nv8_lookup_counts.tsv and,
    for the whole-name search, research/nv8_name_search_counts.tsv (scripts/nv8_name_search.py)."""
    L = rows_map.LOOKUPS; a = lambda w: L.get(('analysts', w), 0); b = lambda w: L.get(('bylines', w), 0)
    k = lambda reg, w: L.get((reg, w), 0)
    S = {r['what']: int(r['count']) for r in csv.DictReader(open(R / 'nv8_name_search_counts.tsv', newline=''), delimiter='\t')}
    left = S['not searched as a whole name (bylines that are an agency, a label or an address; analyst labels under four letters)']
    assert S['controls found, of 7'] == 7
    same = a('not drawn: cannot tell') + a('not drawn: name match, not settled')
    same_words = '1 the look-up could not tell apart from another person of the same name' if same == 1 else f'{same} the look-up could not tell apart from others of the same name'
    W = lambda n: {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}.get(n, str(n))
    other = b('pairs: record of another kind, not drawn'); assert other == 2, other        # the two the next sentence describes
    return (f"The articles counted quote {rows_map.N_ANALYSTS} analysts, experts and research groups (a person or firm written two ways is counted once). Each was looked up in the records held. "
            f"On Nov 15 the names not drawn were searched again as whole names in the {S['tables searched']} tables of the four evidence sets: {S['people: different names searched']:,} names of two to four words among the analysts and the bylines (people's names, and a few firms and labels of the same form), "
            f"and {S['others: different names searched']} other firm names and one-word names among the analysts; {left} entries (bylines that are an agency, a label or an address, and analyst labels under four letters) were left out of that pass. "
            f"The {rows_map.N_ANALYSTS_DRAWN} drawn each have a remark of these days and a tie on record to Anthropic, Open Philanthropy or Nvidia: their own (a fellowship, research support, a past post, a seat on an advisory council) "
            "or that of the organisation where they hold a post (an award to it, a paid business relationship, a paper it was commissioned to write); each row says which, and an award to an organisation is not a payment to the person. "
            "At a university an award counts for a person only where the record names that person's own unit. "
            f"Not drawn: {a('not drawn: none found for the person')} people at universities whose only award on record names the university as a whole, or another researcher there; "
            f"{a('not drawn: not drawn')} for whom the record is a remark or report not shown to be of these days, a past post at a group funded only later, a grant from another company, a grant to their group from an investor in Anthropic, or an invitation to speak with no post or payment on record; "
            f"{same_words}; {a('not drawn: at a bank, not drawn')} entries that are one of the banks below or its analysts; and the other {a('not drawn: none found')}, for whom no record was found. No tie is implied for anyone not drawn. "
            "Bank analysts, and investors quoted for their view of the shares, are not drawn, whatever their ties; three investors, Ackman, Maguire and Conway, are drawn among the public voices, under that row's rule of three articles. "
            f"Quartz reported on Sep 4, 2026, citing unnamed sources of Bloomberg's, that Anthropic was nearing a credit facility before its share sale, and named {k('banks', 'named by Quartz on Sep 4, 2026 as lenders to Anthropic')} banks in it, four of them also leading the sale; the report says the details could still change. "
            f"Analysts, or executives in office, of {k('banks', 'of those, with an analyst, a note or an executive quoted on the saved pages')} of those banks are quoted on the saved pages. The banks' business with Nvidia was not looked up. "
            + {2: "Two quoted investors are described on the pages as a shareholder and a short seller of Nvidia. ", 1: "One quoted investor is described on the pages as holding or shorting Nvidia shares. "}[k('investors', 'quoted and described on the pages as holding or shorting Nvidia shares')] +
            f"The pages counted carry {b('pairs of outlet and name')} bylines, counting a name once for each outlet it appears at: {b('different names')} different names, {b('names that are an agency or not a person' + chr(39) + 's name')} of them agencies or not a person's name. "
            "These are the bylines of the pages counted, those of the first search and those saved since; a page saved as an actor's own original is cited on that actor's chip and its byline is not counted here. "
            f"Each was looked up in the fellowship and staff records held and, on Nov 15, in the whole-name search. {rows_map.NUMBER[rows_map.N_BYLINES_DRAWN].capitalize()} have a tie on record and are drawn: "
            "Perlo and Hashim from the records held, Kubinec from his own bio at The Dispatch, Mowshowitz and Schneider from pages saved on Nov 15 (the first look-up had missed both). "
            f"{W(other).capitalize()} more have a record of another kind and no tie is drawn: a congressional fellow of the 2021 cohort of a programme that Open Philanthropy funded in 2025 (the record shows no overlap), "
            "and a reporter named on the page of a CSET event. A CSET staff member's byline on a CSET release of 2025 is no longer counted, because that page is dated before these days (he also wrote CSET's two releases of Nov 10 and 11, which are drawn in CSET's row). "
            f"For {W(b('pairs: name match, not settled'))} the tables hold the name and nothing ties it to the reporter. Pages that could not be saved were not checked. "
            "The lists of the names looked up are not published, because most name people for whom nothing was found; the counts and the rules are. ")


def OWN_CHANNEL_WORDS():
    """The footnote's sentences on the search of the actors' own channels, with every number from research/nv8_s6_counts.tsv
    (scripts/nv8_s6_counts.py, which reads research/nv8_s6_items.tsv)."""
    C = {r['what']: int(r['count']) for r in csv.DictReader(open(R / 'nv8_s6_counts.tsv', newline=''), delimiter='\t')}
    n_chips = sum(1 for r in rows_map.rows() if r['row_id'].startswith('MA')); searched = C['chips whose original was searched for']       # every chip ever drawn, one since withdrawn among them
    W = lambda n: rows_map.NUMBER.get(n, {7: 'seven', 8: 'eight', 9: 'nine'}.get(n, n))
    held, loc, cx = C['actors: an item about the affair is held and was read'], C['actors: links located, none could be read'], C['actors: only items that are not about the affair or not their own']
    n_act = C['actors whose own channels were searched']; unsearched = [a[2] for a in rows_map.ACTORS if a[0] in ('hodges', 'conway')]
    assert n_act == 80 and len(unsearched) == 2 and len(rows_map.WITHDRAWN) == 1 and C['actors: the reader matched an item about the affair to a chip, and the project holds no copy'] == 0 and loc == 2
    return (f"The own channel (official site, newsroom, own feed or account) of each of the {C['actors whose own channels were searched']} actors who had spoken was searched once for these fifteen days by a reader from another model family: "
            "on Nov 14 for the 63 then drawn, on Nov 15 for the 14 added since and then for the three members drawn later that day (the two share-price rows have none; one voice among the 80 is no longer drawn). "
            "The two people drawn last, an adviser and an investor, have not had their own channels searched. "
            f"An item about the affair is held and was read for {held} (the three papers among them, through articles saved by hand); for {rows_map.NUMBER.get(loc, 'two')} links were located and none could be saved (Anthropic's SEC filings, a page of OpenAI's); "
            f"{rows_map.NUMBER.get(cx, cx)} had only items that do not mention the affair or are not their own; for {C['actors: nothing found on a channel that could be read']} a channel that could be read showed no item about the affair in these fifteen days; "
            f"for {C['actors: no channel could be read']} no channel could be read. An item is counted only where the project holds the page, and a share-sale filing or policy paper that a chip draws as context is not counted as an item about the affair. "
            "The reader could open no account on X in either round, and a channel with nothing found is not proof of silence. "
            f"Of the {searched} chips drawn before those searches, the original was read and is now cited for {C['chips: original read and cited on the chip']}; for {W(C["chips: the search did not yield the original; a saved copy of the publisher's page is now cited"])} more the search did not yield the original, but a saved copy of the publisher's page is now cited (one of them shows only the opening); "
            f"for {W(C['chips: the search could not open the post; the post itself, saved afterwards by its id, is now cited'])} more the reader could not open a post on X, and the post itself, saved afterwards by its id, is now cited; for one it carries the first of the chip's two remarks; "
            f"for {C['chips: original could not be opened']} it still could not be opened (posts on X and Truth Social, broadcasters' video, papers behind a paywall); "
            f"for {rows_map.NUMBER.get(C['chips: original found by the reader and refused to the project (not saved)'], 'two')} the reader found it and the site refused the project's own copy (the Journal's page, an SEC filing); and for {C['chips: original not found']} it was not found. "
            f"Of the chips still without their original, {C["chips still without their original that now also cite a paper's own report of the act"]} now also cite a paper's own report of the act, from the papers' pages saved since the first census. "
            f"The {n_chips - searched} chips added without such a search each cite the actor's own page, the paper's own article (some in a licensed copy) or, where neither is held, a report that the chip names. ")


def ARTICLE_WORDS():
    """How the saved pages become the articles counted, with every number from research/nv8_articles.tsv (scripts/nv8_articles.py)."""
    rows = list(csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t'))
    n1 = sum(r['set'] == 'first census' for r in rows); n2 = len(rows) - n1
    arts = {r['article_id'] for r in rows}; cnt = {r['article_id'] for r in rows if r['counted'] == 'yes'}
    why = Counter('after' if 'after the fifteen days' in r['why_not'] else 'before' if 'before the fifteen days' in r['why_not'] else 'no text' if 'no article text' in r['why_not'] else 'not news'
                  for r in rows if r['counted'] == 'no')
    assert sum(why.values()) == sum(r['counted'] == 'no' for r in rows) and why['not news'] == sum('not a news piece' in r['why_not'] for r in rows)
    undated = sum(1 for r in rows if r['counted'] == 'yes' and not r['day'])
    return (f"Counts of who is named or quoted are counts of articles, each counted once: the {n1:,} pages saved by the first search and the {n2} saved since (the papers' own articles, saved by hand or in a licensed copy, and a few transcripts) "
            f"are {len(arts):,} articles once copies of one article are joined (the same address, or four fifths of the shorter text inside the longer), and {len(cnt):,} of them are counted. "
            f"A page is not counted when its own date, read as a U.S. Eastern day, is after Nov 12 ({why['after']} pages) or before Oct 29 ({why['before']}, background pages), when no text could be read ({why['no text']}) or when it is not a news piece ({why['not news']}); "
            f"{undated} pages carry no date and are counted. A republished copy dated later than its original is counted only through a counted copy of the same article. ")


def LOBBY_WORDS():
    """The footnote's sentences on lobbyists' gifts on all three sides, from research/lobbyist_gifts_map.csv (scripts/build_lobbyist_gifts_map.py)."""
    g = list(csv.DictReader(open(R / 'lobbyist_gifts_map.csv', newline='')))
    own = [r for r in g if r['measure'] in ('named', 'firm_only', 'firm_only_not_classified')]
    tot = lambda side, named: sum(float(r['amount_usd']) for r in own if r['side'] == side and (r['measure'] == 'named' or not named))
    M = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']; mo = lambda d: f"{M[int(d[5:7]) - 1]} {d[:4]}"
    S_ = {r['what']: r['value'] for r in csv.DictReader(open(R / 'lobbyist_gifts_map_summary.tsv', newline=''), delimiter='\t')}
    a, b = S_['first gift counted'], S_['last gift counted']
    return (f"The same record was then pulled for both companies: the lobbyists' contribution reports for {S_['years of reports read']} of all {S_['firms whose reports were read (registered for Nvidia, for Anthropic or for a group Open Philanthropy funds)']} firms registered for Nvidia, for Anthropic or for one of the groups above. "
            f"To the {S_['members drawn']} members drawn, in gifts of {mo(a)} to {mo(b)} made while the firm was registered for the client, lobbyists listed for the client gave ${tot('nvidia', True):,.0f} on Nvidia's side, ${tot('anthropic', True):,.0f} on Anthropic's and ${tot('network', True):,.0f} on the groups' side; "
            f"counting every lobbyist at those firms, ${tot('nvidia', False):,.0f}, ${tot('anthropic', False):,.0f} and ${tot('network', False):,.0f}. A firm registered for two clients puts one gift on two sides, so the sides are not added up. "
            "Each member's row gives its lines from this table by the same rule for each side: every gift of a lobbyist at a firm then registered for the client, and how much of it came from lobbyists listed for that client. "
            "The table is published with the figure. For the Speaker and for Sen. Kennedy, who share a surname with other members, only a gift whose report gives the office is counted. ")

MON = lambda d: (lambda p: f"{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(p[1]) - 1]} {int(p[2])}, {p[0]}")(d.split('-'))      # 2026-10-14 -> Oct 14, 2026
from collections import Counter, OrderedDict, defaultdict

from PIL import ImageFont

import member_mentions, rows_context, rows_coverage, rows_map, rows_people, rows_ties, story_scope
from fig_common import *

R = ROOT / 'research'
PAGE = 3320; W = PAGE - 120
X_ROOT, W_ROOT = 0, 190
X_MID, W_MID = 300, 246
X_INST, W_INST = 712, 214
X_NAME, W_NAME = 996, 322
X_T0 = 1332; T_W = W - X_T0; DAY_W = T_W / 15
PITCH = 6.0; DOT_R = 2.35
ROW_MIN, HDR_H, GAP = 46, 52, 14
ROW_MIN_GROUP = {'analysts': 80, 'bylines': 62}      # room for the institution boxes beside these rows
DAYS = [(datetime.date(2026, 10, 29) + datetime.timedelta(d)).isoformat() for d in range(15)]
WD = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# one line per day for the axis: a pointer to chips drawn below, nothing that is not in a row
DAYNOTE = {'2026-10-29': 'First report, in the Times', '2026-10-30': 'Journal report; Singapore denies it', '2026-10-31': 'Trump: "I would like to say yes"',
           '2026-11-03': 'Midterms: Democrats win both chambers', '2026-11-05': 'House chairs\' letter released', '2026-11-06': 'Memo reported; two posts on X',
           '2026-11-07': 'Coons: "Congress will investigate"', '2026-11-08': 'Huang\'s memo; board inquiry', '2026-11-09': 'Nvidia shares fall; rivals rise',
           '2026-11-10': 'Schumer speech; Anthropic IPO range', '2026-11-11': 'Second report; calls to resign', '2026-11-12': 'Huang resigns'}
# tie kinds as drawn: colour, dash, legend wording
KIND = OrderedDict([('money', (ORANGE, '', 'Money: contribution, donation, grant award, agreed stock purchase')),
                    ('own', (ORANGE, '2 5', 'Employees\' own contributions: their money, not the company\'s')),
                    ('ad', (ORANGE, '10 6', 'Named in ads it announced')),
                    ('lobby', ('#b0499b', '', 'Its lobbying reports name a bill he sponsors')),      # magenta: passes the palette check beside orange, blue and aqua
                    ('post', (BLUE, '', 'Post or seat held now; its own body')),
                    ('past', (BLUE, '10 6', 'Former post')),
                    ('act', (AQUA, '', 'Official act: an order, an award')),
                    ('meet', ('#8a8c82', '2 6', 'Same session scheduled; testimony to his committee'))])
KMAP = {'own': 'own', 'lobby': 'lobby', 'post': 'post', 'money': 'money', 'ad': 'ad', 'role': 'post', 'seat': 'post', 'past': 'past', 'grant': 'money', 'panel': 'meet', 'act': 'act', 'meet': 'meet'}
# coverage classes
THREE = {'nytimes.com', 'wsj.com', 'ft.com'}
OPN = re.compile(r'/opinion|/opinions/|commentisfree|/leaders/|breakingviews|/commentary/|/editorial|/the-lede|/ideas/')
MAGS = {'economist.com', 'theatlantic.com', 'newyorker.com', 'nymag.com', 'thecut.com', 'vox.com', 'vanityfair.com', 'wired.com', 'slate.com',
        'newrepublic.com', 'motherjones.com', 'thenation.com', 'prospect.org', 'talkingpointsmemo.com', 'thebulwark.com', 'nationalreview.com',
        'spectator.com', 'reason.com', 'thefp.com', 'thedispatch.com', 'foreignpolicy.com', 'scientificamerican.com', 'theconversation.com',
        'dailykos.com', 'huffpost.com', 'thedailybeast.com', 'redstate.com', 'hotair.com'}
COV = OrderedDict([('three', (INK, 'News pages of the New York Times, the Wall Street Journal and the Financial Times')),
                   ('opinion', (YELLOW, 'Magazines, opinion sections and opinion-led sites')),
                   ('other', ('#b4b2a6', 'Every other outlet'))])
# the lint's patterns: a tooltip must not trip them (keep in step with lint_figures.py)
LINT = re.compile(r'\b(?:EV|OP|CL|BN|TI|AC|RU|ST|AP|MA|MT)\d{2,3}\b|\b(?:HM|SP|RD|TL|TCS|TCP)\d{2,5}\b|\bT\d{3,4}\b|[\w/-]+\.(?:csv|json|jsonl|py|tsv|html|pdf)\b|research/|scripts/|/(?:mnt|home)/')


# The page asks for Arial; on this machine that is Liberation Sans, so its metrics give the browser's widths.
_FONT = {}


def tw(text, size, bold=False):
    if bold not in _FONT:
        _FONT[bold] = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-' + ('Bold' if bold else 'Regular') + '.ttf', 100)
    return _FONT[bold].getlength(text) * size / 100


def wrap_lines(words, width):
    """Lines a browser needs for `words` [(word, size, bold)] in `width` px, breaking at spaces only."""
    n, cur = 1, 0.0
    for w, size, bold in words:
        ww, sp = tw(w, size, bold), tw(' ', size, bold)
        if cur and cur + sp + ww > width:
            n += 1; cur = ww
        else:
            cur += (sp if cur else 0) + ww
    return n


def text_lines(text, size, width, bold=False):
    return wrap_lines([(w, size, bold) for w in text.split()], width)


def cov_class(domain, url):
    if 'world-in-brief' in url:
        return 'other'
    if OPN.search(url) or domain in MAGS:
        return 'opinion'
    return 'three' if domain in THREE else 'other'


def box(x, y, w, h, inner, style='', fit=True, attrs=''):
    return (f'<div {"data-fit " if fit else ""}{attrs} style="position:absolute;left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px;height:{h:.1f}px;'
            f'overflow:hidden;{style}">{inner}</div>')


PARTIAL = False          # set by generate.py for trial renders made before both FEC pulls are finished
# With more than one panel: True lets a panel break fall between two rows joined by an arc (a tie between two actors who both
# have rows); the arc is then drawn at each end to a small dashed box naming the row at the other end. False keeps every such
# pair of rows in one panel, at the cost of less equal panels.
SPLIT_ARCS = True
GUTTER = 100             # between two panels


def pack(items, lo, hi):
    """Centres for the boxes of one column. items: [(wanted centre, height, least gap to the box above)], top to bottom.
    Each box goes as near its wanted centre as the others allow (boxes that would touch move as one block, by least squares),
    inside lo..hi."""
    def span(i, j):
        return sum(items[k][1] for k in range(i, j + 1)) + sum(items[k][2] for k in range(i + 1, j + 1))

    def top(i, j):
        off = 0.0; s = 0.0
        for k in range(i, j + 1):
            if k > i:
                off += items[k - 1][1] + items[k][2]
            s += items[k][0] - items[k][1] / 2 - off
        return min(max(s / (j - i + 1), lo), hi - span(i, j))

    blocks = []                    # [first, last, top]
    for i in range(len(items)):
        blocks.append([i, i, top(i, i)])
        while len(blocks) > 1 and blocks[-2][2] + span(blocks[-2][0], blocks[-2][1]) + items[blocks[-1][0]][2] > blocks[-1][2]:
            b = blocks.pop(); blocks[-1][1] = b[1]; blocks[-1][2] = top(blocks[-1][0], b[1])
    out = []
    for i, j, y in blocks:
        assert y >= lo - 0.01, ('a column of the network is too full for its panel', lo, hi, [round(c) for c, _, _ in items])
        for k in range(i, j + 1):
            out.append(y + items[k][1] / 2); y += items[k][1] + (items[k + 1][2] if k < j else 0)
    return out


def curve(p0, c1, c2, p3, n=40):
    """Points along the curve the figure draws from p0 to p3 with the control points c1 and c2."""
    out = []
    for i in range(1, n):
        t = i / n; a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        out.append((a * p0[0] + b * c1[0] + c * c2[0] + d * p3[0], a * p0[1] + b * c1[1] + c * c2[1] + d * p3[1]))
    return out


def hidden(points, boxes):
    """How many of the points lie behind one of the boxes (x, top, width, height), or within 12 px of one."""
    return sum(any(x0 - 12 <= x <= x0 + w + 12 and y0 - 12 <= y <= y0 + h + 12 for x0, y0, w, h in boxes) for x, y in points)


def route(p0, p3, boxes, f=0.5, dips=True):
    """(how much of it lies behind the boxes, c1, c2) for a line from a box's right edge at p0 into a row at p3. The plain line
    has its control points at the fraction f of the way across, level with each end (c1 and c2 are then None). Where a box
    hides part of a line that runs nearly level, a line that passes just under or just over a box is taken instead if less
    of it is hidden (a steep line keeps its plain shape: bent round a box it would hug the rows' edge)."""
    mx = p0[0] + (p3[0] - p0[0]) * f
    best = (hidden(curve(p0, (mx, p0[1]), (mx, p3[1]), p3), boxes), None, None)
    for x0, y0, w, h in (boxes if best[0] and dips and abs(p3[1] - p0[1]) <= 220 else ()):
        for dip in (y0 + h + 26, y0 - 26):
            if min(p0[1], p3[1]) - 160 <= dip <= max(p0[1], p3[1]) + 160:
                c1, c2 = (p0[0] + 110, dip), (p3[0] - 110, dip)
                n = hidden(curve(p0, c1, c2, p3), boxes) + 0.5
                if n < best[0]:
                    best = (n, c1, c2)
    return best


def fig_web(KICKER, DRAFT, panels=2, stem='nv8-fifteen-days-mapped'):      # two slices since Nov 15, 2026 (three from Nov 14; panels=3 still draws those)
    assert isinstance(panels, int) and panels >= 1, panels
    # ------------------------------------------------------------------ data
    actors = OrderedDict((a[0], {'key': a[0], 'group': a[1], 'name': a[2], 'tag': a[3], 'fec': a[4]}) for a in rows_map.ACTORS)
    by_name = {a['name']: a for a in actors.values()}
    acts = [a for a in rows_map.acts() if not a['withdrawn']]
    mrows = [r for r in rows_map.rows() if not r.get('withdrawn')]
    people = rows_people.rows()
    ties = [r for r in people if r['row_id'].startswith('TI')] + [r for r in mrows if r['row_id'].startswith('MT') and not r.get('arc') and r['kind'] != 'context']
    # third version: the announcement's own words for the ads ("highlighting the strong records"); the audited row and its source are unchanged
    ties = [dict(r, label=r['label'].replace('ads naming him announced', 'ads praising his record announced')) if r['kind'] == 'ad' else r for r in ties]
    context = [r for r in mrows if r['row_id'].startswith('MT') and r['kind'] == 'context']
    # third version: the member ties built from the FEC lines and the evidence packs (rows_ties). draw=line: a line and words;
    # draw=words: words only (Nvidia's side of the same record, second-hand ties); draw=held: already a tie above (AnthroPAC)
    key2name = {a['key']: a['name'] for a in actors.values()}
    ty = {(r['member'], r['type'], r['side']): r['row_id'] for r in rows_ties.rows() if r['row_id'].startswith('TY')}
    mties = rows_ties.ties(); gift_rate = rows_ties.rates(); worded = []; ty_used = []
    assert all(gift_rate[s]['basis'].startswith('FEC lines') for s in ('anthropic', 'nvidia')) or PARTIAL, 'both companies\' employee gifts must come from the same FEC pull'
    pac_drawn = {r['b'] for r in ties if r['a'] == 'AnthroPAC'}
    for t in mties:
        rid = ty[(t['member'], t['type'], t['side'])]
        assert t['draw'] != 'held' or key2name[t['member']] in pac_drawn or PARTIAL, ('a PAC line is held back as drawn above, and no AnthroPAC tie is drawn for', t['member'])
        if t['draw'] == 'line' and t['node']:
            ties.append({'row_id': rid, 'a': t['node'], 'b': key2name[t['member']], 'kind': t['kind'], 'label': t['words'], 'words': t['words'], 'src': t['src'], 'q': t['q']}); ty_used.append(rid)
        elif t['draw'] == 'words':
            worded.append((key2name[t['member']], t['words'])); ty_used.append(rid)
    undated_acts = [t for t in acts if not t['date']]
    acts = [t for t in acts if t['date']]
    n_acts = len(acts); day_chip = {}
    for t in acts:                          # two acts of one actor on one day share a chip; each keeps its own row and sources
        k = (t['actor'], t['date'])
        day_chip[k] = dict(day_chip[k], what=day_chip[k]['what'].rstrip('.') + '. ' + t['what'], reported=day_chip[k]['reported'] and t['reported'],
                           src=list(day_chip[k]['src']) + list(t['src']), q=list(day_chip[k]['q']) + list(t['q'])) if k in day_chip else t
    acts = list(day_chip.values())
    arcs = [r for r in mrows if r.get('arc')]
    pac = {r['recipient']: r for r in csv.DictReader(open(R / 'anthropac_by_recipient.csv'))}
    party = Counter(r['party'] for r in csv.DictReader(open(R / 'anthropac_party.csv')))
    n_cand = sum(party.values())
    assert n_cand == 81 and party['D'] == 38 and party['R'] == 43, party
    members = [a for a in actors.values() if a['fec'] is not None]
    # recipients in the PAC's filings that carry a drawn member's surname and are someone else's committee (read on Nov 15, 2026: the senator from
    # Florida's committee, and a representative whose given name is Scott)
    OTHERS_OF_THE_NAME = {'Sen. Tim Scott': ('RICK SCOTT FOR FLORIDA', 'SCOTT FRANKLIN FOR CONGRESS')}
    paid = [a for a in members if a['fec']]
    # negative with a control: a member drawn without PAC money must be absent from the filings by surname, a paid one present
    for a in members:
        sur = a['name'].split()[-1].upper()
        found = [k for k in pac if sur in k.replace(',', ' ').split() and k not in OTHERS_OF_THE_NAME.get(a['name'], ())]
        assert bool(found) == bool(a['fec']), (a['name'], found)
        assert not a['fec'] or a['fec'] in pac, a['fec']
    assert paid and len(paid) < len(members)
    # pages naming each member: the rule that decides who is drawn, checked here
    n_pages, hit, _ = member_mentions.count()
    named = {a['key']: len(hit[a['name'].split()[-1]]) for a in members}
    assert all(v >= 3 for v in named.values()), {k: v for k, v in named.items() if v < 3}

    # ties worded in each actor's name cell
    lines = defaultdict(list)     # name -> [(kind, text)]
    for t in ties:
        if t['b'] in by_name:
            k = KMAP[t['kind']]
            if t.get('words'):
                txt = t['words']
            elif t['a'] == 'AnthroPAC':
                txt = f'AnthroPAC: {t["label"]}, 2026'
            elif t['a'] == 'Anthropic':
                txt = t['label'][0].upper() + t['label'][1:]
            else:
                txt = f'{t["a"]}: {t["label"]}'
            lines[t['b']].append((k, txt))
    for t in arcs:
        lines[t['at']].append((KMAP[t['kind']], t['label'][0].upper() + t['label'][1:]))
    for t in context:                       # a third party's statement: worded in the row, no line drawn
        lines[t['b']].append(('none', t['label'][0].upper() + t['label'][1:]))
    for nm, words in worded:
        lines[nm].append(('none', words))
    for t in undated_acts:                  # an act with no day cannot sit on the calendar
        lines[actors[t['actor']]['name']].append(('none', t['what']))
    for a in members:
        if not a['fec']:
            lines[a['name']].append(('none', 'No AnthroPAC contribution on file'))
        lines[a['name']].append(('count', f'Named in {named[a["key"]]} of the {n_pages:,} articles counted'))
    for a in actors.values():
        if a['group'] == 'papers':
            lines[a['name']].append(('none', 'Sources not public. Its reporters\' names, where a saved page carries them, were looked up in the fellowship and staff records held: no record. Nothing else about them was examined'))

    # coverage
    cov = defaultdict(list); undated = 0; sites = set(); sites_dated = set(); n_story = 0; n_scope = Counter()
    read_rows = list(csv.DictReader(open(R / 'coverage_scope_read.tsv', newline='', encoding='utf-8'), delimiter='\t'))
    n_read = sum(r['finding'] == 'on the story' for r in read_rows); n_unsettled = sum(r['finding'] == 'not settled' for r in read_rows)
    for r in csv.DictReader(open(R / 'harvest.tsv'), delimiter='\t'):
        n_scope[story_scope.scope(r['url'], r['anchor_text']) or 'other'] += 1
        if story_scope.scope(r['url'], r['anchor_text']) != 'story':
            continue
        n_story += 1; sites.add(r['domain'])
        if r['first_listed'] in DAYS:
            sites_dated.add(r['domain'])
            cov[r['first_listed']].append((cov_class(r['domain'], r['url']), r['domain'], r['anchor_text']))
        else:
            undated += 1
    n_dated = sum(len(v) for v in cov.values())
    n_quiet = {0: 'none', 1: 'one', 2: 'two', 3: 'three'}.get(sum(len(cov[d]) for d in DAYS[1:7]), str(sum(len(cov[d]) for d in DAYS[1:7])))
    per_row = int((DAY_W - 12) // PITCH)
    max_rows = max(math.ceil(len(v) / per_row) for v in cov.values())
    COV_H = max_rows * PITCH + 34
    dots_p = panels - 1              # the panel whose calendar carries the dots: the last one, top right of the page
    CH = [COV_H if p == dots_p else 10.0 for p in range(panels)]     # per panel: the height above its day axis
    # in each panel the day labels start 6 below that height and the first group header 84 below it

    # ------------------------------------------------------------------ rows: plan the chips, then size each row to its text
    by_actor = defaultdict(list)
    for t in acts:
        by_actor[t['actor']].append(t)
    CH_FONT, CH_LH, CH_ACROSS = 12.8, 14.6, 19        # chip text size, line height, padding plus borders across
    NAME_IN = W_NAME - 20                             # inner width of a name cell
    chips = {}
    for a in actors.values():
        mine = sorted(by_actor[a['key']], key=lambda t: t['date'])
        taken = [DAYS.index(t['date']) for t in mine]
        assert len(set(taken)) == len(taken), ('two acts on one day', a['key'])
        plan = []
        for t in mine:
            di = DAYS.index(t['date'])
            one = tw(t['what'], CH_FONT) + CH_ACROSS + 4      # the width that holds it on one line
            span = 1
            while span < 3 and span * DAY_W - 8 < one and di + span < 15 and (di + span) not in taken:
                span += 1
            w = max(DAY_W - 8, min(span * DAY_W - 8, one))
            plan.append((di, w, text_lines(t['what'], CH_FONT, w - CH_ACROSS - 3), t))
        chips[a['key']] = plan
    rowh = {}; grp_h = OrderedDict()
    for g in rows_map.GROUPS:
        gkey = g[0]; grp_h[gkey] = HDR_H + GAP
        for a in actors.values():
            if a['group'] != gkey:
                continue
            row_min = ROW_MIN_GROUP.get(gkey, ROW_MIN)
            name_l = wrap_lines([(w, 15.5, True) for w in a['name'].split()] + [(w, 13, False) for w in a['tag'].split()], NAME_IN - 3)
            tie_l = sum(text_lines(t, 12.5, NAME_IN - 17 - 3) for _, t in lines[a['name']])
            cell = 18 + name_l * 19.4 + tie_l * 15.5 + 3
            chip = max([n * CH_LH for _, _, n, _ in chips[a['key']]] or [0]) + 12 + 4
            rowh[a['key']] = max(row_min, math.ceil(cell), math.ceil(chip)); grp_h[gkey] += rowh[a['key']]
    key_of = {a['name']: a['key'] for a in actors.values()}
    grp_of = {a['key']: a['group'] for a in actors.values()}

    # ------------------------------------------------------------------ panels: whole groups, in order, heights as equal as they allow
    gkeys = list(grp_h)

    def shares(cuts):
        b = (0,) + tuple(cuts) + (len(gkeys),)
        return [gkeys[b[p]:b[p + 1]] for p in range(panels)]

    def heights(cuts):
        return [CH[p] + 84 + sum(grp_h[g] for g in gs) for p, gs in enumerate(shares(cuts))]

    def whole(cuts):                 # no arc has its two rows in different panels
        where = {g: p for p, gs in enumerate(shares(cuts)) for g in gs}
        return all(where[grp_of[key_of[t['a']]]] == where[grp_of[key_of[t['b']]]] for t in arcs)

    options = [c for c in itertools.combinations(range(1, len(gkeys)), panels - 1) if SPLIT_ARCS or whole(c)]
    assert options, ('no way to share the groups out over the panels', panels)
    cuts = min(options, key=lambda c: (max(heights(c)), sum(v * v for v in heights(c))))
    gpan = {g: p for p, gs in enumerate(shares(cuts)) for g in gs}
    geo = {}; hdr = {}; pan = {}; Y0S = []; HP = []
    for p in range(panels):
        y = CH[p] + 84; Y0S.append(y)
        for gkey in shares(cuts)[p]:
            hdr[gkey] = y; y += HDR_H
            for a in actors.values():
                if a['group'] != gkey:
                    continue
                geo[a['key']] = (y, rowh[a['key']]); pan[a['key']] = p; y += rowh[a['key']]
            y += GAP
        HP.append(y)
    assert [round(v, 3) for v in HP] == [round(v, 3) for v in heights(cuts)]
    HT = max(HP)
    yc = {k: t + h / 2 for k, (t, h) in geo.items()}

    # ------------------------------------------------------------------ left nodes: x, centre y, w, h, subtitle
    # The centres written here are the one-sheet layout's, placed by hand; with more than one panel each panel's copy is
    # placed by rule further down, and only the widths, heights and captions of this list are used.
    r0 = Y0S[0]
    grant = {(g[0], g[1]): g[2] for g in rows_map.GRANTS + rows_map.GRANTS_V3}
    ra = gift_rate['anthropic']; n_emp = sum(1 for t in mties if t['type'] == 'employee_gifts' and t['side'] == 'anthropic' and t['usd'])
    n_ari = sum(1 for t in mties if t['type'] == 'ari_pac')
    OP = 'Open Philanthropy'
    NODES = OrderedDict([
        ('Richard Fontaine', (X_MID, r0 + 50, W_MID, 0, 'trustee of the trust that will elect most of Anthropic\'s board; chief executive of CNAS')),
        ('Holden Karnofsky', (X_MID, r0 + 152, W_MID, 0, 'joined Anthropic\'s staff, Jan 2025; led Open Philanthropy until 2023')),
        (OP, (X_MID, r0 + 250, W_MID, 0, 'funder, renamed Coefficient Giving in 2025; $107.75M to CSET since 2019')),
        ('Jack Clark', (X_MID, r0 + 348, W_MID, 0, 'Anthropic co-founder; listed in CSET rosters, Jan 2020 to Jan 2022; gave AnthroPAC $5,000, Jul 31, 2026')),
        ('Tarun Chhabra', (X_MID, r0 + 458, W_MID, 0, 'Anthropic head of national security policy; on the NSC, 2021–25, as technology coordinator; listed in CSET rosters, 2019–21')),
        ('AnthroPAC', (X_MID, (yc['coons'] + yc['huizenga']) / 2, W_MID, 0,
                       f'Anthropic\'s connected PAC, registered Apr 2026; paid {n_cand} candidates ({party["D"]} D, {party["R"]} R), Jun 29 to Sep 30')),
        ('Public First Action', (X_MID, (yc['mast'] + yc['moolenaar']) / 2 + 60, W_MID, 0,
                                 'received $40 million from Anthropic, Feb and Jul 2026, for policy and education work, Anthropic says; announced a $15M ad project naming Republicans, Jul 2026')),
        ('CNAS', (X_INST, r0 + 44, W_INST, 0, 'think tank; ' + grant[(OP, 'CNAS')].replace(' in awards', ' from Open Philanthropy'))),
        ('Tarbell Center for AI Journalism', (X_INST, (yc['kubinec'] + yc['perlo']) / 2, W_INST, 0, grant[(OP, rows_map.TARBELL)].replace(' in awards', ' from Open Philanthropy'))),
        ('CSET at Georgetown', (X_INST, (yc['bresnick'] + yc['fedasiuk']) / 2, W_INST, 0, 'research centre')),
        ('NSC technology office', (X_INST, yc['mcguire'], W_INST, 0, 'National Security Council')),
        (rows_map.IAPS, (X_INST, yc['grunewald'], W_INST, 0, grant[(OP, rows_map.IAPS)].replace(' in awards', ''))),
        (rows_map.IFP, (X_INST, yc['stapp'], W_INST, 0, grant[(OP, rows_map.IFP)].replace(' in awards', ''))),
        (rows_map.EMPLOYEES, (X_MID, (yc['warren'] + yc['cramer']) / 2, W_MID, 0,
                              f'{ra["donors"]} people who gave Anthropic as employer; gifts to {ra["members_with_a_gift"]} of the 535 sitting members since Jan 2025, {money(float(ra["usd"]))} in all')),
        (rows_map.HORIZON, (X_INST, (yc['banks'] + yc['blumenthal']) / 2, W_INST, 0, 'places fellows in congressional offices and committees')),
        (rows_map.ARI, (X_INST, (yc['crawford'] + yc['meeks']) / 2, W_INST, 0, 'advocacy group with a PAC; ' + grant[(OP, rows_map.ARI)].replace(' in awards', ' from Open Philanthropy'))),
    ])
    for n, (x, c, w, _, sub) in list(NODES.items()):        # height from the text it must hold
        NODES[n] = (x, c, w, math.ceil(15 + 18.6 * text_lines(n, 15.5, w - 23 - 3, bold=True) + 2 + 15 * text_lines(sub, 12.5, w - 23 - 3) + 3), sub)
    y_root = (NODES['Richard Fontaine'][1] + NODES['Public First Action'][1]) / 2
    NODES['Anthropic'] = (X_ROOT, y_root, W_ROOT, 124, 'AI company')
    drawn = {t['a'] for t in ties} | {t['b'] for t in ties}
    assert all(n in drawn for n in NODES), [n for n in NODES if n not in drawn]
    assert all(n in NODES or n in by_name for n in drawn), [n for n in drawn if n not in NODES and n not in by_name]
    # ports on each row's name cell, one per incoming line or arc
    incoming = defaultdict(list)
    for t in ties:
        if t['b'] in by_name:
            incoming[key_of[t['b']]].append(('tie', t))
    for t in arcs:
        incoming[key_of[t['a']]].append(('arc', t)); incoming[key_of[t['b']]].append(('arc', t))

    def port(key, item):
        ks = incoming[key]; i = [id(x[1]) for x in ks].index(id(item)); n = len(ks)
        return (X_NAME, yc[key] + (i - (n - 1) / 2) * 10)

    # everything downstream of a node, so hovering a row lights its whole chain
    feeds = defaultdict(set)
    for t in ties:
        if t['b'] in by_name:
            feeds[t['a']].add(key_of[t['b']])
    changed = True
    while changed:
        changed = False
        for t in ties:
            if t['b'] in NODES and feeds[t['b']] - feeds[t['a']]:
                feeds[t['a']] |= feeds[t['b']]; changed = True

    # ------------------------------------------------------------------ each panel's copy of the network
    # A panel holds the boxes with a line into its rows, directly or through other boxes. A box with no line into any row
    # (it only hangs off other boxes) is drawn once, in the first panel, where the one-sheet layout has it.
    CAT = NODES; cat_col = {n: (0 if n == 'Anthropic' else (1 if CAT[n][0] == X_MID else 2)) for n in CAT}
    rows_of = [{k for k in geo if pan[k] == p} for p in range(panels)]
    IN = []; TP = []
    for p in range(panels):
        names = {n for n in CAT if feeds[n] & rows_of[p]} | ({n for n in CAT if not feeds[n]} if p == 0 else set())
        changed = True
        while changed:               # and whatever feeds those boxes
            changed = False
            for t in ties:
                if t['b'] in names and t['b'] not in by_name and t['a'] not in names:
                    names.add(t['a']); changed = True
        IN.append(names)
        TP.append([t for t in ties if (key_of[t['b']] in rows_of[p] if t['b'] in by_name else t['b'] in names)])
        assert all(t['a'] in names for t in TP[p]), [t['row_id'] for t in TP[p] if t['a'] not in names]
    assert all(any(n in s for s in IN) for n in CAT) and all(sum(t in tp for tp in TP) >= 1 for t in ties)
    assert all(sum(t in tp for tp in TP) == 1 for t in ties if t['b'] in by_name), 'a line into a row is drawn once'
    # an arc whose two rows fell into different panels: at each end, a small box naming the row at the other end
    SI = [[] for _ in range(panels)]
    for t in arcs:
        ka, kb = key_of[t['a']], key_of[t['b']]
        if pan[ka] != pan[kb]:
            for k, other in ((ka, t['b']), (kb, t['a'])):
                w = min(W_INST, math.ceil(tw(other, 15.5, True)) + 28)
                SI[pan[k]].append({'row': k, 'name': other, 't': t, 'w': w, 'x': X_NAME - 206 - w, 'h': math.ceil(13 + 19.4 * text_lines(other, 15.5, w - 23 - 3, bold=True) + 2)})
    assert panels > 1 or not any(SI)
    # a panel with no network keeps no room for one: it starts a little left of its names, where its arcs and the note fit
    X_LO = [0 if (IN[p] or panels == 1) else min([X_NAME - 416] + [s['x'] - 20 for s in SI[p]]) for p in range(panels)]
    OX = []; x = 0
    for p in range(panels):
        OX.append(x - X_LO[p]); x += W - X_LO[p] + GUTTER
    WT = x - GUTTER                  # the plot's width; each panel is drawn in its own coordinates and moved right by OX[p]

    def place(p):
        """One panel's boxes, placed by rule: an institution beside the rows it has lines to; a person or vehicle beside the
        institutions and rows it has lines to (one whose only line runs down its own column sits just above the box that
        line reaches); the company halfway down its column. A line from a box into a row is drawn over the columns between
        them and under their boxes, so a person, a vehicle and the company are each moved, as little as will do, to where
        the least of their lines into rows lies behind a box. Boxes of a column that would touch are then moved apart."""
        names = IN[p]; tp = TP[p]; lo, hi = Y0S[p] + 8, HP[p] - GAP - 6; c = {}; solid = []

        def behind(n, cy, step, f):  # of n's lines into rows, the part behind the boxes placed so far, were n centred at cy
            out = sorted((t for t in tp if t['a'] == n and (t['b'] in by_name or cat_col[t['b']] != cat_col[n])),
                         key=lambda t: yc[key_of[t['b']]] if t['b'] in by_name else c[t['b']])        # as the drawing spreads them
            k = len(out); step = min(step, (CAT[n][3] - 16) / (k - 1)) if k > 1 else 0
            return sum(route((CAT[n][0] + CAT[n][2], cy + (i - (k - 1) / 2) * step), port(key_of[t['b']], t), solid, f, dips=n != 'Anthropic')[0]
                       for i, t in enumerate(out) if t['b'] in by_name)

        for col in (2, 1):
            mine = [n for n in CAT if n in names and cat_col[n] == col]
            want = {}; above = {}
            for n in mine:
                ys = [yc[key_of[t['b']]] if t['b'] in by_name else c[t['b']] for t in tp if t['a'] == n and (t['b'] in by_name or cat_col[t['b']] != col)]
                if ys:
                    want[n] = sum(ys) / len(ys)
                    if col == 1:
                        want[n] += min(range(-400, 401, 20), key=lambda d: (behind(n, want[n] + d, 12, 0.5) + 0.005 * abs(d), abs(d), d))
            for n in mine:
                down = [t['b'] for t in tp if t['a'] == n and t['b'] in want]
                if n not in want and down:
                    above[n] = down[0]
            for n in mine:
                if n not in want and n not in above:      # no line to place it by: the top of its column
                    want[n] = lo + CAT[n][3] / 2
            items = [(want[n], 1, i, n, CAT[n][3]) for i, n in enumerate(mine) if n in want]
            items += [(want[above[n]], 0, i, n, CAT[n][3]) for i, n in enumerate(mine) if n in above]
            if col == 2:
                items += [(yc[s['row']], 1, 100 + i, s, s['h']) for i, s in enumerate(SI[p])]
            items.sort(key=lambda it: it[:3])
            boxes = []
            for j, (wc, kind, _, n, hh) in enumerate(items):
                if kind == 0:                             # just above the box its line reaches, with room for the line
                    assert items[j + 1][3] == above[n], ('two boxes want the place above', above[n])
                    boxes.append((wc - CAT[above[n]][3] / 2 - 29 - hh / 2, hh, 14))
                else:
                    boxes.append((wc, hh, 29 if j and items[j - 1][1] == 0 else 14))
            for (_, _, _, n, hh), cy in zip(items, pack(boxes, lo, hi)):
                if isinstance(n, dict):
                    n['c'] = cy; solid.append((n['x'], cy - hh / 2, n['w'], hh))
                else:
                    c[n] = cy; solid.append((CAT[n][0], cy - hh / 2, CAT[n][2], hh))
        if 'Anthropic' in names:
            ms = [c[t['b']] for t in tp if t['a'] == 'Anthropic' and t['b'] in c]; mid = (min(ms) + max(ms)) / 2; half = CAT['Anthropic'][3] / 2
            c['Anthropic'] = min(range(math.ceil(lo + half), int(hi - half) + 1, 10), key=lambda y: (behind('Anthropic', y, 14, 0.62) + 0.004 * abs(y - mid), abs(y - mid)))
        SOLID[p] = [b for b in solid if b[0] >= X_INST - 200]          # the institutions' boxes and the dashed ones
        return OrderedDict((n, (CAT[n][0], c[n], CAT[n][2], CAT[n][3], CAT[n][4])) for n in CAT if n in names)

    SOLID = {}
    PN = [CAT] if panels == 1 else [place(p) for p in range(panels)]

    def right(n, dy=0):
        x, c, w, h, _ = NODES[n]; return (x + w, c + dy)

    def left(n, dy=0):
        x, c, w, h, _ = NODES[n]; return (x, c + dy)

    panes = []
    for p in range(panels):
        # this panel's share: its boxes, the lines among them and into its rows, its top and bottom
        NODES = PN[p]; tiesp = TP[p]; Y0 = Y0S[p]; Y_AX = CH[p] + 6; H = HP[p]
        # no two boxes in one column may touch
        for X in (X_MID, X_INST):
            colv = sorted((c - h / 2, c + h / 2, n) for n, (x, c, w, h, _) in NODES.items() if x == X)
            colv += sorted((s['c'] - s['h'] / 2, s['c'] + s['h'] / 2, s['name']) for s in SI[p] if X == X_INST)
            for (t0, b0, n0), (t1, b1, n1) in zip(sorted(colv), sorted(colv)[1:]):
                assert t1 - b0 >= 4, ('boxes overlap', n0, n1, round(b0), round(t1))

        svg = []
        # ------------------------------------------------------------------ SVG: grid, weekend bands, coverage dots
        for i, d in enumerate(DAYS):
            x = X_T0 + i * DAY_W
            wd = datetime.date.fromisoformat(d).weekday()
            if wd >= 5:
                svg.append(f'<rect x="{x:.1f}" y="{Y0}" width="{DAY_W:.1f}" height="{H - Y0 - GAP:.1f}" fill="#f0ece2"/>')
            svg.append(f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{H - GAP:.1f}" stroke="{GRID}" stroke-width="1"/>')
        svg.append(f'<line x1="{W:.1f}" y1="{Y0}" x2="{W:.1f}" y2="{H - GAP:.1f}" stroke="{GRID}" stroke-width="1"/>')
        svg.append(f'<line x1="{X_T0}" y1="{CH[p]}" x2="{W}" y2="{CH[p]}" stroke="{AXIS}" stroke-width="1.5"/>')
        order = list(COV)
        for i, d in (enumerate(DAYS) if p == dots_p else ()):
            items = sorted(cov[d], key=lambda t: (order.index(t[0]), t[1]))
            x0 = X_T0 + i * DAY_W + 6 + PITCH / 2
            for j, (c, dom, head) in enumerate(items):
                cx = x0 + (j % per_row) * PITCH; cy = COV_H - 4 - (j // per_row) * PITCH
                tip = LINT.sub('…', f'{dom} · {head}')
                svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{DOT_R}" fill="{COV[c][0]}"><title>{esc(tip)}</title></circle>')
            if items:
                top = COV_H - 4 - math.ceil(len(items) / per_row) * PITCH
                svg.append(f'<text x="{X_T0 + (i + 0.5) * DAY_W:.1f}" y="{top - 5:.1f}" font-size="15" font-weight="bold" text-anchor="middle" fill="{INK}">{len(items):,}</text>')
        # midterms marker, through the rows
        xm = X_T0 + (DAYS.index('2026-11-03') + 0.5) * DAY_W
        svg.append(f'<line x1="{xm:.1f}" y1="{Y0}" x2="{xm:.1f}" y2="{H - GAP:.1f}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="3 5" opacity="0.55"/>')

        # ------------------------------------------------------------------ SVG: ties
        def path(p0, p3, kind, key='', c1=None, c2=None, width=3.0, f=0.5):
            col, dash, _ = KIND[kind]
            mx = p0[0] + (p3[0] - p0[0]) * f
            c1 = c1 or (mx, p0[1]); c2 = c2 or (mx, p3[1])
            d = f' stroke-dasharray="{dash}"' if dash else ''
            cap = ' stroke-linecap="round"' if kind == 'meet' else ''
            return (f'<path class="e" data-a="{key}" d="M{p0[0]:.1f},{p0[1]:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}" '
                    f'fill="none" stroke="{col}" stroke-width="{width}" opacity="0.9"{d}{cap}/>')

        def keys(n):                 # the rows of this panel that a box leads to
            return ' '.join(sorted(feeds[n] & rows_of[p]))

        def colof(n):
            return 0 if n == 'Anthropic' else (1 if NODES[n][0] == X_MID else 2)

        def target_y(t):
            return yc[key_of[t['b']]] if t['b'] in by_name else NODES[t['b']][1]

        side = [t for t in tiesp if t['b'] in NODES and colof(t['a']) == colof(t['b'])]          # both ends in one column
        outs, ins = defaultdict(list), defaultdict(list)
        for t in tiesp:
            if t in side:
                continue
            outs[t['a']].append(t)
            if t['b'] in NODES:
                ins[t['b']].append(t)
        for n in outs:
            outs[n].sort(key=target_y)
        for n in ins:
            ins[n].sort(key=lambda t: NODES[t['a']][1])

        def spread(lst, t, h, step):
            n = len(lst); i = [id(x) for x in lst].index(id(t))
            step = min(step, (h - 16) / (n - 1)) if n > 1 else 0
            return (i - (n - 1) / 2) * step

        for t in tiesp:
            k = KMAP[t['kind']]; a_, b_ = t['a'], t['b']
            key = key_of[b_] if b_ in by_name else keys(b_)
            if t in side:
                xa, ca, wa, ha, _ = NODES[a_]; xb, cb, wb, hb, _ = NODES[b_]
                lo, hi = (a_, b_) if ca < cb else (b_, a_)
                gap0 = NODES[lo][1] + NODES[lo][3] / 2; gap1 = NODES[hi][1] - NODES[hi][3] / 2
                between = [n for n in NODES if NODES[n][0] == xa and gap0 < NODES[n][1] < gap1]
                if not between:                                   # neighbours: a short line down the column
                    gx = xa + wa / 2; col_, dash, _ = KIND[k]
                    d = f' stroke-dasharray="{dash}"' if dash else ''
                    svg.append(f'<line class="e" data-a="{key}" x1="{gx}" y1="{gap0:.1f}" x2="{gx}" y2="{gap1:.1f}" stroke="{col_}" stroke-width="3.2" opacity="0.9"{d}/>')
                else:                                             # others in between: an arc round the left of the column
                    s = 1 if ca < cb else -1                      # down the column, or up it
                    p0 = left(a_, 12 * s); p3 = left(b_, -20 * s)
                    svg.append(path(p0, p3, k, key, c1=(p0[0] - 56, p0[1] + 40 * s), c2=(p3[0] - 56, p3[1] - 40 * s)))
                continue
            p0 = right(a_, spread(outs[a_], t, NODES[a_][3], 14 if a_ == 'Anthropic' else 12))
            if b_ in by_name:
                p3 = port(key_of[b_], t)
                if a_ == 'Tarun Chhabra' and panels == 1:         # the shared panel: under the boxes between them (a panel's copy is placed so that the plain line is clear)
                    dip = NODES['NSC technology office'][1] + NODES['NSC technology office'][3] / 2 + 26
                    svg.append(path(p0, p3, k, key, c1=(p0[0] + 110, dip), c2=(p3[0] - 110, dip), width=2.6))
                else:
                    c1, c2 = route(p0, p3, SOLID[p])[1:] if panels > 1 and colof(a_) == 1 else (None, None)       # a person's or vehicle's line: round a box in its way
                    svg.append(path(p0, p3, k, key, c1=c1, c2=c2, width=2.2 if k == 'own' else (2.6 if a_ == 'Anthropic' else 3.0), f=0.62 if a_ == 'Anthropic' else 0.5))
            else:
                p3 = left(b_, spread(ins[b_], t, NODES[b_][3], 10))
                svg.append(path(p0, p3, k, key, width=3.4 if a_ == 'Anthropic' else 3.0))
        # arcs between rows, beside the names
        for t in sorted(arcs, key=lambda t: -abs(yc[key_of[t['a']]] - yc[key_of[t['b']]])):
            ka, kb = key_of[t['a']], key_of[t['b']]
            if not pan[ka] == pan[kb] == p:
                continue
            pa, pb = port(ka, t), port(kb, t)
            bulge = min(250, 34 + 0.36 * abs(pa[1] - pb[1]))
            svg.append(path(pa, pb, KMAP[t['kind']], f'{ka} {kb}', c1=(pa[0] - bulge, pa[1]), c2=(pb[0] - bulge, pb[1]), width=2.8))
        for s in SI[p]:              # the near end of an arc whose other row is in another panel
            t = s['t']
            svg.append(path((s['x'] + s['w'], s['c']), port(s['row'], t), KMAP[t['kind']], f'{key_of[t["a"]]} {key_of[t["b"]]}', width=2.8))

        # ------------------------------------------------------------------ HTML boxes
        h = []
        # day axis
        for i, d in enumerate(DAYS):
            dt = datetime.date.fromisoformat(d)
            note = f'<div style="font-size:12.5px;line-height:14px;color:{INK};margin-top:4px">{esc(DAYNOTE[d])}</div>' if d in DAYNOTE else ''
            h.append(box(X_T0 + i * DAY_W + 3, Y_AX, DAY_W - 6, 70, f'<b>{MONTHS[dt.month - 1]} {dt.day}</b> <span style="color:{MUTED};font-size:13px">{WD[dt.weekday()]}</span>{note}',
                         'text-align:center;font-size:17px;line-height:1.1'))
        # coverage title, legend and the quiet-days note, in the empty early columns
        cx0 = X_T0 + 1 * DAY_W + 10
        (h if p == dots_p else []).append(box(cx0, 0, 6 * DAY_W - 20, COV_H - 52,
                     f'<div style="font-size:21px;font-weight:bold;line-height:1.2">{n_dated:,} pieces on the story, by the day first listed</div>'
                     f'<div style="font-size:14.5px;color:{MUTED};line-height:1.35;margin-top:6px">One dot is one piece. Techmeme and Memeorandum pages were saved five times a day; '
                     f'{len(sites_dated):,} sites appear among the dots ({len(sites):,} with the pieces that have no day). The six days after the first report brought {n_quiet} more.</div>'
                     + ''.join(f'<div style="display:flex;align-items:center;gap:9px;font-size:14.5px;margin-top:7px"><i style="width:12px;height:12px;border-radius:50%;background:{c};flex:none"></i>{esc(t)}</div>' for c, t in COV.values())))
        # top-left: the three numbers, the tie legend (with more than one panel they go up beside the title: placed further down)
        n_m = len(members)
        stats = [(f'{n_story:,}', f'pieces on the story listed by two aggregators, from {len(sites):,} sites'),
                 (f'{len(actors)}', f'actors drawn, with {n_acts} dated acts between Oct 29 and Nov 12'),
                 (f'{n_emp} of {n_m}', f'members drawn got a gift from an Anthropic employee; {len(paid)} got one from AnthroPAC')]
        sx = 0; head = []
        for big, small in stats:
            head.append((sx, 0, 372, 112, f'<div style="font-size:54px;font-weight:bold;letter-spacing:-1.5px;line-height:1">{big}</div>'
                                          f'<div style="font-size:15px;color:{MUTED};line-height:1.3;margin-top:6px">{esc(small)}</div>'))
            sx += 396
        leg = f'<div style="font-size:13px;letter-spacing:1.6px;font-weight:bold;color:{MUTED};margin-bottom:6px">LINES AT LEFT: DOCUMENTED TIES</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:5px 26px">'
        for k, (col, dash, label) in KIND.items():
            d = f' stroke-dasharray="{dash}"' if dash else ''
            cap = ' stroke-linecap="round"' if k == 'meet' else ''
            leg += (f'<div style="display:flex;align-items:center;gap:10px;font-size:14.5px"><svg width="46" height="10" style="flex:none"><line x1="1" y1="5" x2="45" y2="5" stroke="{col}" stroke-width="3.2"{d}{cap}/></svg>{esc(label)}</div>')
        leg += '</div>'
        head.append((0, 128, 1150, COV_H + 40 - 128, leg))
        if panels == 1:
            h += [box(*b) for b in head]
        elif p == 0:
            band = head
        # column heads for the network (a panel's copy shows a head only over a column it has boxes in)
        for x, t in [(X_ROOT, 'The company'), (X_MID, 'Its people and vehicles'), (X_INST, 'Institutions'), (X_NAME, 'Who acted')]:
            if panels == 1 or x == X_NAME or any(v[0] == x for v in NODES.values()):
                h.append(box(x, Y0 - 26, 300, 20, t.upper(), f'font-size:13px;letter-spacing:1.6px;font-weight:bold;color:{MUTED}', fit=False))
        # group headers: the group's background sentence (a stakes row, word for word), then what no document shows
        stakes = {r['row_id']: r for r in rows_context.rows() if r['row_id'].startswith('ST')}
        for gkey, gtitle, gap, st, lead in rows_map.GROUPS:
            if gpan[gkey] != p:
                continue
            y = hdr[gkey]
            before = stakes[st]['before'] if st else ''
            if lead:
                before = f'{lead} {before[0].lower()}{before[1:]}'
            bg = f'<div><b style="color:{INK}">Background:</b> {esc(before)}</div>' if before else ''
            h.append(box(X_NAME, y + 3, W - X_NAME, HDR_H - 6,
                         f'<div style="display:flex"><div style="width:{X_T0 - X_NAME - 12}px;flex:none;font-weight:bold;letter-spacing:1.4px;font-size:13.5px">{esc(gtitle.upper())}</div>'
                         f'<div style="font-size:13.5px;color:{MUTED}">{bg}'
                         f'<div><b style="color:{INK}">No document here shows</b> {esc(gap)}</div></div></div>',
                         'background:#e6e2d7;border-radius:5px;padding:4px 12px;white-space:nowrap;line-height:19px'))
        # rows: name cells and chips
        for a in actors.values():
            if pan[a['key']] != p:
                continue
            top, rh = geo[a['key']]
            tag = f' <span style="color:{MUTED};font-weight:normal;font-size:13px">{esc(a["tag"])}</span>' if a['tag'] else ''
            inner = f'<div style="font-size:15.5px;font-weight:bold;line-height:1.25">{esc(a["name"])}{tag}</div>'
            for k, txt in lines[a['name']]:
                if k == 'count':
                    inner += f'<div style="font-size:11.5px;line-height:15.5px;color:{MUTED};padding-left:17px">{esc(txt)}</div>'
                    continue
                if k == 'none':
                    sw = f'<i style="width:9px;height:9px;border:1.5px solid {GRAY};border-radius:2px;flex:none;margin-top:3px"></i>'; colr = MUTED
                else:
                    sw = f'<i style="width:10px;height:10px;background:{KIND[k][0]};border-radius:2px;flex:none;margin-top:3px"></i>'; colr = INK
                inner += f'<div style="display:flex;gap:7px;font-size:12.5px;line-height:15.5px;color:{colr}">{sw}<span>{esc(txt)}</span></div>'
            h.append(box(X_NAME, top + 3, W_NAME, rh - 6, inner, f'background:{CARD};border-radius:7px;padding:6px 10px', attrs=f'data-a="{a["key"]}" class="row"'))
            svg.append(f'<line x1="{X_T0}" y1="{top + rh:.1f}" x2="{W}" y2="{top + rh:.1f}" stroke="{GRID}" stroke-width="1"/>')
            for di, w, _, t in chips[a['key']]:
                h.append(box(X_T0 + di * DAY_W + 4, top + 5, w, rh - 10,
                             f'<div style="display:flex;height:100%;align-items:center"><span style="font-size:{CH_FONT}px;line-height:{CH_LH}px">{esc(t["what"])}</span></div>',
                             f'background:#fffdf8;border:1px solid {LGRAY};border-left:4px {"dashed" if t.get("reported") else "solid"} {INK};border-radius:5px;padding:0 7px', attrs=f'data-a="{a["key"]}" class="chip"'))
        # left nodes
        for name, (x, c, w, nh, sub) in NODES.items():
            if name == 'Anthropic':
                inner = (f'<div style="font-size:26px;font-weight:bold;letter-spacing:-.4px">Anthropic</div>'
                         f'<div style="font-size:13.5px;line-height:1.3;opacity:.82;margin-top:4px">{esc(sub)}; set its IPO price range on Nov 10</div>')
                st = f'background:{INK};color:#fff;border-radius:10px;padding:16px 14px'
            else:
                inner = (f'<div style="font-size:15.5px;font-weight:bold;line-height:1.2">{esc(name)}</div>'
                         f'<div style="font-size:12.5px;line-height:15px;color:{MUTED};margin-top:2px">{esc(sub)}</div>')
                st = f'background:#fffdf8;border:1.5px solid {AXIS};border-radius:8px;padding:6px 10px'
            h.append(box(x, c - nh / 2, w, nh, inner, st))
        for s in SI[p]:              # the row at the far end of an arc that leaves this panel: its name, in a dashed box
            h.append(box(s['x'], s['c'] - s['h'] / 2, s['w'], s['h'], f'<div style="font-size:15.5px;font-weight:bold;line-height:1.25">{esc(s["name"])}</div>',
                         f'background:{CARD};border:1.5px dashed {GRAY};border-radius:7px;padding:5px 10px'))
        panes.append((svg, h))
    # the note: on the one sheet in the empty lower left; with panels, at the top of the last one, left of the dots
    ny = hdr['admin'] if panels == 1 else 0
    nx = X_LO[dots_p]
    assert panels == 1 or (nx + 640 <= X_T0 - 60 and 350 <= Y0S[dots_p] - 34), 'the note does not fit beside the dots'
    note = (f'<div style="font-size:30px;font-weight:bold;letter-spacing:-.6px;line-height:1.12">A tie is a dated record, not a motive.</div>'
            f'<div style="font-size:17px;line-height:1.42;color:{INK};margin-top:12px">No document here shows that any tie prompted a report, a post or a statement. '
            f'Each line ends at a person or a body, never at an act; the acts sit on the calendar at right.</div>'
            f'<div style="font-size:15px;line-height:1.45;color:{MUTED};margin-top:12px">{len(paid)} of the {n_m} members drawn received an AnthroPAC contribution; {n_m - len(paid)} did not, '
            f'and they pressed the matter too. The PAC paid {n_cand} candidates in all, {party["D"]} Democrats and {party["R"]} Republicans. '
            f'Nvidia, AMD and Broadcom are themselves among the seven companies that agreed to buy Anthropic stock. '
            f'Employees\' gifts are their own money: {ra["members_with_a_gift"]} of the 535 sitting members received one from someone who gave Anthropic as employer, {n_emp} of the {n_m} drawn here. '
            f'The same count for Nvidia\'s employees is worded in each member\'s row. '
            f'Ties the source article asserts but no document here supports are not drawn.</div>')
    panes[dots_p][1].append(box(nx, ny, 640, 350, note, f'border-left:6px solid {INK};padding:4px 0 4px 20px'))

    hover = ''.join(f'.plot:has([data-a="{k}"].row:hover) .e:not([data-a~="{k}"]),.plot:has([data-a="{k}"].row:hover) .chip:not([data-a="{k}"]){{opacity:.13}}' for k in actors)
    css = f'.plot{{position:relative;width:{WT}px;height:{HT:.0f}px}}.plot>svg{{position:absolute;left:0;top:0}}.e,.chip{{transition:opacity .12s}}.row{{cursor:default}}' + hover

    foot = ('<b>Reading it:</b> the dots count pieces, not readers; a piece is placed on the first day a saved Techmeme or Memeorandum page lists it '
            f'(pages for 9 am, noon, 4 pm, 8 pm and 11 pm Eastern each day), and {undated} more pieces seen only on undated pages are left out. '
            'A piece counts as on the story when its address or listed headline names Huang, Megaspeed or Alice Huang, tells of the spy affair without naming them, '
            'or names Nvidia with a word of the affair (resign, board, inquiry, chief, successor and the like). '
            f'That rule was applied by script, not by reading each piece, to the {sum(n_scope.values()):,} links on those pages that name Huang, Nvidia, Megaspeed or the spy story. '
            f'The {n_scope["fallout"] + n_scope["other"] + n_read:,} links the rule left out were then read, 150 of them by an independent auditor and the rest by the builder: {n_read} are plainly on the story and are counted with it, and {n_unsettled} could not be settled from their headlines. '
            f'Left out are {n_scope["fallout"]:,} links on the wider fallout (export controls, the Commerce secretary, the share price, Anthropic\'s stock offering) and {n_scope["other"]:,} others; '
            'a counted piece may name Huang for another reason. Every link, its class and each reading is published with the figure\'s tables. '
            'They are sorted into the three kinds by site and by the section named in the page address, not by reading them. '
            'A chip is one dated act, worded from a saved report; it starts on its day, and a long one may run on over empty days to its right. '
            'View counts are those shown when the posts were saved on Nov 12. '
            'An act is placed on the day its source gives or, failing that, the day the source was published: those chips have a dashed left edge, and the act itself may be earlier. Where one chip holds two acts of a day and only one is dated by its report, the edge is solid and the words say which. '
            'Where a chip rests on one outlet\'s account of another\'s report, it says so. Grant figures are awards, not payments traced to a bank. An announced ad is not proof that it ran. '
            'Nvidia\'s board said on Nov 8 it had "no reason to believe" national security or company secrets were compromised, and NBC reported on Nov 12 that Alice Huang\'s "precise role" remained unclear. '
            + esc(ARTICLE_WORDS()) +
            f'Members of Congress drawn are every current member named in three or more of those {n_pages:,} articles for something said or done about the matter in these days, '
            'and one senator (Cotton) whom they name that often for a letter on Megaspeed a year earlier; each one\'s count is in their row. '
            'Six others named that often are not drawn, because the pages name them for other things: a leadership vote, a lost election, an impeachment bid and other inquiries. '
            'The count for every name searched is published with the figure\'s tables. '
            + LOOKUP_WORDS(n_pages) +
            '"No AnthroPAC contribution on file" means none in the PAC\'s filings with the Federal Election Commission for Jun 29 to Sep 30, 2026. '
            f'A line that says no gift from a company\'s employees means that no FEC line for Jan 2025 to {MON(gift_rate["anthropic"]["read_through"])} gives that company as the donor\'s employer to a committee tied to the member; it is not proof that no employee gave. '
            f'Lines dated after {MON(gift_rate["anthropic"]["read_through"])} are not in the FEC records read here: where a committee must file a post-general report (its books close Nov 23), that report is due on Dec 3, 2026; other committees follow their own schedules. '
            + CONDUIT(gift_rate) +
            'A committee is tied to a member when it is the member\'s campaign committee, a leadership PAC the member sponsors, or a joint fundraising committee whose statement of organisation lists that member\'s committee and no other sitting member\'s; '
            'money given to a joint committee is shared with its other participants (a party committee, a PAC), and the FEC lines do not show how much reached the member\'s own campaign. Joint committees of several members are listed with the figure\'s tables and attributed to no one. '
            'An employee\'s gift is counted from an FEC line on which the donor gave the company as employer, to a committee tied to the member; donors are counted, not named, and the two companies are counted by one rule, though not from equally deep records, as the next sentences say. ' + esc(rows_ties.basis_words()) + ' '
            + NEGATIVES(gift_rate, key2name) +
            'A lobbying report names a bill; it does not say which office was visited or what was asked. Fellows, advisers and former staff are as the programme\'s, the group\'s or Congress\'s own pages list them. '
            'A lobbyists\' line names the clients that the lobbying reports held here list for the givers\' firms. The reports give each gift as the lobbyist\'s own money; '
            'they do not show whether a client asked for it. Whether the firm had the client when the gift was made is taken from the firm\'s registration dates, which the published table gives beside each gift. '
            'Why each client is on this map: Open Philanthropy\'s awards on record include $3.4M to Americans for Responsible Innovation (2024–25), $12.5M to the Center for AI Safety (2022–23) and $1.9M to the Future of Life Institute (2015–20), '
            'and its action fund gave IFP Action $2.0M (2022–23). The grants on record to the Center for AI Safety\'s action fund and to Encode AI are from Jaan Tallinn, and the Future of Life Institute gave Encode $250,000 in 2024; no Open Philanthropy award to either is on record, and none of any kind to Fathom. '
            'Nvidia registered its own political committee on Aug 27, 2026; its one report on file, through Sep 30, shows no contribution to any candidate. '
            + LOBBY_WORDS() +
            '<b>What the record does not show:</b> who gave the intelligence assessment to reporters; whether it is correct; any contact about these reports between Anthropic, or anyone tied to it, and the reporters or their sources; '
            'any contact with a member of Congress about these reports or about what the member then said or did (earlier public contacts, such as testimony at a hearing, are drawn at left). '
            'The saved reports state limits of their own: the Times\'s first report says officials "did not believe" Huang knew the woman was gathering information when the president was first briefed, '
            'and that Huang "has not received a defensive briefing"; Nvidia said its customers get "zero information relevant to national security", and the Times reports its spokesman saying that customers do not ask Nvidia to press the U.S. government to change its policies on chip sales to China. '
            'That first report also says it "could not be determined which intelligence agency or agencies" monitored her, and that it is not clear what information she passed along or what it was worth to China. '
            'NBC reports that the president, asked whether he was briefed before he took Huang to China in May, said "I didn\'t hear about it then" and later "They could have been mentioned." '
            '<b>Nvidia\'s side, the same classes of record:</b> its employees\' gifts are drawn beside Anthropic\'s; its political committee is new and has given to no candidate; its lobbyists\' gifts are counted above with Anthropic\'s and the groups\'; '
            'bills named in its lobbying reports are drawn; past posts with a drawn member that its lobbyists declare are drawn (Banks, Kennedy, McCaul), as is the one found for a lobbyist of Anthropic (Thune). '
            'Its support of institutions whose people are drawn is worded in their rows (CSET, CNAS, the Council on Foreign Relations); the donor lists of Brookings and 80,000 Hours do not name it, and a reader from another model family found it on none of the lists that IAPS, the Foundation for American Innovation, the Institute for Progress and the Tarbell Center publish, most of which are partial. '
            'Quoted people with a past post at Nvidia or paid work for it are drawn (Moorhead, Newman, Boloor, Yoo; both companies support Barez\'s research), and business with Nvidia that a saved page states is worded for two public voices (Musk, Delangue). '
            'Looked for and not established: a witness from Nvidia before these members\' committees, advertising aimed at their districts, a seat on their advisory bodies. Those searches have gaps: the ad libraries could not be read, the search of the records held ended with 3,839 hits unread, and the web search left 491 targets unopened. '
            'The map still starts from Anthropic and Open Philanthropy at the left of each slice, so the number of lines says nothing about either company\'s influence. The Times\'s and the FT\'s reports are cited from their own articles, saved by hand; the Journal\'s own site turns away automated readers: its report of Oct 30 is cited from its own page, saved by hand, and from the copy a licensed partner carries (Tiger Brokers), its report of Nov 11 from a partner\'s copy (the Greek paper To Vima). An earlier exclusive that a paper drew from an Anthropic executive is drawn as a tie in that paper\'s row: one is on record, the FT\'s of Sep 2025, known here through another outlet\'s account of it. The papers\' earlier reporting was not searched for others, and exclusives from Nvidia were not looked up. '
            + OWN_CHANNEL_WORDS() +
            f'<b>Source:</b> {n_story:,} links from saved aggregator pages; saved reports, posts and releases; committee filings; rows held in the congress, lineage, toner and evaluators packs. Aggregator pages for Oct 29 to Nov 12 were retrieved on Nov 12 and Nov 14, 2026; other sources were saved Nov 12 to 15, 2026; rows of the packs carry their own earlier dates. {DRAFT}')
    title = 'Fifteen days, mapped: the coverage, who acted, and the documented ties'
    sub = ('Top right, each dot is one piece on the story. Below it, each row is one actor and each chip one dated act. At left, each line is a documented tie '
           'between an actor and a company, a funder or a group: a contribution, a post held, a grant, an official act. ' + {2: 'Both', 3: 'The three', 4: 'The four'}[panels] + ' slices repeat the same companies, funders and people at their left; a dashed box names an actor whose own row is in another slice. '
           'The ties are mapped outward from Anthropic and Open Philanthropy; Nvidia\'s are added where the same kind of record was searched (the note at the foot lists them), and each group\'s heading gives the rule for who is drawn. '
           'The figure sets these records side by side; it does not say one caused another.')
    # also behind drawn words: the midterms note (an events row), two node captions (run-up rows), the header backgrounds (stakes rows)
    caption_rows = [r['row_id'] for r in rows_context.rows() if r['row_id'].startswith('RU') and ('Chip Smuggling' in r['text'] or '$15 million' in r['text'])]
    assert len(caption_rows) == 2, caption_rows
    ids = ([r['row_id'] for r in mrows] + [r['row_id'] for r in people if r['row_id'].startswith('TI')] + ['EV05', 'NT02', 'NT03'] + [r['row_id'] for r in rows_context.rows() if r['row_id'].startswith('NT') and int(r['row_id'][2:]) >= 5] + caption_rows
           + [g[3] for g in rows_map.GROUPS if g[3]] + [r['row_id'] for r in rows_coverage.rows() if r['drawn']] + ty_used + [r['row_id'] for r in rows_ties.rows() if r['row_id'].startswith('TR')])
    if panels == 1:
        svg, h = panes[0]
        body = f'<div class="plot"><svg width="{W}" height="{HT:.0f}" viewBox="0 0 {W} {HT:.0f}">{"".join(svg)}</svg>{"".join(h)}</div>'
        doc = cite(ids) + shell(title, KICKER, sub, body, foot, PAGE, extra_css=css)
        render(stem, doc, PAGE)
        return
    page = WT + 120
    # the three numbers and the tie legend, in the band the title leaves empty at its right. The band's height is the shell's:
    # the kicker's line, then the title and the subtitle with their margins (the subtitle is at most 1900 wide).
    sub_w = min(page - 220, 1900)
    band_h = 19.5 + 12 + 49.2 * text_lines(title, 46, page - 160, bold=True) + 10 + 29.7 * text_lines(sub, 22, sub_w) + 16
    bx = max(sub_w, math.ceil(tw(title, 46, True))) + 80; by = -band_h + (band_h - 16 - 112) / 2
    top = [box(bx + x, by, w, hh, inner) for x, _, w, hh, inner in band[:3]] + [box(bx + 3 * 396 + 60, by + 4, band[3][2], 116, band[3][4])]
    assert bx + 3 * 396 + 60 + band[3][2] <= WT and by >= -band_h, 'the numbers and the legend do not fit beside the title'
    # one drawing layer and one hover scope for the page; each panel's lines and boxes sit in a group moved right by OX[p]
    rules = ''.join(f'<line x1="{OX[p] + X_LO[p] - GUTTER / 2:.1f}" y1="0" x2="{OX[p] + X_LO[p] - GUTTER / 2:.1f}" y2="{HT:.0f}" stroke="{AXIS}" stroke-width="1"/>' for p in range(1, panels))
    body = (f'<div class="plot"><svg width="{WT}" height="{HT:.0f}" viewBox="0 0 {WT} {HT:.0f}">{rules}'
            + ''.join(f'<g transform="translate({OX[p]},0)">{"".join(svg)}</g>' for p, (svg, h) in enumerate(panes)) + '</svg>'
            + ''.join(f'<div class="pan" style="position:absolute;left:{OX[p]}px;top:0">{"".join(h)}</div>' for p, (svg, h) in enumerate(panes))
            + ''.join(top) + '</div>')
    css += f'.footnote{{column-count:{panels};column-gap:{GUTTER}px}}'
    doc = cite(ids) + shell(title, KICKER, sub, body, foot, page, extra_css=css)
    render(stem, doc, page)
