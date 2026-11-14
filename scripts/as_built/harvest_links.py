"""Harvest every Huang-related article link from the saved aggregator snapshots (Techmeme, Memeorandum).
Run: python3 -I scripts/harvest_links.py  -> research/harvest.tsv (domain, first snapshot, url, anchor text, first listed)
A link counts when its URL or anchor text names Huang, Nvidia, Megaspeed or the spy story. Aggregator-internal
links and social posts are skipped. This is a finding aid: it says what was published, not what it says.
A piece's day (first_listed) is the earliest day of a timed capture of an aggregator's front page that lists it; a
permalink page of one story can grow after its date, so it never dates a piece."""
import csv, glob, re, sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse, parse_qsl
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
KEY = re.compile(r'huang|nvidia|jensen|megaspeed|chinese[- ]spy|spy[- ]', re.I)
# whole domains only: an unanchored 'x\.com' also dropped vox.com (found 2026-11-12)
SKIP = re.compile(r'(^|\.)(techmeme\.com|memeorandum\.com|mediagazer\.com|x\.com|twitter\.com|bsky\.app|threads\.(net|com)|linkedin\.com|youtube\.com|reddit\.com|facebook\.com|instagram\.com|t\.co|news\.ycombinator\.com)$|mastodon')
assert SKIP.search('x.com') and SKIP.search('mobile.x.com') and not SKIP.search('vox.com') and not SKIP.search('netflix.com')
TIMED = re.compile(r'-(\d{2})(\d{2})-h(\d{4})[a-z]?$')      # timed snapshots only; permalink pages can grow later


TRACKING = re.compile(r'^(utm_\w+|fbclid|gclid|ref|ref_src|smid|share|src|source|cmp|ocid|mc_cid|mc_eid)$', re.I)
SCRIPT = re.compile(r'\.(php|asp|aspx|jsp|cgi|do|nhn)$', re.I)


def key(h):
    """What makes two links the same piece: host and path. The query string is dropped, because it mostly carries tracking
    fields and access tokens, except where the path names no piece by itself: the site's root (/?post=123) or a script
    (view.php?key=123). There the query is part of the address. (Until Nov 14, 2026 the query was always dropped, which
    counted six articles of one site, all at view.php, as one piece.)"""
    k = re.sub(r'^https?://(www\.)?', '', h.split('?')[0]).rstrip('/'); path = urlparse(h.split('?')[0]).path
    if '?' in h and (path in ('', '/') or SCRIPT.search(path)):
        q = '&'.join(f'{a}={b}' for a, b in parse_qsl(h.split('?', 1)[1]) if not TRACKING.match(a))
        if q:
            k += '?' + q
    return k


assert key('https://www.a.com/view.php?key=1') != key('https://a.com/view.php?key=2') and key('https://a.com/x/story?utm_source=q&tok=1') == 'a.com/x/story' and key('https://a.com/?post=5&utm_medium=x') == 'a.com?post=5'


def snapshots():
    return [Path(d) for d in sorted(glob.glob(str(R / 'primary' / 'techmeme-*')) + glob.glob(str(R / 'primary' / 'memeorandum-*'))) if (Path(d) / 'body.html').exists()]


def links(d):
    """Every counted link on one saved page: (key, domain, address as kept, anchor text)."""
    soup = BeautifulSoup((d / 'body.html').read_bytes(), 'lxml')
    for a in soup.find_all('a', href=True):
        h = a['href'].split('#')[0]
        if not h.startswith('http'): continue
        dom = urlparse(h).netloc.lower().replace('www.', '')
        if SKIP.search(dom): continue
        t = re.sub(r'\s+', ' ', a.get_text(' ', strip=True))
        if not KEY.search(h + ' ' + t): continue
        h = re.sub(r'^http://', 'https://', h.split('?')[0]) if 'economist.com' in h or 'nytimes.com' in h or 'wsj.com' in h else h
        yield key(h), dom, h, t


def day(name):
    m = TIMED.search(name)
    return f'2026-{m.group(1)}-{m.group(2)}' if m else ''


def harvest():
    seen = {}
    for d in snapshots():
        listed = day(d.name)
        for k, dom, h, t in links(d):
            cur = seen.get(k)
            first = min(x for x in [listed, cur[4] if cur else ''] if x) if (listed or (cur and cur[4])) else ''
            if cur is None or (len(t) > len(cur[3])):
                seen[k] = (dom, cur[1] if cur else d.name, h, t[:220], first)
            else:
                seen[k] = cur[:4] + (first,)
    # a piece keeps the spelling of its address first recorded for it (the row-id register), so a later page that lists
    # it with a tracking field does not change the address the tables and the audit hold
    reg = R / 'coverage_row_ids.csv'
    keep = {key(r['url']): r['url'] for r in csv.DictReader(open(reg, newline=''))} if reg.exists() else {}
    return sorted((v[0], v[1], keep.get(k, v[2]), v[3], v[4]) for k, v in seen.items())


def main(out=None):
    rows = harvest()
    with open(out or (R / 'harvest.tsv'), 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow(['domain', 'first_snapshot', 'url', 'anchor_text', 'first_listed']); w.writerows(rows)
    c = Counter(r[0] for r in rows)
    print('links', len(rows), 'domains', len(c)); print(' '.join(f'{d}:{n}' for d, n in c.most_common()))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
