"""A third pass over the hand-saved PDF pages, by the cause. The owner of the cleaner found why lines were dropped (Nov 16, 2026): it took the line
standing directly above a page number ("10 of 24") for a running title, and some PDFs print the page number at the foot of the page, under the last
line of prose. The two earlier passes (scripts/recover_bodies_4.py, recover_bodies_5.py) looked for raw lines whose words the cleaned text lacks, and
so could not see a dropped line whose words also stand elsewhere in the piece (a one-word line end). This pass takes EVERY line that stands directly
above a page number in the raw text layer of every hand-saved page and asks whether it still follows the line before it in the cleaned text
(text.article.txt). Left out: a line already added, the title under the header block, and one site's mirrored "Feedback" tab. Every line left was read:
prose of the piece (PROSE, written to a new file text.added3.txt beside the page) or not (OTHER: a reporter's biography and the print edition's
headline under the piece, stray letters of a button). A line in neither list stops the script.
Run: python3 -I scripts/recover_bodies_6.py [--write]      (without --write it only shows what it would write)"""
import csv, re, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'; R = ROOT / 'research'
WRITE = '--write' in sys.argv
norm = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
HDR = re.compile(r'^(ID|URL|SAVED|PDF_SHA256|COPY|ROUTE|STATUS|TITLE|OUTLET|PUBLISHED|AUTHOR|EXTENT|MODIFIED|DESCRIPTION|FETCHED|NOTE|SOURCE)\s*:')
FOOT = re.compile(r'^\d+ of \d+$|^\d+/\d+$|^page \d+', re.I); STAMP = re.compile(r'^\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2}|^https?://')
PROSE = {'man-nyt-1112-09': ['economy.']}
OTHER = {'man-456b8da2ad6b': ['g'], 'man-wapo-1112-02': ['pp'],
         'man-8fe865a2b656': ['Maggie Haberman is a White House correspondent for The Times, reporting on President Trump.'],
         'man-d89c11b35532': ['Chips Ending Up? The U.S. Is Asking.'],
         'man-nyt-1029-01': ['Ana Swanson covers trade and international economics for The Times and is based in Washington. She has', 'Target of Chinese Spy Plot']}


def main():
    dirs = sorted(d for d in P.iterdir() if (d / 'text.article.txt').exists() and (d / 'text.txt').exists())
    n_pages = n_foot = 0; tally = Counter(); todo = {}
    for d in dirs:
        raw = (d / 'text.txt').read_text(errors='replace')
        if '\f' not in raw: continue
        n_pages += 1
        held = ' ' + norm((d / 'text.article.txt').read_text(errors='replace')) + ' '
        added = {norm(l) for f in sorted(d.glob('text.added*.txt')) for l in f.read_text(errors='replace').splitlines() if l.strip()}
        left = []
        for pg in raw.split('\f'):
            ls = [l.strip() for l in pg.splitlines() if l.strip()]
            for i, l in enumerate(ls):
                if not FOOT.match(l): continue
                n_foot += 1
                prev = [x for x in ls[:i] if not STAMP.match(x) and not FOOT.match(x)]
                if len(prev) < 2: tally['nothing above it']; continue
                K, L = prev[-2], prev[-1]
                if not norm(L): continue
                if norm(L) in added: tally['already added'] += 1
                elif HDR.match(K): tally['the title under the header block'] += 1
                elif norm(L) == 'kcabdeef': tally['a mirrored Feedback tab'] += 1
                elif (' ' + norm(K) + ' ' + norm(L) + ' ') in held: tally['follows its line in the cleaned text'] += 1
                else: left.append(L)
        if not left: continue
        prose = [l for l in left if l in PROSE.get(d.name, [])]; other = [l for l in left if l not in prose]
        unread = [l for l in other if not any(l.startswith(o) for o in OTHER.get(d.name, []))]
        assert not unread, ('a line no one has read', d.name, unread)
        print(d.name, '| prose', len(prose), '| not prose', len(other)); [print('     +', l) for l in prose]
        if prose: todo[d.name] = prose
    print('hand-saved pages of more than one PDF page', n_pages, '| page numbers', n_foot, '|', dict(tally))
    assert tally['already added'] >= 14 and {k: sorted(v) for k, v in todo.items()} == {k: sorted(v) for k, v in PROSE.items()}        # control: the lines the first passes restored stand above a page number too
    for pid, prose in todo.items():
        f = P / pid / 'text.added3.txt'; assert not f.exists(), ('already written', pid)
        if WRITE: f.write_text('\n'.join(prose) + '\n', encoding='utf-8')
    if not WRITE:
        print('nothing written: read the above, then run again with --write'); return
    t = R / 'nv8_text_added.tsv'; rows = list(csv.reader(open(t, newline=''), delimiter='\t'))
    for r in rows[1:]:
        if r[0] in todo:
            ls = [l for f in sorted((P / r[0]).glob('text.added*.txt')) for l in f.read_text(errors='replace').splitlines() if l.strip()]
            r[2], r[3] = len(ls), sum(len(l) for l in ls)
    assert sum(r[0] in todo for r in rows[1:]) == len(todo)
    with open(t, 'w', newline='') as fh:
        csv.writer(fh, delimiter='\t', lineterminator='\n').writerows(rows)
    print('written:', sorted(todo), '| research/nv8_text_added.tsv updated for them')


if __name__ == '__main__':
    main()
