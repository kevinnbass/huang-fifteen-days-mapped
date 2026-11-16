"""Entries of live pages that the saved HTML holds and the text read lacked (found by the thirteenth reading, Nov 16, 2026, and then looked for on
every saved page with scripts/nv8_live_pages.py). The first extraction took the entries a live page showed before its "more updates" control; the
page's own structured data (schema.org LiveBlogPosting) holds every entry the page had when it was saved. For each page below, every entry whose
headline and opening the text read does not hold is written, oldest first, to a new file text.added.txt beside the page: the entry's time as the
page gives it, its headline, its author where the page names one, and its text. Nothing is replaced.
Also one short paragraph of one article that the extraction had dropped, which that reading named.
Run: python3 scripts/recover_bodies_7.py [--write]      (without --write it only shows what it would write)"""
import csv, html, re, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M, nv8_live_pages as L
WRITE = '--write' in sys.argv
LIVE = {'huffpost-live': 122, 'cnn-1111-live': 49, 'sw-protoscom-b7e5971b': 1}        # page: entries expected to be added (a different number stops the script)
PARAGRAPH = {'sw-rawstorycom-02': 'Commerce did not comment to Axios.'}
flat = L.flat


def clean(t):
    t = html.unescape(t or '')
    if '<' in t and '>' in t: t = BeautifulSoup(t, 'lxml').get_text(' ')
    return re.sub(r'[ \t]+', ' ', t).strip()


def author(u):
    a = u.get('author'); a = a if isinstance(a, list) else [a] if a else []
    return ', '.join(x.get('name', '') if isinstance(x, dict) else str(x) for x in a if x).strip(', ')


def main():
    text_of = {pid: t for copies in M.articles().values() for pid, t in copies}; rows = []
    for pid, expect in LIVE.items():
        d = P / pid; f = d / 'text.added.txt'; assert not list(d.glob('text.added*.txt')), ('already written', pid)
        u, _ = L.updates((d / 'body.html').read_bytes()); t = text_of[pid]
        miss = [x for x in u if not L.held(x, t)]; assert len(miss) == expect, (pid, len(u), len(miss))
        blocks = ['\n'.join(p for p in (x.get('datePublished', ''), clean(x.get('headline')), ('By ' + author(x)) if author(x) else '', clean(x.get('articleBody'))) if p) for x in miss]
        out = '\n\n'.join(blocks) + '\n'
        print(pid, '| entries in the HTML', len(u), '| already in the text read', len(u) - len(miss), '| to add', len(miss), '| characters', len(out), '| entries with no text of their own', sum(not clean(x.get('articleBody')) for x in miss))
        print('    first:', flat(blocks[0])[:170]); print('    last: ', flat(blocks[-1])[:170])
        if WRITE: f.write_text(out, encoding='utf-8')
        rows.append([pid, 'entries of a live page that the saved HTML holds', len(miss), len(out)])
    for pid, para in PARAGRAPH.items():
        d = P / pid; f = d / 'text.added.txt'; assert not list(d.glob('text.added*.txt')), ('already written', pid)
        soup = BeautifulSoup((d / 'body.html').read_bytes(), 'lxml')
        hit = [p for p in soup.find_all('p') if flat(p.get_text(' ')) == para]; assert len(hit) == 1 and para not in flat(text_of[pid]), (pid, len(hit))
        prev = flat(hit[0].find_previous('p').get_text(' ')); assert prev[:60] in flat(text_of[pid]), ('the paragraph before it is not in the text read', pid)       # it stands inside the article
        print(pid, '| a paragraph of the article, after:', prev[-80:], '>>', para)
        if WRITE: f.write_text(para + '\n', encoding='utf-8')
        rows.append([pid, 'a short paragraph of the article', 1, len(para)])
    if not WRITE:
        print('nothing written: read the above, then run again with --write'); return
    with open(R / 'nv8_text_added.tsv', 'a', newline='') as fh:
        csv.writer(fh, delimiter='\t', lineterminator='\n').writerows(rows)
    print('written:', [r[0] for r in rows])


if __name__ == '__main__':
    main()
