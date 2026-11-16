"""Run: python3 -I scripts/nv8_collapse_screen.py      (written after the twelfth reading, Nov 16, 2026)
The twelfth reading found a counted live page whose entries were collapsed in the saved copy ("Show more"), which the screen for subscription barriers
(scripts/nv8_partial_screen.py) cannot see. This searches the text read of every counted page for a collapse mark and writes research/nv8_collapse_screen.tsv:
one line per page with a mark and what the mark belongs to, as read by the builder on Nov 16, 2026. A page with a mark and no reading stops the script.
Control: the page the reading found must be among the hits. Limit: a live page that loads further entries only on request, with no mark in the saved
text, is not seen by this search either; the live pages among the counted pages are listed at the end for a reader."""
import sys, csv, re
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M
R = ROOT / 'research'
MARK = re.compile(r'show more|see more|show full|load more|view more|read more|continue reading|expand (?:to|for)|read full (?:post|update)', re.I)
OWN_LINE = re.compile(r'(?im)^\s*(?:show more|see more|read more|view more|load more|continue reading)\s*[›»>+…]*\s*$')
LIVE = re.compile(r'live (?:updates|blog|coverage)|\blive\b.{0,40}\bupdates\b', re.I)
SUMMARY = 'the summary box under the headline'; LINKS = 'a list of links to other articles'
READ = {'man-nyt-1112-09': 'entries of a live page, collapsed in the saved copy: the page is held in part',
        'sw-foreignpolicycom-01': 'a link card to another article, and the comment rules', 'sw-irishtimescom-01': LINKS, 'sw-theregistercom-01': LINKS,
        'sw-euronewscom-01': LINKS, 'sw-euronewscom-02': LINKS, 'sw-euronewscom-05': LINKS, 'sw-euronewscom-06': LINKS,
        'man-0c5b4e4f24c9': 'a photo caption', 'man-e8a4f78b0d7e': 'a photo caption', 'man-109ae199a0e7': 'lists of other videos under a video page'}
READ.update({p: SUMMARY for p in ('man-923fe8754943', 'man-9de9f2a5db75', 'man-bb944902439c', 'man-wsj-1109-09', 'man-wsj-1110-03', 'man-wsj-1112-05', 'man-506b033a9fd4', 'man-05b8d5160f55',
                                  'man-wsj-1109-06', 'man-5dbffa3344fb', 'man-wsj-1109-08', 'man-83733609b719', 'man-wsj-1112-08')})
LIVE_LINKS = "links from a live page's entries to full stories or to other outlets' reports"; SPONSOR = "a sponsor's box inside the article"
READ.update({p: LIVE_LINKS for p in ('huffpost-live', 'sw-financeyahoocom-23', 'sw-financeyahoocom-25', 'sw-financeyahoocom-32', 'yahoo-live-ousted', 'man-ft-1112-05')})
READ.update({p: SPONSOR for p in ('sw-financeyahoocom-07', 'sw-financeyahoocom-17', 'sw-financeyahoocom-20', 'sw-financeyahoocom-24', 'sw-financeyahoocom-26', 'sw-financeyahoocom-28', 'sw-financeyahoocom-29')})
READ.update({'sw-fortunecom-07': "links from a newsletter's items to other outlets' reports", 'sw-inquirercom-53b966e2': LINKS, 'sw-pbsorg-01': LINKS, 'sw-pbsorg-02': LINKS,
             'sw-triviumchinacom-01': 'a list of other posts under the article'})
arts = [r for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t') if r['counted'] == 'yes']
text_of = {pid: t for copies in M.articles().values() for pid, t in copies}
out, live = [], []
for r in arts:
    pid = r['page_id']; t = text_of.get(pid, '')
    own = len(OWN_LINE.findall(t)); every = len(MARK.findall(t))
    if own or every >= 2:
        assert pid in READ, ('a counted page with a collapse mark that no one has read', pid, own, every)
        out.append({'page_id': pid, 'site': r['site'], 'marks_on_a_line_of_their_own': own, 'marks_in_all': every, 'what_the_mark_belongs_to': READ[pid], 'saved_in_part': r['saved_in_part']})
    if LIVE.search(t[:1500]) or '/live/' in r.get('url', '').lower() or 'live-updates' in r.get('url', '').lower(): live.append((pid, r['site'], r['saved_in_part'], len(t)))
assert any(o['page_id'] == 'man-nyt-1112-09' for o in out), 'control: the page the reading found is not among the hits'
assert set(READ) == {o['page_id'] for o in out}, ('a reading for a page that no longer has a mark', sorted(set(READ) - {o['page_id'] for o in out}))
with open(R / 'nv8_collapse_screen.tsv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
print('counted pages', len(arts), '| with a collapse mark', len(out), '| of them collapsed entries of the piece itself', sum('held in part' in o['what_the_mark_belongs_to'] for o in out))
print(dict(Counter(o['what_the_mark_belongs_to'] for o in out)))
print('live pages among the counted pages:', len(live)); [print('   ', x) for x in live]
