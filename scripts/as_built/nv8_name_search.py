"""Whole-name search of the look-up registers in the 85 top-level tables of the four evidence sets (a backstop to the look-up lanes).

Run: python3 -I scripts/nv8_name_search.py
Reads research/nv8_gap_register.tsv (analysts and bylines). Two passes, one read of each table:
  people : every name of two to four words that reads as a person's name (letters, no organisation word), searched as a whole name;
  others : every other analyst entry (a firm, a one-word name, a longer label), searched as a whole name, with the rows that also name
           Anthropic, Open Philanthropy, Coefficient Giving or Nvidia counted apart.
Writes (private, not published: they name people for whom nothing was found)
  research/nv8_name_search_names.tsv   the frozen query list: pass, register, key, name as searched
  research/nv8_name_search_hits.tsv    one line per register line whose name occurs in a table
and (published) research/nv8_name_search_counts.tsv, the counts the figure prints. Controls: names known to be in the sets must be found."""
import csv, glob, re, collections
from pathlib import Path
csv.field_size_limit(10**9)
R = Path(__file__).resolve().parent.parent / 'research'
PACKS = 'EVIDENCE_SETS/'
ORG = ('analysts', 'research', 'staff', 'news', 'team', 'the', 'and', 'capital', 'group', 'securities', 'bank', 'university', 'institute', 'editors', 'wire', 'reports', 'desk')
CONTROLS = ['Shakeel Hashim', 'Jared Perlo', 'Jason Ly', 'Jordan Schneider', 'Zvi Mowshowitz', 'Fazl Barez', 'Geoffrey Cain']
TIE = re.compile(r'Anthropic|Open Philanthropy|Coefficient Giving|Nvidia|NVIDIA')


def person(n):
    n = n.strip()
    if n.startswith('http') or not re.fullmatch(r"[A-Za-zÀ-ÿ.'’\- ]{5,60}", n):
        return None
    w = n.split()
    if not 2 <= len(w) <= 4 or any(x.lower() in ORG for x in w):
        return None
    return n


def main():
    norm = lambda n: re.sub(r'\s+', ' ', n.strip().replace('’', "'"))
    rows = [r for r in csv.DictReader(open(R / 'nv8_gap_register.tsv', newline=''), delimiter='\t') if r['register'] in ('analyst', 'byline')]
    people, others, left = collections.defaultdict(list), collections.defaultdict(list), []
    for r in rows:
        n = norm(r['name'])
        if person(n):
            people[n].append(r)
        elif r['register'] == 'analyst' and not n.startswith('http') and len(re.sub(r'[^A-Za-z]', '', n)) >= 4:
            others[n].append(r)
        else:
            left.append(r)                                   # a byline that is an agency, a label or an address; an analyst label under four letters
    allnames = sorted(set(people) | set(others) | set(CONTROLS), key=len, reverse=True)
    rx = re.compile(r'(?<![A-Za-z])(' + '|'.join(re.escape(n) for n in allnames) + r')(?![A-Za-z])')
    files = []
    for base in ('lineage/research/', 'congress/research/', 'toner/research/', 'evaluators-deep/research/'):
        files += sorted(glob.glob(PACKS + base + '*.csv')) + sorted(glob.glob(PACKS + base + '*.tsv'))
    hits, tied = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    for f in files:
        short = '/'.join(f.split('/')[-3:])
        for line in open(f, errors='replace'):
            line = line.replace('’', "'")
            for m in rx.finditer(line):
                hits[m.group(1)][short] += 1
                if TIE.search(line):
                    tied[m.group(1)][short] += 1
    found = {c: sum(hits[c].values()) for c in CONTROLS}
    assert len(files) == 85 and all(found.values()), ('control: a name known to be in the sets was not found, or the tables changed', len(files), found)
    with open(R / 'nv8_name_search_names.tsv', 'w', newline='') as fh:
        w = csv.writer(fh, delimiter='\t', lineterminator='\n'); w.writerow(['pass', 'register', 'key', 'name'])
        for tag, d in (('people', people), ('others', others)):
            for n, rs in sorted(d.items()):
                w.writerows([tag, r['register'], r['key'], n] for r in rs)
        w.writerows(['not searched', r['register'], r['key'], norm(r['name'])] for r in left)
    n_hit = collections.Counter()
    with open(R / 'nv8_name_search_hits.tsv', 'w', newline='') as fh:
        w = csv.writer(fh, delimiter='\t', lineterminator='\n'); w.writerow(['pass', 'register', 'key', 'name', 'status', 'tables', 'tables_with_a_row_that_also_names_a_company_or_funder'])
        for tag, d in (('people', people), ('others', others)):
            for n, rs in sorted(d.items()):
                if hits[n]:
                    for r in rs:
                        n_hit[tag] += 1
                        w.writerow([tag, r['register'], r['key'], n, r['status'], '; '.join(f'{k}:{v}' for k, v in hits[n].most_common()), '; '.join(f'{k}:{v}' for k, v in tied[n].most_common())])
    low = lambda d: len({n.lower() for n in d})
    counts = [('register lines of analysts and bylines', len(rows)), ('tables searched', len(files)),
              ('people: register lines searched', sum(map(len, people.values()))), ('people: different names searched', low(people)),
              ('people: register lines whose name occurs in a table', n_hit['people']),
              ('others (firms, one-word names, longer labels among the analysts): register lines searched', sum(map(len, others.values()))),
              ('others: different names searched', low(others)), ('others: register lines whose name occurs in a table', n_hit['others']),
              ('not searched as a whole name (bylines that are an agency, a label or an address; analyst labels under four letters)', len(left)),
              ('controls found, of %d' % len(CONTROLS), sum(v > 0 for v in found.values()))]
    with open(R / 'nv8_name_search_counts.tsv', 'w', newline='') as fh:
        w = csv.writer(fh, delimiter='\t', lineterminator='\n'); w.writerow(['what', 'count']); w.writerows(counts)
    for c in counts:
        print(f'{c[1]:>6}  {c[0]}')


if __name__ == '__main__':
    main()
