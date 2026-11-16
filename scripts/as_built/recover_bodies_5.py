"""A second, wider pass over the hand-saved PDF pages, after the twelfth reading's own count for one page (eight lines) came out higher than the first
pass's (scripts/recover_bodies_4.py, which looked only at the lines next to a page break and so missed a dropped line that the PDF's page number
follows after a blank). This pass takes EVERY line of the raw text layer (text.txt) that the cleaned text (text.article.txt) and the lines already
added (text.added.txt) do not hold, on every page that has a cleaned text, and leaves out only: the header fields, page numbers, print times and
addresses, the page's running title, and a line repeated on three or more PDF pages. Every line left was read (Nov 16, 2026): it is either prose of
the piece (PROSE, written to a new file text.added2.txt beside the page) or furniture (FURNITURE: menus, a reporter's biography, the print
edition's headline, "Reuse this content"). A line in neither list stops the script.
Run: python3 -I scripts/recover_bodies_5.py [--write]      (without --write it only shows what it would write)"""
import csv, re, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'; R = ROOT / 'research'
WRITE = '--write' in sys.argv
norm = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
HDR = re.compile(r'^(ID|URL|SAVED|PDF_SHA256|COPY|ROUTE|STATUS|TITLE|OUTLET|PUBLISHED|AUTHOR|EXTENT|MODIFIED|DESCRIPTION|FETCHED|NOTE|SOURCE)\s*:')
FURN = re.compile(r'^(\d+ of \d+|\d+/\d+|\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2}.*|https?://\S+|page \d+.*)$', re.I)
PROSE = {'man-8fe865a2b656': ['in Alaska.', 'employee.'],
         'man-nyt-1112-09': ['Devices.', 'weigh on shares.', 'leather-clad co-founder and chief executive.', 'has frequently appeared alongside him.']}
FURNITURE = {'● Insider', 'Weekly edition', 'World in brief', 'Opinion', 'United States', 'Finance & economics', 'Business', 'China', 'For you', 'Menu', '0:00 / 0:00', 'Share', 'Reuse this content',
             'Chips Ending Up? The U.S. Is Asking.', 'Target of Chinese Spy Plot', 'Save', 'g', 'pp'}          # the last two: the print edition's headline, in the note under the piece
BIO = re.compile(r'^[A-Z][a-z]+ [A-Z][a-z]+ (?:is a|covers) .{10,80} for The Times')    # a reporter's biography under the piece


def main():
    dirs = sorted(d for d in P.iterdir() if (d / 'text.article.txt').exists() and (d / 'text.txt').exists())
    left = defaultdict(list); n_pages = 0
    for d in dirs:
        raw = (d / 'text.txt').read_text(errors='replace'); held = norm((d / 'text.article.txt').read_text(errors='replace'))
        if (d / 'text.added.txt').exists(): held += ' ' + norm((d / 'text.added.txt').read_text(errors='replace'))
        pages = raw.split('\f')
        if len(pages) < 2: continue
        n_pages += 1
        m = re.search(r'(?m)^TITLE:\s*(.+)$', raw); title = norm(m.group(1)) if m else ''
        cand = [l.strip() for pg in pages for l in pg.splitlines() if l.strip() and not HDR.match(l.strip()) and not FURN.match(l.strip())]
        cand = [l for l in cand if norm(l) and not re.search(r'(?:^| )' + re.escape(norm(l)) + r'(?: |$)', held)]
        freq = Counter(norm(l) for l in cand)
        for l in cand:
            n = norm(l)
            if n == 'kcabdeef' or freq[n] >= 3 or (title and (n.startswith(title[:22]) or (title.startswith(n[:22]) and len(n) > 12))): continue
            left[d.name].append(l)
    print('pages with a cleaned text', len(dirs), '| of them with more than one PDF page', n_pages, '| pages with a line left to class', len(left))
    todo = {}
    for pid, lines in sorted(left.items()):
        prose = [l for l in lines if l in PROSE.get(pid, [])]; other = [l for l in lines if l not in prose]
        unread = [l for l in other if l not in FURNITURE and not BIO.match(l) and not l.startswith('World in brief: ')]         # the last: a link to another piece in the site's menu
        assert not unread, ('a line no one has read', pid, unread)
        assert sorted(prose) == sorted(PROSE.get(pid, [])), ('a listed line of prose was not found', pid)
        print(pid, '| prose', len(prose), '| furniture', len(other)); [print('     +', l) for l in prose]
        if prose: todo[pid] = prose
    assert set(todo) == set(PROSE)
    for pid, prose in todo.items():
        f = P / pid / 'text.added2.txt'; assert not f.exists(), ('already written', pid)
        if WRITE: f.write_text('\n'.join(prose) + '\n', encoding='utf-8')
    if not WRITE:
        print('nothing written: read the above, then run again with --write'); return
    t = R / 'nv8_text_added.tsv'; rows = list(csv.reader(open(t, newline=''), delimiter='\t'))
    for r in rows[1:]:
        if r[0] in todo:
            ls = [l for n in ('text.added.txt', 'text.added2.txt') for l in (P / r[0] / n).read_text(errors='replace').splitlines() if l.strip()]
            r[2], r[3] = len(ls), sum(len(l) for l in ls)
    assert sum(r[0] in todo for r in rows[1:]) == len(todo)
    with open(t, 'w', newline='') as fh:
        csv.writer(fh, delimiter='\t', lineterminator='\n').writerows(rows)
    print('written:', sorted(todo), '| research/nv8_text_added.tsv updated for them')


if __name__ == '__main__':
    main()
