"""Third extraction for saved pages whose article is in the saved HTML and in neither text.txt nor text.reextract.txt (the eighth reading,
Nov 16, 2026: five articles had been left out as block pages although body.html holds them, and several pages listed as saved in part hold
their whole body). Run: python3 scripts/recover_bodies.py   -> text.recovered.txt beside text.txt, for the pages
listed below only; it never changes or replaces a file. The list was made by running scripts/nv8_dense_text.py over every page that the
census readers listed as a gap or whose saved text is short (117 pages) and reading the start and end of each result: a page is listed
when the result is the piece's own text and the saved text was not (metadata only, an ad-blocker wall, another page's headlines, readers'
comments under a story). The result can still carry a teaser or a footer line after the article; quote from it only after reading it.
research/nv8_recovered_pages.tsv records each page, how its text was found and how much."""
import csv, json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; P = ROOT / 'research' / 'primary'
sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_dense_text as D
PAGES = {  # page: what the saved text held before
 'sw-aacomtr-05': 'metadata only', 'sw-capitalbriefcom-01': 'the opening only', 'sw-cnbccom-23': 'headline and description only', 'sw-englobescoil-01': 'metadata only',
 'sw-forbesmiddleeastcom-01': 'metadata only', 'sw-forbesmiddleeastcom-03': 'metadata only', 'sw-globaltimescn-01': "a list of other pieces' headlines",
 'sw-holyroodcom-01': 'metadata only', 'sw-japantimescojp-02': 'metadata only', 'sw-newsercom-01': 'an ad-blocker wall', 'sw-newsercom-02': 'an ad-blocker wall',
 'sw-newsercom-82742fcd': 'an ad-blocker wall', 'sw-newsrthkhk-01': 'headline and navigation only', 'sw-pbsorg-01': 'metadata only', 'sw-pbsorg-02': 'metadata only',
 'sw-tmzcom-02': "another piece's headline", 'sw-garymarcussubstackcom-01': 'a short preview',
 # story pages of one site whose saved text was the readers' comments: the story's own summary is taken
 'sw-hardwareslashdotorg-01': "readers' comments", 'sw-slashdotorg-01': "readers' comments", 'sw-slashdotorg-02': "readers' comments", 'sw-slashdotorg-03': "readers' comments",
 'sw-slashdotorg-b1958825': "readers' comments", 'sw-techslashdotorg-01': "readers' comments", 'sw-yroslashdotorg-01': "readers' comments", 'sw-yroslashdotorg-02': "readers' comments",
}


def main():
    now = subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip(); rows = []
    for pid, before in PAGES.items():
        d = P / pid; m = json.loads((d / 'meta.json').read_text()); out = d / 'text.recovered.txt'
        how, text = D.best_text(d / 'body.html'); assert len(text) >= 300, (pid, len(text))
        if not out.exists():
            with open(out, 'x', encoding='utf-8') as f:     # 'x': fails rather than replace an existing file
                f.write(f"URL: {m.get('url')}\nTITLE: {m.get('title') or ''}\nEXTRACTION: third pass, {now}: {how}, from the saved body.html; the first pass held {before}. May carry a line that is not the article\n\n{text}\n")
        rows.append([pid, how, len(text), before])
    with open(ROOT / 'research' / 'nv8_recovered_pages.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['page_id', 'text_found_in', 'chars', 'first_extraction_held']); w.writerows(rows)
    print(len(rows), 'pages; texts written or already there')


if __name__ == '__main__':
    main()
