"""Run: python3 scripts/nv8_live_pages.py      (written after the thirteenth reading, Nov 16, 2026)
The thirteenth reading found live pages whose saved HTML holds more entries than the text read (the extraction took only the entries the page
showed before its "more updates" control). This looks at EVERY saved page that has a body.html for a live-blog record in the page's own structured
data (schema.org LiveBlogPosting, liveBlogUpdate) and writes research/nv8_live_pages.tsv: for each such page, how many entries the HTML holds, how
many of them the text read holds (the entry's headline, or the opening of its text), whether the HTML shows a control that loads further entries,
and the mark the page carries. Control: the pages the reading named must be found. A live page saved by hand as PDF has no HTML and is not seen here."""
import csv, json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M
R = ROOT / 'research'; P = R / 'primary'
MORE = re.compile(r'more updates|load more|story continues|show more updates|see more updates|load older|view more updates', re.I)
flat = lambda t: re.sub(r'\s+', ' ', t or '').strip()


def updates(body):
    """The entries of the page's own live-blog record, oldest first (None when the page has no such record)."""
    if b'liveBlogUpdate' not in body: return None, None
    soup = BeautifulSoup(body, 'lxml')
    for s in soup.find_all('script', type='application/ld+json'):
        try: d = json.loads(s.string or '')
        except Exception: continue
        stack = [d]
        while stack:
            x = stack.pop()
            if isinstance(x, list): stack.extend(x)
            elif isinstance(x, dict):
                if 'liveBlogUpdate' in x:
                    u = x['liveBlogUpdate']; u = u if isinstance(u, list) else [u]
                    return sorted(u, key=lambda z: z.get('datePublished', '')), soup
                stack.extend(v for v in x.values() if isinstance(v, (dict, list)))
    return None, soup


def held(u, text):
    """Is this entry in the text read: its headline, or the first 60 characters of its text."""
    t = flat(text); h = flat(u.get('headline')); b = flat(u.get('articleBody'))
    return bool((h and h[:60] in t) or (b and b[:60] in t))


def main():
    arts = {r['page_id']: r for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')}
    text_of = {pid: t for copies in M.articles().values() for pid, t in copies}
    out = []; n_html = 0
    for pid, r in arts.items():
        f = P / pid / 'body.html'
        if not f.exists(): continue
        n_html += 1
        u, soup = updates(f.read_bytes())
        if not u: continue
        t = text_of.get(pid, '')
        more = sorted({flat(b.get_text(' '))[:40] for b in soup.find_all(['button', 'a']) if MORE.search(b.get_text(' ')) and len(flat(b.get_text(' '))) < 40})
        n_read = sum(held(x, t) for x in u)
        out.append({'page_id': pid, 'site': r['site'], 'counted': r['counted'], 'entries_in_the_saved_html': len(u), 'of_them_in_the_text_read': n_read,
                    'first_entry': min(x.get('datePublished', '') for x in u)[:16], 'last_entry': max(x.get('datePublished', '') for x in u)[:16],
                    'control_that_loads_more': '; '.join(more), 'saved_in_part': r['saved_in_part']})
    assert {'huffpost-live', 'cnn-1111-live', 'yahoo-live-ousted', 'sw-financeyahoocom-23'} <= {o['page_id'] for o in out}, 'control: the pages the reading named are not all found'
    with open(R / 'nv8_live_pages.tsv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
    print('pages with a saved HTML', n_html, '| with a live-blog record', len(out), '| counted', sum(o['counted'] == 'yes' for o in out),
          '| whose text read lacks an entry the HTML holds', sum(o['of_them_in_the_text_read'] < o['entries_in_the_saved_html'] for o in out))
    for o in out: print('   ', ' | '.join(str(v) for v in o.values()))


if __name__ == '__main__':
    main()
