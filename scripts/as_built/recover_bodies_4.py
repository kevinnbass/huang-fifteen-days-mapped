"""Two repairs of the text read, both found by the twelfth reading (Nov 16, 2026) and then looked for on every page of the kind.
1. Hand-saved PDF pages: the cleaner that cuts the article out of the PDF's text layer dropped a line of prose at some page breaks. Every such
   page's raw layer (text.txt) was compared with its cleaned text (text.article.txt) at each page break (144 pages; the candidates were read: most
   are running titles and footers). The lines of prose are written to text.added.txt beside the page (a new file; nothing is replaced). Each is
   one line of a sentence that the cleaned text still breaks off: the words are restored for searching, not the sentence's order.
2. Two pages of one site show, under the article, the opening of the next article of an endless scroll. That opening was in the text read. The
   text up to it is written as text.recovered2.txt (a new file, read first by the loaders).
Run: python3 scripts/recover_bodies_4.py [--write]      (without --write it only shows what it would write)"""
import csv, re, sys
from pathlib import Path
from bs4 import BeautifulSoup, Comment
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M
WRITE = '--write' in sys.argv
flat = lambda t: re.sub(r'\s+', ' ', t).strip()
norm = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
# page: the opening words of each dropped line (read on Nov 16, 2026; bylines' biographies, running titles and "Reuse this content" are left out)
PDF_LINES = {'man-8fe865a2b656': ['president on the intelligence showing', '2026, according to trade records obtained', 'Huang’s relationship with the woman was romantic', 'company. He had been married to'],
             'man-d89c11b35532': ['In Singapore and Malaysia, traces of Megaspeed', 'Singapore, where employees told a Times reporter', 'When a Times reporter visited, three employees'],
             'man-nyt-1029-01': ['person with knowledge of the plans.'],
             'man-nyt-1112-09': ['opening for Google and Amazon.', 'the company as well as with a woman who', 'authority as Huang did.', 'A timeline shows how Huang', 'Huang over Trump’s approach to A.I. and China.', 'without interruption.”']}
FEED = ('sw-easterneyebiz-01', 'sw-easterneyebiz-02')


def main():
    added, trimmed = [], []
    for pid, starts in PDF_LINES.items():
        d = P / pid; raw = (d / 'text.txt').read_text(errors='replace'); art = norm((d / 'text.article.txt').read_text(errors='replace')); f = d / 'text.added.txt'
        assert not f.exists(), ('already written', pid)
        lines = []
        for s in starts:
            hit = [l.strip() for l in raw.replace('\f', '\n').splitlines() if l.strip().startswith(s)]; assert len(hit) == 1, (pid, s, len(hit))
            assert norm(hit[0]) not in art, ('the cleaned text holds this line', pid, s); lines.append(hit[0])
        print(pid, len(lines), 'lines at page breaks'); [print('    ', l[:150]) for l in lines]
        if WRITE: f.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        added.append([pid, 'lines of prose at page breaks of the PDF', len(lines), sum(len(l) for l in lines)])
    text_of = {pid: t for copies in M.articles().values() for pid, t in copies}
    for pid in FEED:
        d = P / pid; f = d / 'text.recovered2.txt'; assert not f.exists(), ('already written', pid)
        soup = BeautifulSoup((d / 'body.html').read_bytes(), 'lxml'); tpl = soup.find('template'); t = text_of[pid]
        # the next article is the <article> element that holds the template; the cut is at the earliest of its own sentences (40 characters or
        # more, so that a byline both pieces share cannot move it) found in the text read: its standfirst comes before its first paragraphs
        box = tpl.find_parent('article'); assert box is not None and box is not soup.find('article'), pid
        own = [flat(s) for s in box.find_all(string=True) if not isinstance(s, Comment) and s.find_parent(['template', 'script', 'style']) is None]
        at = [a for a in (t.find(s[:60]) for s in own if len(s) >= 40) if a >= 0]; assert at and min(at) > 3000, (pid, at)
        cut = min(at); keep = t[:cut].rstrip()
        assert len(t) - cut < 900 and len(keep) > 3000, (pid, cut, len(t))
        assert not any(s[:60] in keep for s in own if len(s) >= 40), ('a sentence of the next article is still in the kept text', pid)
        print(pid, 'cut at', cut, 'of', len(t), '| removed:', flat(t[cut:])[:260]); print('     kept text ends:', flat(keep[-200:]))
        if WRITE: f.write_text(keep + '\n', encoding='utf-8')
        trimmed.append([pid, len(t), len(keep)])
    if not WRITE:
        print('nothing written: read the above, then run again with --write'); return
    with open(R / 'nv8_text_added.tsv', 'a', newline='') as fh:
        csv.writer(fh, delimiter='\t', lineterminator='\n').writerows(added)
    with open(R / 'nv8_text_trimmed.tsv', 'x', newline='') as fh:
        w = csv.writer(fh, delimiter='\t', lineterminator='\n'); w.writerow(['page_id', 'characters_read_before', 'characters_read_now', 'what_was_cut']); w.writerows(r + ["the opening of the next article of the site's endless scroll"] for r in trimmed)


if __name__ == '__main__':
    main()
