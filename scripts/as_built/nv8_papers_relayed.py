"""Every chip that names one of the three papers with a row of its own (the New York Times, the Wall Street Journal, the Financial Times),
that stands on such a paper's row, or that cites a listed copy of one of their articles carried by another outlet: how the chip stands toward
that paper's own page.

Run: python3 -I scripts/nv8_papers_relayed.py   -> research/nv8_papers_relayed.tsv (row_id, paper, how_it_stands, why, copies_cited)

How a pair of chip and paper gets into the table (since the answer to the forty-first reading, which found five pairs missing):
  - the chip's words name the paper (the patterns below; 'the Journal' in either case), or the chip stands on the paper's row; or
  - the chip cites a page listed in COPIES: another outlet's copy of an article of the paper. COPIES is kept by hand from a census of every
    page a live chip cites. The script repeats the census's strong signs on every run (the paper's short name in the page id, a join with a
    page of the paper's own site in the table of articles, one of a few credit lines: the Times's company name or 'originally appeared in The New York Times', an address at wsj.com or the
    words 'Dow Jones', 'The Financial Times Limited') and STOPS on a cited page that shows one and is in neither COPIES nor NOT_COPIES.
    A copy with another credit line, or with none, is not found by it: the forty-second reading found one such page by comparing texts.
How a pair stands, tried in this order:
  the items table says why not     the chip cites a copy of an article of the paper that is not held on the paper's own site, and
                                   research/nv8_s6_items.tsv has a line for the chip: part 'original of a chip' (the chips drawn before the
                                   searches of Nov 14 and 15, 2026) or part "a paper's report on a chip" with that paper's name. Where the
                                   chip also cites a page of the paper's own site for another report, the table says so.
  cites the paper's own page       one of the pages the chip cites is on the paper's own site (and every copy it cites is of an article
                                   that the table of articles joins with a page of that site);
  the items table says why not     no page of the paper's site and no copy is cited, and the items table has a line for the chip;
  names the paper, not as relayed  the chip names the paper without giving the paper's report through another outlet: classed by hand in
                                   BY_HAND, each with one of the reasons in WHY.
The script STOPS when a pair stands in none of these ways, when a hand class is no longer needed, and when a line of the new part is.
'Cites the paper's own page' is a statement about the citation, not a check that the page carries everything the chip takes from the paper:
the forty-first reading read fifteen such pairs and found two that also took a second report of the paper from a copy; those are caught
now through COPIES, and a second report taken from a relay that is not a copy would not be."""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
csv.field_size_limit(10**9)
ROOT = Path(__file__).resolve().parent.parent; R = ROOT / 'research'; sys.path.insert(0, str(ROOT / 'scripts'))
import rows_map

T, J, F = 'The New York Times', 'The Wall Street Journal', 'Financial Times'
PAPERS = {T: ('nyt', 'nytimes.com', r"New York Times|(?<!Financial )(?<!Los Angeles )(?<!Seattle )(?<!Straits )(?<!Japan )(?<!Korea )(?<!Taipei )(?<!Global )(?<!EE )(?<!Business )(?<!Irish )(?<!Hindustan )(?<!Asia )(?<!Gulf )(?<!Kuwait )(?<!Premium )(?<!Tech )\bTimes\b(?! of )"),
          J: ('wsj', 'wsj.com', r"Wall Street Journal|\b[Tt]he Journal\b|\bJournal's\b"),
          F: ('ft', 'ft.com', r"Financial Times|\bFT\b")}
assert not re.search(PAPERS[T][2], 'as the International Business Times quotes him') and re.search(PAPERS[T][2], "on the Times's report") and not re.search(PAPERS[F][2], 'a SOFTBANK deal')
assert re.search(PAPERS[J][2], 'The Journal reports that') and re.search(PAPERS[J][2], 'as the Journal has it')          # the forty-first reading: the capital had escaped the pattern
WHY = {'own statement': "the chip is the actor's own statement, post or reply about the paper's report, cited from the actor's own page or post or from the outlet that carries the statement",
       'pointer': "the paper is named only as a pointer to another chip or to the paper's own row",
       'another outlet': "the words drawn are another outlet's own; the paper's report is named as their occasion"}
BY_HAND = {('MA113', T): 'own statement', ('MA145', T): 'own statement', ('MA148', F): 'own statement', ('MA221', T): 'own statement', ('MA277', T): 'own statement',
           ('MA421', F): 'own statement', ('MA422', T): 'own statement', ('MA423', T): 'own statement',
           ('MA169', J): 'pointer', ('MA207', T): 'pointer', ('MA293', J): 'pointer', ('MA358', J): 'pointer', ('MA360', T): 'pointer', ('MA361', T): 'pointer',
           ('MA362', J): 'pointer', ('MA392', T): 'pointer',
           ('MA322', T): 'another outlet'}
# another outlet's copy of an article of the paper (read in the census of Nov 18, 2026: research/scratch_archive_s9a/papers_copies_census_s11c.tsv in the project, not published)
COPIES = {'art-fc-bs-nyt-1110-woman': T, 'art-fc-bs-nyt-1112-trump': T, 'sw-bostoncom-01': T, 'sw-bostonglobecom-01': T, 'sw-sfexaminercom-02': T,
          'art-fc-itiger-wsj-1030': J, 'art-fc-itiger-wsj-1030-v1': J, 'art-fc-mint-wsj-taiwan': J, 'art-fc-tovima-wsj-1108-board': J, 'art-fc-tovima-wsj-1109-woman': J,
          'art-fc-tovima-wsj-1110': J, 'art-fc-tovima-wsj-1111-oust': J, 'art-fc-tovima-wsj-1112-kangwei': J,
          'art-fc-tovima-ft-1109-admits': F,
          'art-fc-itiger-2682389645': J}          # found by the forty-second reading: a plain Dow Jones credit, which the signs did not read
# a cited page that shows a strong sign and is not a copy
NOT_COPIES = {'ms-ag-bworld-1114-wsj-gain': "an agency's relay of the Journal's report, carried by a third outlet: not a copy of the article"}
ID_SIGN = {T: r'(?:^|-)nyt(?:-|$)', J: r'(?:^|-)wsj(?:-|$)', F: r'(?:^|-)ft(?:-|$)'}
CREDIT = {T: r"The New York Times Company|originally appeared in The New York Times", J: r"@wsj\.com|Dow Jones(?! Industrial)", F: r"The Financial Times Limited"}
OLD, NEW = 'original of a chip', "a paper's report on a chip"


def main():
    art = list(csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')); tab = {r['page_id']: r for r in art}; group = defaultdict(list)
    for r in art:
        group[r['article_id']].append(r['page_id'])

    def site(p):
        s = tab.get(p, {}).get('site', '')
        if not s:
            try:
                s = re.sub(r'^https?://(www\.)?', '', json.loads((R / 'primary' / p / 'meta.json').read_text()).get('url', '') or '').split('/')[0]
            except Exception:
                s = ''
        return s.lower()

    def own_joined(p, own):
        return [q for q in group.get(tab[p]['article_id'], []) if q != p and tab[q]['site'] == own] if p in tab else []
    live = [r for r in rows_map.rows() if r['row_id'].startswith('MA') and not r.get('withdrawn')]
    # the census's strong signs, on every page a live chip cites that is not on one of the three sites
    cited = sorted({p for r in live for p in r['src']}); unlisted = []
    for p in cited:
        if any(o in site(p) for _, o, _ in PAPERS.values()) or p in COPIES or p in NOT_COPIES:
            continue
        d = R / 'primary' / p; t = '\n'.join(f.read_text(errors='replace') for f in sorted(d.glob('text*.txt'))) if d.is_dir() else ''
        for paper, (_, own, _) in PAPERS.items():
            if re.search(ID_SIGN[paper], p) or own_joined(p, own) or re.search(CREDIT[paper], t):
                unlisted.append((p, paper))
    assert not unlisted, ('a cited page shows a strong sign of being a copy of a paper\'s article and is in neither COPIES nor NOT_COPIES: read it and list it', unlisted)
    assert all(p in cited for p in COPIES) and all(p in cited for p in NOT_COPIES), ('a listed page is no longer cited', [p for p in list(COPIES) + list(NOT_COPIES) if p not in cited])
    items = list(csv.DictReader(open(R / 'nv8_s6_items.tsv', newline=''), delimiter='\t'))
    old = {r['key'] for r in items if r['part'] == OLD}; new = {(r['key'], r['actor']) for r in items if r['part'] == NEW}
    assert all(p in PAPERS for _, p in new) and len(new) == sum(1 for r in items if r['part'] == NEW), 'a line of the new part names no paper, or two lines are alike'
    out, open_, used, used_new = [], [], set(), set()
    for r in live:
        pages = list(dict.fromkeys(r['src'])); sites = {p: site(p) for p in pages}
        for paper, (actor, own, pat) in PAPERS.items():
            copies = [p for p in pages if COPIES.get(p) == paper]
            if not (re.search(pat, r['what']) or r['actor'] == actor or copies):
                continue
            k = (r['row_id'], paper); ownp = [p for p in pages if own in sites[p]]; unheld = [p for p in copies if not own_joined(p, own)]
            line = "its line of the part \"a paper's report on a chip\"" if k in new else ("its line of the part 'original of a chip'" if r['row_id'] in old else '')
            if unheld:
                if not line:
                    open_.append((k, 'cites a copy of an article that is not held on the paper\'s site, and has no line', unheld)); continue
                how, why = 'the items table says why not', line + ("; the chip also cites a page of the paper's own site, for another report" if ownp else '')
                if k in new: used_new.add(k)
            elif ownp:
                how, why = "cites the paper's own page", ''
            elif line:
                how, why = 'the items table says why not', line
                if k in new: used_new.add(k)
            elif k in BY_HAND:
                how, why = 'names the paper, not as relayed', WHY[BY_HAND[k]]; used.add(k)
            else:
                open_.append((k, 'stands in none of the ways', [])); continue
            out.append([r['row_id'], paper, how, why, ' '.join(copies)])
    assert not open_, ('class it, cite the paper\'s page or write the line', open_)
    assert used == set(BY_HAND), ('a hand class is no longer needed: take it away', sorted(set(BY_HAND) - used))
    assert used_new == new, ('a line of the items table is no longer needed', sorted(new - used_new))
    with open(R / 'nv8_papers_relayed.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['row_id', 'paper', 'how_it_stands', 'why', 'copies_cited']); w.writerows(out)
    c = Counter((x[1], x[2]) for x in out); h = Counter(x[2] for x in out)
    print('chips that name one of the three papers, stand on its row or cite a copy of its article:', len({x[0] for x in out}), '| pairs of chip and paper:', len(out), '|', dict(h))
    for p in PAPERS:
        print('  ', p, {k[1]: v for k, v in c.items() if k[0] == p})
    print('by hand:', len(BY_HAND), dict(Counter(BY_HAND.values())), '| lines of the new part:', len(new), '| copies listed:', len(COPIES), '| pairs through a copy alone:', sum(1 for x in out if x[4] and not re.search(PAPERS[x[1]][2], next(r['what'] for r in live if r['row_id'] == x[0])) and next(r['actor'] for r in live if r['row_id'] == x[0]) != PAPERS[x[1]][0]),
          "| controls: 'International Business Times' is not read as the Times; 'The Journal' with a capital is read as the Journal")


if __name__ == '__main__':
    main()
