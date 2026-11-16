"""Three lines of one live page (cnn-1111-live) that its saved HTML shows inside its entries and the text read lacked, found when a census reader
read the page again after its entries were recovered (lane remarks_nv8_i, Nov 16, 2026): an analyst's quoted note that follows "Ives said:", a pull
quotation, and the salutation of a letter. Every block (paragraph, list item, heading) of the page's 70 visible entries was compared with the text
read; what else is missing is photo credits, which are left out. Written to a new file text.added2.txt beside the page.
Run: python3 scripts/recover_bodies_8.py [--write]      (without --write it only shows what it would write)"""
import csv, re, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M
WRITE = '--write' in sys.argv; PID = 'cnn-1111-live'
flat = lambda t: re.sub(r'\s+', ' ', t or '').strip()


def main():
    d = P / PID; f = d / 'text.added2.txt'; assert not f.exists(), 'already written'
    soup = BeautifulSoup((d / 'body.html').read_bytes(), 'lxml'); ft = flat({p: x for copies in M.articles().values() for p, x in copies}[PID])
    posts = soup.select('article.live-story-post, div.live-story-post, [data-component-name="live-story-post"]'); assert len(posts) >= 69, len(posts)
    miss, credits = [], 0
    for p in posts:
        for el in p.find_all(['p', 'blockquote', 'li', 'h2', 'h3', 'figcaption']):
            if el.find(['p', 'li']): continue
            s = flat(el.get_text(' '))
            if len(s) < 8 or s[:50] in ft: continue
            if el.name == 'figcaption': credits += 1
            elif s not in miss: miss.append(s)
    print(PID, '| visible entries', len(posts), '| blocks the text read lacks:', len(miss), '| photo credits left out:', credits)
    for s in miss: print('    +', s[:150])
    assert len(miss) == 3 and any(s.startswith('The old Jensen') for s in miss), miss
    if not WRITE:
        print('nothing written: read the above, then run again with --write'); return
    f.write_text('\n'.join(miss) + '\n', encoding='utf-8')
    t = R / 'nv8_text_added.tsv'; rows = list(csv.reader(open(t, newline=''), delimiter='\t'))
    hit = [r for r in rows if r[0] == PID]; assert len(hit) == 1 and 'live page' in hit[0][1]
    rows.append([PID, 'three short passages inside its entries (a quoted note, a pull quotation, a salutation)', len(miss), sum(len(s) for s in miss)])
    with open(t, 'w', newline='') as fh:
        csv.writer(fh, delimiter='\t', lineterminator='\n').writerows(rows)
    print('written')


if __name__ == '__main__':
    main()
