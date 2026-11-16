"""One line per saved news page with the article it is a copy of, so that a count of "pages" counts each article once.

Run: nice python3 -I scripts/nv8_articles.py   -> research/nv8_articles.tsv, and a summary
Pages: the 1,086 of the first census (scripts/member_mentions.pages) and the pages saved since (the list of lane remarks_nv8_e).
Two pages are the same article only on proof: the same address (a site's AMP address counts as the same); or text, by seven-word runs
with each site's furniture left out: at least 80% of the shorter page's runs occur in the longer, the shorter has at least 150 and is at
least half the longer's length, and neither page is a post; or a reader's verdict on the pair (research/nv8_article_pairs.tsv), which
overrides the rule either way. Anything less keeps both (Kevin, 2026-11-15:
"count them for everyone. don't use duplicates. deduplicate. don't add the pieces dates 13 and 14."). A page of either set is not counted when its
own stamp, read as a U.S. Eastern day, is after Nov 12, 2026 (a republished copy stamped later is counted only through a counted copy of
the same article) or before Oct 29, 2026 (a background page: an earlier article, a biography, a statement of 2025); a page saved since the census is also not counted when it has no article text or is not a news piece (a reference
page, a company's own site, an image). The day of a page is read by scripts/nv8_page_dates.py (the header stamp, or the page's own address or
stamp line where the header has none); a page whose day cannot be read is counted. Controls: two pairs known to be copies of one article must be joined, and two different articles must not be."""
import csv, html, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import member_mentions as M
import nv8_page_dates as D
ROOT = Path(__file__).resolve().parent.parent; R = ROOT / 'research'; P = R / 'primary'
LANE = Path('lanes/remarks_nv8_e')
FIRST, LAST = '2026-10-29', '2026-11-12'
NOT_NEWS = ('wikipedia.org', 'pbs.twimg.com')       # a company's home page that carries a dated statement is counted like its newsroom pages (the eighth reading)
# first-census pages that are reference pages, read on Nov 15, 2026: a fellow's profile at a think tank, an organisation chart
REFERENCE = {'hoover-chhabra', 'theorg-heck'}
# the census reader's note says the saved copy is not the piece: a block, error or ad-blocker page, or other content saved in its place.
# A copy that holds part of the piece (a headline and description, a teaser, an excerpt, readers' comments under a story) is counted.
NOT_THE_PIECE = re.compile(r'\b403\b|\b404\b|Access Denied|Ad-blocker wall|unrelated headline|instead of the article', re.I)


def runs(text):
    body = text.split('\n\n', 1)[1] if '\n\n' in text[:1500] else text
    w = re.findall(r"[a-z0-9']+", body.lower().replace('’', "'"))
    return {hash(' '.join(w[i:i + 7])) for i in range(len(w) - 6)}


def opening(text, n):
    """The seven-word runs among the first n words of a page's body: its lead."""
    body = text.split('\n\n', 1)[1] if '\n\n' in text[:1500] else text
    w = re.findall(r"[a-z0-9']+", body.lower().replace('’', "'"))[:n]
    return {hash(' '.join(w[i:i + 7])) for i in range(len(w) - 6)}


def main():
    pages = []                                                    # (id, set, text)
    for pid, text in M.pages():
        pages.append((pid, 'first census', text))
    first = len(pages)
    # what the readers of the census could not read, for every page (lanes a to d read the first census, e the pages saved since)
    gaps = {}
    for t_ in 'abcdefg':               # f read the recovered pages and two saved since: its gaps are what is still missing of those; g read the 54 pages saved on Nov 16
        if not (LANE.parent / f'remarks_nv8_{t_}' / 'done' / 'DONE').exists():
            continue
        for r in csv.DictReader(open(LANE.parent / f'remarks_nv8_{t_}' / 'out' / 'gaps.csv', newline='')):
            gaps[r['page_id']] = r['what_failed']
    gaps_f = {r['page_id'] for r in csv.DictReader(open(LANE.parent / 'remarks_nv8_f' / 'out' / 'gaps.csv', newline=''))}
    # A second net for pages held only in part (after the eleventh reading, Nov 16, 2026, which found a subscription preview that no census reader had listed):
    # every counted page that shows a sign of a barrier, or whose text is short, was read for whether the saved copy holds the whole piece
    # (scripts/nv8_partial_screen.py lists them; research/nv8_pages_in_part_read.tsv holds the reader's verdicts).
    _pr = R / 'nv8_pages_in_part_read.tsv'
    part_read = {r['page_id'] for r in csv.DictReader(open(_pr, newline=''), delimiter='\t') if r['verdict'] == 'part'} if _pr.exists() else set()
    for r in csv.DictReader(open(LANE / 'pages.tsv', newline=''), delimiter='\t'):
        pages.append((r['page_id'], 'saved since', M.saved_since_text(r['page_id'])))
    # pages saved after that list was closed (research/nv8_pages_added.tsv says why each was saved); counted by the same rules
    for r in csv.DictReader(open(R / 'nv8_pages_added.tsv', newline=''), delimiter='\t'):
        pages.append((r['page_id'], 'saved since', M.saved_since_text(r['page_id'])))
    recovered = {pid for pid, _, _ in pages if (M.P / pid / 'text.recovered.txt').exists()}
    info = {pid: D.meta(pid) for pid, _, _ in pages}
    host = lambda u: re.sub(r'^www\.', '', re.sub(r'^https?://', '', u).split('/')[0].lower())
    def key(u):
        u = re.sub(r'^https?://(www\.|amp\.|m\.)?', '', u.split('?')[0].split('#')[0]).rstrip('/').lower()
        return re.sub(r'/amp$', '', u.replace('/amp/', '/'))                 # a site's AMP address is the same article
    is_post = lambda pid: host(info[pid][0]) in ('x.com', 'twitter.com')
    RAW = {pid: runs(text) for pid, _, text in pages}
    LEAD = {pid: opening(text, 120) for pid, _, text in pages}
    # the headline of a page, as words, without the site's name after a bar or dash
    tw = {pid: frozenset(re.findall(r"[a-z0-9']+", html.unescape(re.split(r'\s[|–—-]\s', info[pid][1])[0]).lower().replace('’', "'"))) for pid, _, _ in pages}
    alike_title = lambda a, b: bool(tw[a]) and bool(tw[b]) and len(tw[a] & tw[b]) / len(tw[a] | tw[b]) >= 0.8
    # site furniture: a seven-word run found on two pages of one site that carry different headlines (navigation, related links, a
    # subscription offer, a standing background paragraph) says nothing about whether two pages are one article, and is left out
    by_site = defaultdict(list)
    for pid, _, _ in pages:
        by_site[host(info[pid][0])].append(pid)
    S = {}
    for site, ids in by_site.items():
        if not site or len(ids) < 2:
            for pid in ids:
                S[pid] = RAW[pid]
            continue
        where = defaultdict(list)
        for pid in ids:
            for h in RAW[pid]:
                where[h].append(pid)
        furniture = {h for h, ps in where.items() if len(ps) > 1 and any(not alike_title(ps[0], q) for q in ps[1:])}
        for pid in ids:
            S[pid] = RAW[pid] - furniture
    parent = {pid: pid for pid, _, _ in pages}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    edges = {}                                                    # (a, b) -> why they are one article
    by_key = defaultdict(list)
    for pid, _, _ in pages:
        if info[pid][0]:
            by_key[key(info[pid][0])].append(pid)
    # a page saved by hand prints its address in the margin, and a long address loses its end there (two different Journal newsletters
    # printed one address, Nov 16, 2026): two hand-saved pages with one printed address are joined on it only if their headlines are
    # alike too; else a reader says. A fetched page's address is whole, so a hand-saved page that prints the same one is the same page.
    cut_address = []
    for ids in by_key.values():
        for j, b in enumerate(ids[1:], 1):
            for a in ids[:j]:
                if a.startswith('man-') and b.startswith('man-') and not alike_title(a, b):
                    cut_address.append((a, b)); continue
                edges[(a, b)] = f'same address as {a}'; break

    def pairs_sharing(sets, least):
        idx = defaultdict(list)
        for pid, s in sets.items():
            if len(s) >= least:
                for h in s:
                    idx[h].append(pid)
        share = Counter()
        for ids in idx.values():
            if 1 < len(ids) <= 40:                                # a run on more than 40 pages is boilerplate
                for i, a in enumerate(ids):
                    for b in ids[i + 1:]:
                        share[(a, b)] += 1
        return share
    # the text rule (after the reading of Nov 15, 2026, which found that the first rule joined a memo to the articles quoting it and pages
    # of one site through their navigation): neither page is a post; furniture left out; at least 80% of the shorter page's runs are in
    # the longer; and the shorter is at least half the longer's length, so that a page quoted inside another is not taken for a copy of it
    for (a, b), n in pairs_sharing(S, 150).items():
        if is_post(a) or is_post(b) or (a, b) in edges or (b, a) in edges:
            continue
        small, big = sorted((len(S[a]), len(S[b])))
        c = len(S[a] & S[b]) / small
        # and the two share their lead: a later dispatch that puts a new lead above a retained earlier one is a new report (the eighth
        # reading, Nov 16, 2026: one test for a later version), so the two must share eight seven-word runs within their opening 120 words
        same_lead = len(LEAD[a] & LEAD[b]) >= 8
        if c >= 0.80 and small / big >= 0.5 and same_lead:
            edges[(a, b)] = f'text of the shorter is {c:.0%} inside the other ({a}), which is under twice its length, and the two share their lead'
    # identity by reading: research/nv8_article_pairs.tsv holds each pair a reader opened and judged; a verdict there overrides the rule
    read = {}
    pr = R / 'nv8_article_pairs.tsv'
    if pr.exists():
        for r in csv.DictReader(open(pr, newline=''), delimiter='\t'):
            if r['scope'] == 'all':
                read[frozenset((r['page_a'], r['page_b']))] = (r['verdict'], r['read_by'])
    known = {pid for pid, _, _ in pages}
    for k_ in list(edges):
        v = read.get(frozenset(k_))
        if v and v[0] == 'different':
            del edges[k_]
    for pair, (v, by) in read.items():
        a, b = sorted(pair)
        if v == 'same' and a in known and b in known and (a, b) not in edges and (b, a) not in edges:
            edges[(a, b)] = f'read as the same article as {a} by {by}'
    why = {}
    for (a, b), reason in edges.items():
        if find(a) != find(b):
            parent[find(b)] = find(a)
        why.setdefault(b, reason)
    # no pair read as different may end in one article through other pages
    clash = [sorted(pair) for pair, (v, _) in read.items() if v == 'different' and len(pair) == 2 and all(x in known for x in pair) and len({find(x) for x in pair}) == 1]
    if clash:                      # say which joins tie them, so the pair can be read
        for x, y in clash[:3]:
            grp = [(a_, b_, r_[:70]) for (a_, b_), r_ in edges.items() if find(a_) == find(x)]
            print('CLASH', x, y, '| joins in their group:', grp)
    assert not clash, ('two pages read as different articles are joined through others', clash[:5])
    # pairs that look alike and are not joined: listed for a reader (held with the project: it carries headlines)
    alike = []; listed = set()
    # the screen (widened on Nov 16, 2026, after the eighth reading found three wire copies it had missed: copies with house edits, trims
    # and added paragraphs share far less than half): any two counted-size pages that share 25 or more seven-word runs making up a fifth
    # of the shorter, with each site's furniture left out. Most such pairs are different articles that quote one statement; a reader says.
    tally = Counter()
    for (a, b), n in pairs_sharing(S, 30).items():
        if find(a) == find(b) or frozenset((a, b)) in read:
            continue
        c = n / min(len(S[a]), len(S[b]))
        for lim in (0.5, 0.35, 0.2, 0.1):
            tally[lim] += n >= 25 and c >= lim
        if n >= 25 and c >= 0.20:
            alike.append([a, b, f'{c:.2f}', 'text alike']); listed.add(frozenset((a, b)))
    print('unread pairs sharing 25+ runs, by share of the shorter:', dict(tally))
    for site, ids in by_site.items():
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                if site and alike_title(a, b) and find(a) != find(b) and frozenset((a, b)) not in read and frozenset((a, b)) not in listed:
                    alike.append([a, b, '', 'same site, same headline'])
    for a, b in cut_address:
        if find(a) != find(b) and frozenset((a, b)) not in read and frozenset((a, b)) not in listed:
            alike.append([a, b, '', 'same printed address, different headlines (both saved by hand)']); listed.add(frozenset((a, b)))
    print('address joins not made (two hand-saved pages, one printed address, different headlines):', len(cut_address), cut_address)
    with open(R / 'nv8_article_pairs_to_read.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['page_a', 'page_b', 'share_of_shorter', 'why_listed', 'state', 'title_a', 'title_b'])
        for (a, b), reason in edges.items():
            if frozenset((a, b)) not in read:
                w.writerow([a, b, '', reason[:60], 'joined by the rule, not yet read', info[a][1], info[b][1]])
        for a, b, c, wl in alike:
            w.writerow([a, b, c, wl, 'not joined, not yet read', info[a][1], info[b][1]])
    print('join edges:', len(edges), dict(Counter(' '.join(r.split(' ')[:2]) for r in edges.values())), '| pairs read:', len(read), '| alike and not joined, to read:', len(alike))
    same = lambda a, b: find(a) == find(b)
    assert same('man-923fe8754943', 'art-fc-itiger-wsj-1030') and same('art-fc-cnn-1112', 'art-fc-rec-ktvz-cnn-1112'), 'control: two copies of one article were not joined'
    assert not same('man-nyt-1029-01', 'man-nyt-1106-01') and not same('sw-nvidianewsnvidiacom-03', 'sw-abcnetau-01') and not same('sw-cbsnewscom-02', 'sw-cbsnewscom-11'), 'control: two different articles were joined'
    order = {}; out = []; n_art = 0
    for pid, which, text in pages:
        root = find(pid)
        if root not in order:
            n_art += 1; order[root] = f'A{n_art:04d}'
        url, title, given = info[pid]
        pub, basis, read_from = D.day_of(pid, url, title, given)
        counted, reason = 'yes', ''
        # ONE RULE FOR BOTH SETS OF PAGES (Nov 15, 2026; until then the two tests below were applied only to the pages saved since)
        if any(x in host(url) for x in NOT_NEWS) or pid in REFERENCE:
            counted, reason = 'no', 'not a news piece (a reference page, a company site or an image)'
        elif pub not in ('', '?') and pub > LAST:
            counted, reason = 'no', f'dated {pub} (U.S. Eastern), after the fifteen days'
        elif pub not in ('', '?') and pub < FIRST:
            counted, reason = 'no', f'dated {pub}, before the fifteen days (a background page)'
        elif pid in gaps and NOT_THE_PIECE.search(gaps[pid]) and pid not in recovered:
            # the reader's note describes the first extraction; a page whose article was then found in the saved HTML (scripts/recover_bodies.py) is counted
            counted, reason = 'no', 'the saved copy is a block or error page, or another page in its place (see the census gaps)'
        elif not RAW[pid] and not (title or '').strip():
            counted, reason = 'no', 'an empty capture: the saved copy holds no text and no headline'
        part = 'yes' if counted == 'yes' and ((pid in gaps and (pid not in recovered or pid in gaps_f)) or pid in part_read) else ''          # counted, and the census reader listed what of it could not be read (for a recovered page: the reader of the recovered text), or the second reader found the copy a preview
        out.append([pid, which, order[root], host(url), pub, basis, read_from[:60], len(text), counted, reason, why.get(pid, ''), title, part])
    with open(R / 'nv8_articles.tsv', 'w', newline='') as f:           # published with the figure: no headline, no text
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['page_id', 'set', 'article_id', 'site', 'day', 'day_basis', 'day_read_from', 'chars', 'counted', 'why_not', 'joined_on', 'saved_in_part']); w.writerows(o[:11] + [o[12]] for o in out)
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
