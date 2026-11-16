"""Passages of a page's own piece that the saved HTML holds and the text read lacks: a paragraph, a table, the entries of a list, a photo caption.
Found on Nov 16, 2026 by a screen of every counted page for a member's name that the HTML shows and the text read does not (the reader of the partly
saved pages had found one page whose text lost seven names of a list). Every hit of the screen was read: most are headlines of other stories on the
page and are left alone; these are part of the piece. The passage is written to text.added.txt beside the page's other files (a new name: nothing is
changed or replaced) and research/nv8_text_added.tsv lists each one. The loaders read text.added.txt after the page's text.
Run: python3 scripts/recover_bodies_3.py [--write]"""
import csv, re, sys
from pathlib import Path
from bs4 import BeautifulSoup, Comment
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M
WRITE = '--write' in sys.argv          # without it the passages are only shown: each is read before anything is written beside the saved page
flat = lambda t: re.sub(r'\s+', ' ', t).strip()
words_of = lambda e: flat(' '.join(x for x in e.find_all(string=True) if not isinstance(x, Comment)))        # every string, those inside a <template> too (get_text leaves them out, which is how they were lost)
norm = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
# page: (kind of passage, words that find it in the saved HTML)
# Read and left alone (not this piece): headlines and summaries of other stories; a reader's comment; the title of an embedded video clip; and, on two pages of one
# site, a whole further article that the page keeps in a <template> for its endless scroll (the first run of this script took it for the rest of the article and wrote
# it out; the two files were renamed text.next-article-in-the-feed.not-this-piece.txt and no loader reads them).
PAGES = {'sw-financeyahoocom-11': ('a photo caption', 'is one of the authors of a recently letter'),
         'sw-politicalorg-11': ('a table', 'send letter seeking briefing'),
         'sw-financeyahoocom-d2842b9f': ('a photo caption', 'Mike Johnson'), 'sw-jpostcom-01': ('a photo caption', 'Mike Johnson'), 'sw-rawstorycom-01': ('a photo caption', 'Mike Johnson'),
         'sw-sfstandardcom-03': ('a photo caption', 'Mike Johnson')}


def passage(soup, kind, words):
    hits = [e for e in soup.find_all(string=lambda s: s and words in flat(s)) if e.parent.name not in ('script', 'style', 'title')] or [e for e in soup.find_all(True) if words in words_of(e) and len(words_of(e)) < 900][-1:]
    assert hits, words
    e = hits[0] if hasattr(hits[0], 'name') and hits[0].name else hits[0].parent
    want = {'a table': ('table',), 'a paragraph': ('p',), 'a photo caption': ('figcaption', 'figure', 'p', 'div', 'span')}[kind]
    while e is not None and (e.name not in want or (kind == 'a photo caption' and words not in words_of(e))):
        e = e.parent
    assert e is not None, (kind, words)
    if kind == 'a table':
        return [' | '.join(words_of(c) for c in tr.find_all(['th', 'td'])) for tr in e.find_all('tr')]
    return [words_of(e)]


def main():
    text_of = {pid: t for copies in M.articles().values() for pid, t in copies}
    out = []
    for pid, (kind, words) in PAGES.items():
        d = P / pid; f = d / 'text.added.txt'; assert not f.exists(), ('already written', pid)
        soup = BeautifulSoup((d / 'body.html').read_bytes(), 'lxml'); read = norm(text_of[pid].translate(M.LIGATURES))
        if words is None:             # a list the text read holds in part: its entries that the text lacks
            lines = []
            for lst in soup.find_all(['ul', 'ol']):
                items = [words_of(li) for li in lst.find_all('li', recursive=False)]
                items = [i for i in items if 2 <= len(i.split()) <= 12]
                got = [i for i in items if norm(i) in read]
                if len(items) >= 4 and got and len(got) < len(items) and all(re.search(r'\(|—|-| of ', i) or i[:1].isupper() for i in items):
                    lines += [i for i in items if norm(i) not in read]
            assert lines, pid
        else:
            lines = passage(soup, kind, words)
        lines = [l for l in lines if l]
        assert lines and all(norm(l) not in read for l in lines if len(l) > 40), ('the text read already holds this', pid)
        assert sum(len(l) for l in lines) < 2500, (pid, sum(len(l) for l in lines))
        if WRITE:
            f.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        out.append([pid, kind, len(lines), sum(len(l) for l in lines)])
        print(pid, kind, len(lines), 'lines'); [print('    ', l[:210]) for l in lines[:14]]
    if not WRITE:
        print('nothing written: read the passages above, then run again with --write'); return
    with open(ROOT / 'research' / 'nv8_text_added.tsv', 'x', newline='') as fh:
        w = csv.writer(fh, delimiter='\t', lineterminator='\n'); w.writerow(['page_id', 'what_the_text_read_lacked', 'lines_added', 'characters_added']); w.writerows(out)


if __name__ == '__main__':
    main()
