"""One line per saved news page with the article it is a copy of, so that a count of "pages" counts each article once.

Run: nice python3 -I scripts/nv8_articles.py   -> research/nv8_articles.tsv, and a summary
Pages: the 1,086 of the first census (scripts/member_mentions.pages) and the pages saved since (the list of lane remarks_nv8_e).
Two pages are the same article only on proof: the same address, or the text of one contained in the other (seven-word runs: at least
80% of the shorter page's runs occur in the longer, and the shorter has at least 150). Anything less keeps both (Kevin, 2026-11-15:
"count them for everyone. don't use duplicates. deduplicate. don't add the pieces dates 13 and 14."). A page of either set is not counted when its
own stamp, read as a U.S. Eastern day, is after Nov 12, 2026 (a republished copy stamped later is counted only through a counted copy of
the same article) or before Oct 29, 2026 (a background page: an earlier article, a biography, a statement of 2025); a page saved since the census is also not counted when it has no article text or is not a news piece (a reference
page, a company's own site, an image). The day of a page is read by scripts/nv8_page_dates.py (the header stamp, or the page's own address or
stamp line where the header has none); a page whose day cannot be read is counted. Controls: two pairs known to be copies of one article must be joined, and two different articles must not be."""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import member_mentions as M
import nv8_page_dates as D
ROOT = Path(__file__).resolve().parent.parent; R = ROOT / 'research'; P = R / 'primary'
LANE = Path('lanes/remarks_nv8_e')
FIRST, LAST = '2026-10-29', '2026-11-12'
NOT_NEWS = ('wikipedia.org', 'megaspeed.ai', 'pbs.twimg.com')


def runs(text):
    body = text.split('\n\n', 1)[1] if '\n\n' in text[:1500] else text
    w = re.findall(r"[a-z0-9']+", body.lower().replace('’', "'"))
    return {hash(' '.join(w[i:i + 7])) for i in range(len(w) - 6)}


def main():
    pages = []                                                    # (id, set, text)
    for pid, text in M.pages():
        pages.append((pid, 'first census', text))
    first = len(pages)
    gaps = {r['page_id'] for r in csv.DictReader(open(LANE / 'out' / 'gaps.csv', newline=''))}
    for r in csv.DictReader(open(LANE / 'pages.tsv', newline=''), delimiter='\t'):
        t = Path(r['text_path']); pages.append((r['page_id'], 'saved since', t.read_text(errors='replace') if t.exists() else ''))
    info = {pid: D.meta(pid) for pid, _, _ in pages}
    host = lambda u: re.sub(r'^www\.', '', re.sub(r'^https?://', '', u).split('/')[0].lower())
    key = lambda u: re.sub(r'^https?://(www\.)?', '', u.split('?')[0].split('#')[0]).rstrip('/').lower()
    S = {pid: runs(text) for pid, _, text in pages}
    parent = {pid: pid for pid, _, _ in pages}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    why = {}
    by_key = defaultdict(list)
    for pid, _, _ in pages:
        if info[pid][0]:
            by_key[key(info[pid][0])].append(pid)
    for ids in by_key.values():
        for b in ids[1:]:
            parent[find(b)] = find(ids[0]); why[b] = f'same address as {ids[0]}'
    idx = defaultdict(list)
    for pid, s in S.items():
        if len(s) >= 150:
            for h in s:
                idx[h].append(pid)
    share = Counter()
    for ids in idx.values():
        if 1 < len(ids) <= 40:                                    # a run on more than 40 pages is boilerplate
            for i, a in enumerate(ids):
                for b in ids[i + 1:]:
                    share[(a, b)] += 1
    joined = []
    for (a, b), n in share.items():
        small = min(len(S[a]), len(S[b]))
        c = len(S[a] & S[b]) / small
        if c >= 0.80:
            if find(a) != find(b):
                parent[find(b)] = find(a)
            joined.append((a, b, round(c, 2)))
            why.setdefault(b, f'text of the shorter is {c:.0%} inside the other ({a})')
    same = lambda a, b: find(a) == find(b)
    assert same('man-923fe8754943', 'art-fc-itiger-wsj-1030') and same('art-fc-cnn-1112', 'art-fc-rec-ktvz-cnn-1112'), 'control: two copies of one article were not joined'
    assert not same('man-nyt-1029-01', 'man-nyt-1106-01'), 'control: two different articles were joined'
    order = {}; out = []; n_art = 0
    for pid, which, text in pages:
        root = find(pid)
        if root not in order:
            n_art += 1; order[root] = f'A{n_art:04d}'
        url, title, given = info[pid]
        pub, basis, read_from = D.day_of(pid, url, title, given)
        counted, reason = 'yes', ''
        if which == 'saved since' and any(x in host(url) for x in NOT_NEWS):
            counted, reason = 'no', 'not a news piece (a reference page, a company site or an image)'
        elif pub not in ('', '?') and pub > LAST:
            counted, reason = 'no', f'dated {pub} (U.S. Eastern), after the fifteen days'
        elif pub not in ('', '?') and pub < FIRST:
            counted, reason = 'no', f'dated {pub}, before the fifteen days (a background page)'
        elif which == 'saved since' and len(S[pid]) < 150 and pid in gaps:
            counted, reason = 'no', 'no article text could be read (see the census gaps)'
        out.append([pid, which, order[root], host(url), pub, basis, read_from[:60], len(text), counted, reason, why.get(pid, ''), title])
    with open(R / 'nv8_articles.tsv', 'w', newline='') as f:           # published with the figure: no headline, no text
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['page_id', 'set', 'article_id', 'site', 'day', 'day_basis', 'day_read_from', 'chars', 'counted', 'why_not', 'joined_on']); w.writerows(o[:11] for o in out)
    with open(R / 'nv8_articles_titles.tsv', 'w', newline='') as f:    # held with the project: each page's headline, for reading the table
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['page_id', 'article_id', 'title']); w.writerows([o[0], o[2], o[11]] for o in out)
    art = defaultdict(list)
    for o in out:
        art[o[2]].append(o)
    cnt = {a: v for a, v in art.items() if any(o[8] == 'yes' for o in v)}
    new_only = [a for a, v in cnt.items() if all(o[1] == 'saved since' for o in v)]
    print(f'pages: {first} of the first census + {len(pages) - first} saved since = {len(pages)}')
    print(f'articles: {len(art)} in all; counted {len(cnt)}; of those, {len(new_only)} are known only from pages saved since')
    print('first-census pages that are a copy of another first-census page:', sum(len([o for o in v if o[1] == 'first census']) - 1 for v in art.values() if len([o for o in v if o[1] == 'first census']) > 1))
    print('pages saved since: not counted', dict(Counter(o[9].split(',')[0][:22] for o in out if o[1] == 'saved since' and o[8] == 'no')),
          '| counted', sum(o[1] == 'saved since' and o[8] == 'yes' for o in out), '| of those, a copy of a first-census page:', sum(1 for o in out if o[1] == 'saved since' and o[8] == 'yes' and any(x[1] == 'first census' for x in art[o[2]])))
    print('how each page was dated:', dict(Counter((o[1], o[5]) for o in out)))
    print('pages dated before Oct 29:', dict(Counter(o[1] for o in out if 'before the fifteen days' in o[9])))
    print('first-census pages dated after Nov 12 (Eastern):', sum(1 for o in out if o[1] == 'first census' and 'after the fifteen days' in o[9]), '| with no day:', sum(1 for o in out if o[1] == 'first census' and not o[4]),
          '| stamps that could not be read:', sorted({o[6] for o in out if o[5] == 'stamp not read'})[:12])
    print('articles with a copy that is counted and a copy that is not:', sum(1 for v in art.values() if len({o[8] for o in v}) == 2))
    print('largest groups of copies:', sorted(((len(v), v[0][11][:50]) for v in art.values() if len(v) > 3), reverse=True)[:6])


if __name__ == '__main__':
    main()
