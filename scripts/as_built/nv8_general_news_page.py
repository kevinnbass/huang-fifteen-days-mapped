"""Run: python3 scripts/nv8_general_news_page.py      (written after the fourteenth reading, Nov 16, 2026)
One counted article is a four-day live page of general news (huffpost-live): 143 entries, 16 of which name Nvidia, Huang or Megaspeed. The figure
counts it like any article (a member is counted when its text names the member anywhere). This lists, for every drawn member the page names, how many
of its entries name the member and how many of those are entries on the matter, so that the figure can mark the members whom the page names only
for other news. Writes research/nv8_general_news_page.tsv. Control: the entries' count and the members the independent reading named."""
import csv, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; P = R / 'primary'
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M, nv8_live_pages as L
PID = 'huffpost-live'; MATTER = re.compile(r'nvidia|huang|megaspeed', re.I)


def main():
    u, _ = L.updates((P / PID / 'body.html').read_bytes()); ent = [(x.get('headline') or '') + '\n' + (x.get('articleBody') or '') for x in u]
    on = [e for e in ent if MATTER.search(e)]; assert len(ent) == 143 and len(on) == 16, (len(ent), len(on))
    _, hit, _ = M.count(); page_article = next(aid for aid, copies in M.articles().items() if any(p == PID for p, _ in copies)); out = []
    for s in M.FIRST:
        rx = M.member_re(s); a = sum(bool(rx.search(e)) for e in ent); b = sum(bool(rx.search(e)) for e in on)
        if a:
            assert page_article in hit[s], ('named in an entry and not counted for the page', s)
            out.append({'member': s, 'entries_naming': a, 'of_them_entries_on_the_matter': b, 'named_only_for_other_news': 'yes' if b == 0 else ''})
    only = sorted(o['member'] for o in out if o['named_only_for_other_news']); assert only == ['Cornyn', 'Johnson', 'Schumer', 'Thune'], only
    with open(R / 'nv8_general_news_page.tsv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
    print('entries', len(ent), '| on the matter', len(on), '| drawn members the page names', len(out), '| named only for other news:', only)


if __name__ == '__main__':
    main()
