"""Run: python3 -I scripts/nv8_partial_screen.py <output .tsv>      (written after the eleventh reading, Nov 16, 2026; the list it gave was read page by page
by a reader from another model family, lane partial_nv8_a, and the verdicts are in research/nv8_pages_in_part_read.tsv)
Screen every counted page for signs that the saved copy holds only part of the piece (a subscription or sign-in barrier, a preview), to be read.
Signals: (free) the page's own structured data says isAccessibleForFree false; (wall) a barrier phrase in the text that was read; (html) a barrier
phrase or a paywall marker in the saved HTML; (short) the text read is under 2,000 characters. Control: the pages already flagged as held in part."""
import sys, csv, re, json, html
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M
R = ROOT / 'research'; P = R / 'primary'
arts = list(csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t'))
text_of = {pid: t for copies in M.articles().values() for pid, t in copies}
WALL = re.compile(r"subscribe (?:for|to get|to gain) (?:full|unlimited) access|subscribe to (?:continue|read|unlock|keep reading)|subscribe now to (?:read|continue)|(?:continue|keep) reading (?:this article |with |for )|to (?:continue|keep) reading|"
                  r"already a subscriber|this (?:article|story|content|post) is (?:for|exclusive to|available to|reserved for) (?:paid |paying |our )?(?:subscribers|members)|for (?:paid )?subscribers only|subscriber[- ]only|"
                  r"sign in to (?:continue|read)|log ?in (?:or subscribe )?to (?:continue|read)|register (?:for free )?to (?:continue|read)|create a(?: free)? account to (?:continue|read)|"
                  r"unlock (?:this|the full) (?:article|story)|read the (?:full|whole) (?:article|story) (?:with|by|at|on)|to read the (?:full|rest of (?:this|the)) (?:article|story)|want to (?:read more|keep reading)\?|"
                  r"you(?:'|’)ve (?:reached|hit) your (?:free )?(?:article )?limit|free trial|start your (?:free )?trial|this post is for paid|upgrade to (?:paid|read)|get unlimited access|full access to", re.I)
MARK = re.compile(r'"isAccessibleForFree"\s*:\s*"?false"?|class="[^"]*(?:paywall|pay-wall|regwall|subscriber-only|metered|piano-|tp-container|premium-content|gated)[^"]*"|data-(?:paywall|piano)|id="(?:paywall|piano)[^"]*"', re.I)
FREE = re.compile(r'"isAccessibleForFree"\s*:\s*"?false"?', re.I)
out = []
for r in arts:
    if r['counted'] != 'yes': continue
    pid = r['page_id']; t = text_of.get(pid, ''); d = P / pid
    body = ''
    for n in ('body.html',):
        if (d / n).exists(): body = (d / n).read_text(errors='replace')
    vis = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', body, flags=re.S | re.I))) if body else ''
    sig = []
    if FREE.search(body): sig.append('free')
    m = WALL.search(t)
    if m: sig.append('wall')
    mh = WALL.search(vis) if vis else None
    if mh and not m: sig.append('html')
    if MARK.search(body) and 'free' not in sig: sig.append('mark')
    if len(t) < 2000: sig.append('short')
    out.append({'page_id': pid, 'site': r['site'], 'chars': len(t), 'flagged': r['saved_in_part'], 'signals': ' '.join(sig), 'phrase': (m or mh).group(0) if (m or mh) else '',
                'where': (lambda mm, tt: re.sub(r'\s+', ' ', tt[max(0, mm.start() - 90):mm.end() + 60]))(m, t) if m else ((lambda mm, tt: tt[max(0, mm.start() - 90):mm.end() + 60])(mh, vis) if mh else '')})
with open(sys.argv[1], 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
fl = [o for o in out if o['flagged'] == 'yes']; un = [o for o in out if o['flagged'] != 'yes']
print('counted pages', len(out), '| flagged', len(fl), '| not flagged', len(un))
for name, grp in (('flagged (control)', fl), ('not flagged', un)):
    print(name, dict(Counter(o['signals'] or '(none)' for o in grp).most_common(20)))
strong = lambda o: ('free' in o['signals'] or 'wall' in o['signals'] or ('html' in o['signals'] and 'short' in o['signals']) or ('mark' in o['signals'] and 'short' in o['signals']))
print('control: flagged pages the strong rule catches:', sum(strong(o) for o in fl), 'of', len(fl))
print('candidates among the unflagged (strong rule):', sum(strong(o) for o in un), '| of them the page the reading found:', any(o['page_id'] == 'sw-washingtonexaminercom-03' and strong(o) for o in un))
