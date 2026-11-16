"""Fourth extraction, for recovered pages whose third extraction (scripts/recover_bodies.py) left out part of the article or carried lines
that are not the article (the ninth reading, Nov 16, 2026: three Newser texts held one of the story's two paragraphs, one with the site's
"Read These Next" headlines after it; a Globes text held the site's related headlines in the middle of the article). A rule per site, read
from the page's own markup. Writes text.recovered2.txt beside the earlier files (a new name: nothing is changed or replaced) and
research/nv8_recovered_pages_2.tsv. The loaders read text.recovered2.txt before text.recovered.txt.
Run: python3 scripts/recover_bodies_2.py"""
import csv, json, re, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'
sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_dense_text as D
flat = lambda t: re.sub(r'\s+', ' ', t).strip()


def newser(soup):
    """The headline and every paragraph the site marks as the story's."""
    ps = [flat(p.get_text(' ')) for p in soup.select('p.storyParagraph')]; assert len(ps) >= 2, len(ps)
    return 'the headline and the paragraphs marked storyParagraph', [flat(soup.h1.get_text(' '))] + ps


def globes(soup):
    """The article's paragraphs, without the block of related headlines that sits among them."""
    more = soup.find('section', id='moreArticles'); box = more.parent; more.decompose()
    ps = [flat(p.get_text(' ')) for p in box.find_all('p', recursive=False)]; assert len(ps) >= 6, len(ps)
    return "the paragraphs of the article's own block, without the section of related headlines", [flat(soup.h1.get_text(' '))] + [p for p in ps if p]


PAGES = {'sw-newsercom-01': (newser, 'one of the two paragraphs, then the site\'s "Read These Next" headlines'), 'sw-newsercom-02': (newser, 'one of the two paragraphs'),
         'sw-newsercom-82742fcd': (newser, 'one of the two paragraphs'), 'sw-englobescoil-01': (globes, 'the article with five related headlines in the middle of it')}


def main():
    now = subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip(); rows = []
    for pid, (rule, before) in PAGES.items():
        d = P / pid; m = json.loads((d / 'meta.json').read_text()); out = d / 'text.recovered2.txt'
        how, parts = rule(BeautifulSoup(D.read(d / 'body.html'), 'lxml')); text = '\n\n'.join(parts)
        if not out.exists():
            with open(out, 'x', encoding='utf-8') as f:     # 'x': fails rather than replace an existing file
                f.write(f"URL: {m.get('url')}\nTITLE: {parts[0]}\nEXTRACTION: fourth pass, {now}: {how}, from the saved body.html; the third pass held {before}\n\n{text}\n")
        rows.append([pid, how, len(text), len(parts) - 1, before])
    with open(ROOT / 'research' / 'nv8_recovered_pages_2.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['page_id', 'text_found_in', 'chars', 'paragraphs', 'third_extraction_held']); w.writerows(rows)
    print(len(rows), 'pages; texts written or already there')


if __name__ == '__main__':
    main()
