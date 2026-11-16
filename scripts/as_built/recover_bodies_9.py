"""Small parts of two live pages that their saved HTML holds and the text read lacked, named by the fourteenth reading (Nov 16, 2026).
1. cnn-1111-live: the signature of a letter and the attribution under a pull quotation. The page has 69 entries in its structured data and a
   summary; 20 entries and the summary have a rendered body in the saved copy (the other 49 containers are empty placeholders, and their text came
   from the structured data). Each block of the 21 rendered bodies was compared with the text read; a short block counts as present only when it
   follows the block before it (scripts/recover_bodies_8.py had skipped blocks under eight characters and had called all 70 containers visible entries).
   What is still not in the text read after this: photo credits.
2. sw-aljazeeracom-07: two of the four summary bullets that the page keeps in an encoded data block. The page's 27 live entries are not in the
   saved copy (only their ids and times), and the page stays marked as held in part.
New files beside the pages; nothing is replaced.
Run: python3 scripts/recover_bodies_9.py [--write]      (without --write it only shows what it would write)"""
import base64, csv, html, re, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M
WRITE = '--write' in sys.argv
flat = lambda t: re.sub(r'\s+', ' ', t or '').strip()


def main():
    text_of = {p: x for copies in M.articles().values() for p, x in copies}; rows = []
    # 1
    pid = 'cnn-1111-live'; d = P / pid; f = d / 'text.added3.txt'; assert not f.exists(), 'already written'
    soup = BeautifulSoup((d / 'body.html').read_bytes(), 'lxml'); ft = flat(text_of[pid])
    boxes = soup.select('article.live-story-post, div.live-story-post, [data-component-name="live-story-post"]'); posts = [p for p in boxes if flat(p.get_text(' '))]
    miss = []; n = 0; added_lines = {flat(l) for l in M.added(d).splitlines()}          # a line already added on its own (the salutation) is not added twice
    for p in posts:
        blocks = [b for b in (flat(el.get_text(' ')) for el in p.find_all(['p', 'blockquote', 'li', 'h2', 'h3']) if not el.find(['p', 'li'])) if b]
        for i, s in enumerate(blocks):
            n += 1; before = blocks[i - 1][-40:] if i else ''
            if s[:60] not in ft: miss.append((before, s))
            elif i and before in ft and len(s) < 60 and (before + ' ' + s) not in ft and (before + s) not in ft and s not in added_lines: miss.append((before, s))
    print(pid, '| containers', len(boxes), '| with a rendered body', len(posts), '| blocks compared', n, '| not in the text read at their place:', len(miss))
    for b, s in miss: print('    after "…' + b + '":', s)
    assert len(boxes) == 70 and len(posts) == 21 and sorted(s for _, s in miss) == ['Colette', 'Jensen Huang'], miss
    lines = [s for _, s in miss]
    if WRITE: f.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    rows.append([pid, 'two short lines inside its entries (the signature of a letter, the attribution of a pull quotation)', len(lines), sum(len(s) for s in lines)])
    # 2
    pid = 'sw-aljazeeracom-07'; d = P / pid; f = d / 'text.added.txt'; assert not list(d.glob('text.added*.txt')), 'already written'
    body = (d / 'body.html').read_text(errors='replace'); ft = flat(text_of[pid]); found = []
    for c in re.findall(r'[A-Za-z0-9+/=]{2000,}', body):
        try: dec = base64.b64decode(c + '=' * (-len(c) % 4)).decode('utf-8', 'replace')
        except Exception: continue
        items = [flat(html.unescape(re.sub(r'<[^>]+>', ' ', m))) for m in re.findall(r'<li>(.*?)</li>', dec, flags=re.S)]
        if len(items) == 4 and items[0].startswith('Jensen Huang, 63, has resigned'): found = items
    assert len(found) == 4, 'the four summary bullets were not found'
    held = [x for x in found if x[:60] in ft]; lack = [x for x in found if x[:60] not in ft]
    print(pid, '| summary bullets in the saved data', len(found), '| in the text read', len(held), '| to add', len(lack))
    for x in lack: print('    +', x)
    assert len(lack) == 2
    if WRITE: f.write_text('\n'.join(lack) + '\n', encoding='utf-8')
    rows.append([pid, 'two short summary bullets of a live page, from its encoded data block', len(lack), sum(len(x) for x in lack)])
    if not WRITE:
        print('nothing written: read the above, then run again with --write'); return
    with open(R / 'nv8_text_added.tsv', 'a', newline='') as fh:
        csv.writer(fh, delimiter='\t', lineterminator='\n').writerows(rows)
    print('written')


if __name__ == '__main__':
    main()
