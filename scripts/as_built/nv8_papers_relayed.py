"""Every chip that names one of the three papers with a row of its own (the New York Times, the Wall Street Journal, the Financial Times),
or that stands on such a paper's row: how the chip stands toward that paper's own page.

Run: python3 -I scripts/nv8_papers_relayed.py   -> research/nv8_papers_relayed.tsv (row_id, paper, how_it_stands, why)

A chip stands in one of three ways, tried in this order:
  cites the paper's own page       one of the pages the chip cites is on the paper's own site;
  the items table says why not     research/nv8_s6_items.tsv has a line for the chip: part 'original of a chip' (the chips drawn before the
                                   searches of Nov 14 and 15, 2026) or part "a paper's report on a chip" with that paper's name (later chips
                                   that give a paper's report through another outlet while the paper's own page is not held);
  names the paper, not as relayed  the chip names the paper without giving the paper's report through another outlet. These are classed by
                                   hand in BY_HAND, each with one of the reasons in WHY.
The script STOPS when a chip that names a paper stands in none of the three ways (class it, cite the paper's page, or write the table's line),
and when a hand class is no longer needed (take it away). The patterns that find a paper's name leave out other papers with 'Times' or
'Journal' in their names; a control checks that."""
import csv, json, re, sys
from collections import Counter
from pathlib import Path
csv.field_size_limit(10**9)
ROOT = Path(__file__).resolve().parent.parent; R = ROOT / 'research'; sys.path.insert(0, str(ROOT / 'scripts'))
import rows_map

PAPERS = {'The New York Times': ('nyt', 'nytimes.com', r"New York Times|(?<!Financial )(?<!Los Angeles )(?<!Seattle )(?<!Straits )(?<!Japan )(?<!Korea )(?<!Taipei )(?<!Global )(?<!EE )(?<!Business )(?<!Irish )(?<!Hindustan )(?<!Asia )(?<!Gulf )(?<!Kuwait )(?<!Premium )(?<!Tech )\bTimes\b(?! of )"),
          'The Wall Street Journal': ('wsj', 'wsj.com', r"Wall Street Journal|\bthe Journal\b|\bJournal's\b"),
          'Financial Times': ('ft', 'ft.com', r"Financial Times|\bFT\b")}
assert not re.search(PAPERS['The New York Times'][2], 'as the International Business Times quotes him') and re.search(PAPERS['The New York Times'][2], "on the Times's report") and not re.search(PAPERS['Financial Times'][2], 'a SOFTBANK deal')
WHY = {'own statement': "the chip is the actor's own statement, post or reply about the paper's report, cited from the actor's own page or post or from the outlet that carries the statement",
       'pointer': "the paper is named only as a pointer to another chip or to the paper's own row",
       'another outlet': "the words drawn are another outlet's own; the paper's report is named as their occasion"}
T, J, F = 'The New York Times', 'The Wall Street Journal', 'Financial Times'
BY_HAND = {('MA113', T): 'own statement', ('MA145', T): 'own statement', ('MA148', F): 'own statement', ('MA221', T): 'own statement', ('MA277', T): 'own statement',
           ('MA421', F): 'own statement', ('MA422', T): 'own statement', ('MA423', T): 'own statement',
           ('MA157', J): 'pointer', ('MA169', J): 'pointer', ('MA207', T): 'pointer', ('MA293', J): 'pointer', ('MA358', J): 'pointer', ('MA360', T): 'pointer', ('MA361', T): 'pointer',
           ('MA362', J): 'pointer', ('MA392', T): 'pointer',
           ('MA322', T): 'another outlet'}
OLD, NEW = 'original of a chip', "a paper's report on a chip"


def main():
    site_of = {r['page_id']: r['site'] for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')}

    def site(p):
        s = site_of.get(p, '')
        if not s:
            try:
                s = re.sub(r'^https?://(www\.)?', '', json.loads((R / 'primary' / p / 'meta.json').read_text()).get('url', '') or '').split('/')[0]
            except Exception:
                s = ''
        return s.lower()
    items = list(csv.DictReader(open(R / 'nv8_s6_items.tsv', newline=''), delimiter='\t'))
    old = {r['key'] for r in items if r['part'] == OLD}; new = {(r['key'], r['actor']) for r in items if r['part'] == NEW}
    assert all(p in PAPERS for _, p in new) and len(new) == sum(1 for r in items if r['part'] == NEW), 'a line of the new part names no paper, or two lines are alike'
    out, open_, used, used_new = [], [], set(), set()
    for r in rows_map.rows():
        if not r['row_id'].startswith('MA') or r.get('withdrawn'):
            continue
        sites = {site(p) for p in r['src']}
        for paper, (actor, own, pat) in PAPERS.items():
            if not (re.search(pat, r['what']) or r['actor'] == actor):
                continue
            k = (r['row_id'], paper)
            if any(own in s for s in sites):
                how, why = "cites the paper's own page", ''
            elif k in new:
                how, why = 'the items table says why not', "its line of the part \"a paper's report on a chip\""; used_new.add(k)
            elif r['row_id'] in old:
                how, why = 'the items table says why not', "its line of the part 'original of a chip'"
            elif k in BY_HAND:
                how, why = 'names the paper, not as relayed', WHY[BY_HAND[k]]; used.add(k)
            else:
                open_.append(k); continue
            out.append([r['row_id'], paper, how, why])
    assert not open_, ('a chip names a paper and stands in none of the three ways: class it, cite the page or write the line', open_)
    assert used == set(BY_HAND), ('a hand class is no longer needed: take it away', sorted(set(BY_HAND) - used))
    assert used_new == new, ('a line of the items table is no longer needed', sorted(new - used_new))
    with open(R / 'nv8_papers_relayed.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['row_id', 'paper', 'how_it_stands', 'why']); w.writerows(out)
    c = Counter((x[1], x[2]) for x in out); h = Counter(x[2] for x in out)
    print('chips that name one of the three papers or stand on its row:', len({x[0] for x in out}), '| pairs of chip and paper:', len(out), '|', dict(h))
    for p in PAPERS:
        print('  ', p, {k[1]: v for k, v in c.items() if k[0] == p})
    print('by hand:', len(BY_HAND), dict(Counter(BY_HAND.values())), '| lines of the new part:', len(new), "| control: 'International Business Times' is not read as the Times")


if __name__ == '__main__':
    main()
