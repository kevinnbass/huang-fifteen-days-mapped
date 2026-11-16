"""The interactive map of the figure "Fifteen days, mapped": one static file, built only from what this repository already publishes (the
figure's HTML, its tables, its notes and its status sentence), so the page cannot say anything the audited rows do not. No row id and no file
of a person is shown; donors and lobbyists stay counted, as in the tables.

Run from the repository: python3 scripts/build_site_nv8.py docs        (writes docs/index.html; needs Pillow for the corner map)
     A second argument also writes the same page without its outer document tags, for a host that supplies its own.
Reads: research/nv8_rows.tsv, evidence.tsv, coverage_rows.tsv, README.md, figures/nv8-fifteen-days-mapped.html and .jpg, scripts/rows_map.py and
rows_ties.py for the actors, the groups and the boxes, scripts/nv8_status.py for the kicker; the page layout is scripts/site_nv8_map_template.html.
The repository must be at a clean commit: the page prints the commit it was built from. Nothing is fetched."""
import csv, html, json, os, re, subprocess, sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = Path(os.environ['NV8_PUBLIC_CLONE']) if os.environ.get('NV8_PUBLIC_CLONE') else ROOT        # the builder's own working copy names the public clone; in the repository it is the repository
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'site' / 'nv8'
sys.path.insert(0, str(PUBLIC / 'scripts'))
import rows_map, rows_ties, nv8_status                         # the public copies, not the project's
assert Path(rows_map.__file__).parent == Path(rows_ties.__file__).parent == PUBLIC / 'scripts', 'the page must be built from the published modules'
csv.field_size_limit(10**9)
FIRST, LAST = date(2026, 10, 29), date(2026, 11, 12)
DAYS = [(FIRST + timedelta(days=i)).isoformat() for i in range((LAST - FIRST).days + 1)]
SIDE = {'anthropic': 'Anthropic and its people', 'network': 'Groups that Anthropic or Open Philanthropy has funded', 'nvidia': 'Nvidia', 'both': "Both companies' lobbying reports"}
# 'role' and 'seat' cover a post, a seat, an affiliation or a founding link: the record's own words say which and when (the twelfth reading, Nov 16, 2026: the label
# "held now" had been put on an employer a donor wrote down, a co-founding link and a company's connected PAC)
KIND = {'money': 'Money', 'grant': 'Grant award', 'role': 'Role or affiliation', 'seat': 'Seat or post', 'past': 'Former post',
        'named': 'Named to a body on a stated date; not checked since', 'act': 'Official act', 'ad': 'Named in ads it announced',
        'panel': 'Same session scheduled', 'context': 'Context, worded in the row and not drawn as a line'}


def scope(css):
    """The figure's style sheet with every rule confined to the sheet (.world): html and body become the sheet itself."""
    out = []
    for rule in css.split('}'):
        if '{' not in rule:
            assert not rule.strip(), rule[:80]
            continue
        sel, decl = rule.split('{', 1); assert '@' not in sel, sel
        sels, depth, cur = [], 0, ''
        for ch in sel:                                         # split at commas that are not inside parentheses
            depth += ch == '('; depth -= ch == ')'
            if ch == ',' and depth == 0:
                sels.append(cur); cur = ''
            else:
                cur += ch
        sels.append(cur)
        new = ['.world' if x.strip() in ('html', 'body') else '.world ' + x.strip() for x in sels]
        out.append(','.join(dict.fromkeys(new)) + '{' + decl + '}')
    return '\n'.join(out)


def thumb(jpg):
    """A small picture of the whole figure for the corner map, as a data address. The JPG is decoded at an eighth of its size."""
    import base64, io
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(jpg); w, h_ = im.size
    im.draft('RGB', (w // 8, h_ // 8)); assert im.size[0] * 8 <= w + 64 and im.size[1] * 8 <= h_ + 64 and im.size[0] * im.size[1] <= 16_000_000, im.size      # never decode the full sheet: the draft at an eighth must have taken effect
    im = im.convert('RGB'); im.thumbnail((224, 400))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=68, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def edges(fig_body, ties, lines, name_of):
    """For each tie line of the figure, in the order the page meets them: the records it stands for. A line leaves a box at its edge
    and ends at a box or at an actor's row, so its two ends are read from the figure's own numbers: the box whose edge holds each end
    point, and the row the line is marked as reaching. Returns [[tie numbers], [member-line numbers], from, to] per line."""
    flat = lambda t: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t))).strip()
    pans = re.split(r'<div class="pan" style="position:absolute;left:\d+px;top:0">', fig_body)[1:]
    groups = [g.split('</g>', 1)[0] for g in re.split(r'<g transform="translate\(\d+,0\)">', fig_body)[1:]]
    assert len(pans) == len(groups) >= 1, (len(pans), len(groups))
    box_re = re.compile(r'<div data-fit\s+style="position:absolute;left:([\d.]+)px;top:([\d.]+)px;width:([\d.]+)px;height:([\d.]+)px;[^"]*">'
                        r'<div style="font-size:[\d.]+px;font-weight:bold[^"]*">(.*?)</div>', re.S)
    edge_re = re.compile(r'<(path|line) class="e" data-a="([^"]*)"([^>]*)>')
    assert sum(len(edge_re.findall(g)) for g in groups) == len(re.findall(r'class="e"', fig_body)), 'a tie line outside the two slices'
    drawn = lambda i: ties[i]['k'] != KIND['context']
    out = []
    for pan, group in zip(pans, groups):
        boxes = [(flat(re.sub(r'<span.*?</span>', '', b[4], flags=re.S)), float(b[0]), float(b[1]), float(b[2]), float(b[3])) for b in box_re.findall(pan)]

        def at(x, y):
            hits = [(min(abs(x - bx), abs(x - bx - bw), abs(y - by), abs(y - by - bh)), n) for n, bx, by, bw, bh in boxes
                    if bx - 2 <= x <= bx + bw + 2 and by - 2 <= y <= by + bh + 2]
            return min(hits)[1] if hits else None
        for tag, key, rest in edge_re.findall(group):
            if tag == 'path':
                nums = [float(v) for v in re.findall(r'-?[\d.]+', re.search(r' d="([^"]+)"', rest).group(1))]; p0, p3 = nums[:2], nums[-2:]
            else:
                num = lambda a: float(re.search(rf' {a}="([\d.]+)"', rest).group(1)); p0, p3 = [num('x1'), num('y1')], [num('x2'), num('y2')]
            a, b, ks = at(*p0), at(*p3), key.split(); tt, ll = [], []
            if len(ks) == 2 and not (a and b):                                   # a line between two actors that both have rows
                pair = {name_of[ks[0]], name_of[ks[1]]}; tt = [i for i, t in enumerate(ties) if {t['a'], t['b']} == pair]
                a, b = (ties[tt[0]]['a'], ties[tt[0]]['b']) if tt else (a, b)
            elif a and b:
                tt = [i for i, t in enumerate(ties) if {t['a'], t['b']} == {a, b}]
            elif a and len(ks) == 1:                                             # from a box into one actor's row
                b = name_of[ks[0]]
                tt = [i for i, t in enumerate(ties) if t['a'] == a and t['b'] == b]
                ll = [i for i, l in enumerate(lines) if l['m'] == ks[0] and l.get('n') == a]
            tt = [i for i in tt if drawn(i)] or tt
            out.append([tt, ll, a or '', b or ''])
    return out


def tsv(name):
    return list(csv.DictReader(open(PUBLIC / 'research' / name, newline='', encoding='utf-8'), delimiter='\t'))


def main():
    rows = [r for r in tsv('nv8_rows.tsv') if not r['withdrawn']]
    ev = defaultdict(list)
    for e in tsv('evidence.tsv'):
        ev[e['row_id']].append(e)

    def sources(rid, passages=True):
        """The evidence lines of a row, grouped by source: [title, address or '', table in the repository or '', [passages]]."""
        out = {}
        for e in ev.get(rid, []):
            key = (e['what'], e['url'], e['copy_in_repo'] if not e['url'] else '')
            out.setdefault(key, [])
            if passages and e['kind'] == 'saved original' and e['passage'] and e['passage'] not in out[key]:
                out[key].append(e['passage'])
        return [[k[0], k[1], k[2], v] for k, v in out.items()]
    actors = [{'k': a[0], 'g': a[1], 'n': a[2], 'r': a[3] or ''} for a in rows_map.ACTORS]
    key_of = {a['n']: a['k'] for a in actors}; known = {a['k'] for a in actors}
    acts = []
    for r in rows:
        if r['table'] == 'dated act of an actor':
            assert r['actor'] in known, r['row_id']
            acts.append({'a': r['actor'], 'd': r['date'], 't': r['drawn_text'], 'rep': r['reported_by_others'] == 'True', 's': sources(r['row_id'])})
    ties = []
    for r in rows:
        if r['table'] in ('tie between two actors', 'tie in the network at left'):
            assert r['kind'] in KIND, (r['row_id'], r['kind'])
            ties.append({'a': r['a'], 'b': r['b'], 'ka': key_of.get(r['a'], ''), 'kb': key_of.get(r['b'], ''), 'k': KIND[r['kind']], 't': r['drawn_text'], 's': sources(r['row_id'])})
    # the box a member's line leaves from, where the figure draws it as a line (the published module says which)
    node = {(t['member'], t['type'], t['side']): t['node'] for t in rows_ties.ties() if t['draw'] == 'line' and t['node']}
    lines = []
    for r in rows:
        if r['table'] == 'tie of a member of Congress':
            assert r['member'] in known and r['side'] in SIDE, r['row_id']
            # a member's line is a count from a table of this repository; only the sources that are a public page are listed, without passages
            # every source of the line is listed, a table of this repository included (no passages: the line is a count); a search that found nothing is marked,
            # so that the page does not count it as a tie (the twelfth reading: 100 lines had shown no source, and 34 searches without a result were counted as ties)
            lines.append({'m': r['member'], 'side': r['side'], 't': r['drawn_text'], 's': sources(r['row_id'], passages=False),
                          'n': node.get((r['member'], r['type'], r['side']), ''), 'neg': r['drawn_text'].startswith('No ')})
    assert all(l['s'] for l in lines), [l['t'][:40] for l in lines if not l['s']][:3]
    print('member lines:', len(lines), '| searches that found nothing:', dict(Counter(l['side'] for l in lines if l['neg'])))
    by_id = {r['row_id']: r for r in rows}
    groups = [{'k': g[0], 'label': g[1], 'not_shown': g[2], 'background': by_id[g[3]]['drawn_text'] if g[3] else '', 's': sources(g[3]) if g[3] else []} for g in rows_map.GROUPS]
    assert {a['g'] for a in actors} <= {g['k'] for g in groups}
    events = [{'d': r['date'], 't': r['drawn_text'], 's': sources(r['row_id'])} for r in rows if r['table'] == 'dated event' and r['date'] in DAYS]
    cov = tsv('coverage_rows.tsv'); pieces = []
    for r in cov:
        if r['drawn'] == 'yes':
            assert r['first_listed'] in DAYS, r['row_id']
            pieces.append([DAYS.index(r['first_listed']), r['domain'], r['headline'], r['url']])
    pieces.sort(key=lambda p: (p[0], p[1], p[2]))
    undated = sum(r['drawn'] != 'yes' for r in cov)
    # the figure's own notes, as the README of the repository prints them (one paragraph each, led by a bold label)
    readme = (PUBLIC / 'README.md').read_text(encoding='utf-8')
    sec = readme.split("## The figure's own notes", 1)[1].split('\n## ', 1)[0]
    notes = [[m.group(1), m.group(2).strip()] for m in re.finditer(r'^\*\*([^*]+):\*\*\s*(.+)$', sec, re.M)]
    assert [n[0] for n in notes][:2] == ['Reading it', 'What the record does not show'] and any(n[0] == 'Status' for n in notes), [n[0] for n in notes]
    made = readme.split('## Who made this', 1)[1].strip().split('\n\n')[0].replace('\n', ' ')
    opening = readme.split('## What this is', 1)[1].strip().split('\n\n')[0].replace('\n', ' ')
    commit = subprocess.run(['git', '-C', str(PUBLIC), 'log', '-1', '--format=%h %cs'], capture_output=True, text=True, check=True).stdout.split()
    dirty = subprocess.run(['git', '-C', str(PUBLIC), 'status', '--porcelain', '--', 'research', 'figures', 'README.md', 'scripts/rows_map.py', 'scripts/rows_ties.py', 'scripts/nv8_status.py'], capture_output=True, text=True, check=True).stdout.strip()
    assert not dirty, 'the tables, the figure or the notes have uncommitted changes; the page must be built from a commit'
    commit = subprocess.run(['git', '-C', str(PUBLIC), 'log', '-1', '--format=%h %cs', '--', 'research', 'figures', 'README.md'], capture_output=True, text=True, check=True).stdout.split()      # the last commit that changed what the page is built from
    data = {'days': DAYS, 'groups': groups, 'actors': actors, 'acts': acts, 'ties': ties, 'lines': lines, 'sides': SIDE, 'events': events, 'pieces': pieces,
            'notes': notes, 'made': made, 'opening': opening, 'kicker': nv8_status.KICKER, 'commit': commit[0], 'commit_day': commit[1],
            'n': {'pieces': len(pieces), 'undated': undated, 'sites': len({p[1] for p in pieces}), 'acts': len(acts), 'actors': len(actors),
                  'members': sum(a['g'] in ('senate', 'house') for a in actors), 'ties': len(ties), 'lines': len(lines)}}
    # controls: the page's numbers are the README's
    for n_, what in ((data['n']['pieces'], 'pieces'), (data['n']['acts'], 'acts'), (data['n']['lines'], 'lines for the')):
        assert re.search(rf"\b{n_:,}\b[^.\n]{{0,40}}{what}", readme), ('a count that the README does not print', n_, what)
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    # the figure itself, as published: its HTML becomes the sheet of the map, its style sheet scoped to the sheet
    fig = (PUBLIC / 'figures' / 'nv8-fifteen-days-mapped.html').read_text(encoding='utf-8')
    assert '<script' not in fig.lower(), 'the figure is expected to carry no script'
    fig_css = re.search(r'<style>(.*?)</style>', fig, re.S).group(1); fig_body = fig.split('<body>', 1)[1].rsplit('</body>', 1)[0]
    chips = [(k, html.unescape(re.sub(r'<[^>]+>', '', t))) for k, t in re.findall(r'<div data-fit data-a="([a-z0-9]+)" class="chip"[^>]*>(.*?)</div></div>', fig_body, re.S)]
    flat = lambda t: re.sub(r'\s+', ' ', t).strip()
    # a chip is one act, or the acts of one actor on one day joined by a full stop: every chip must be made of whole acts, and of nothing else
    whole = 0
    for k, t in chips:
        mine = [flat(a['t']) for a in acts if a['a'] == k and flat(a['t']).rstrip('.') in flat(t)]
        left = flat(t)
        for m_ in sorted(mine, key=len, reverse=True):
            left = left.replace(m_.rstrip('.'), '', 1)
        whole += bool(mine) and not left.strip(' .')
    matched = whole
    ed = edges(fig_body, ties, lines, {a['k']: a['n'] for a in actors})
    data['edges'] = [[e[0], e[1], e[2], e[3]] for e in ed]
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    print(f"tie lines on the figure: {len(ed)}; with their record found: {sum(bool(e[0] or e[1]) for e in ed)} "
          f"({sum(len(e[0]) + len(e[1]) == 1 for e in ed)} with exactly one); without: {[(e[2], e[3]) for e in ed if not (e[0] or e[1])]}")
    page = (Path(__file__).with_name('site_nv8_map_template.html')).read_text(encoding='utf-8')
    for mark_ in ('__DATA__', '__FIGURE__', '__FIGSTYLE__', '__THUMB__'):
        assert page.count(mark_) == 1, mark_
    page = page.replace('__FIGSTYLE__', scope(fig_css)).replace('__FIGURE__', fig_body).replace('__THUMB__', thumb(PUBLIC / 'figures' / 'nv8-fifteen-days-mapped.jpg'))
    print(f'the figure as published: {len(fig_body):,} characters; chips on it {len(chips)}, of which {matched} are made of whole dated acts and nothing else')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'index.html').write_text(page.replace('__DATA__', blob), encoding='utf-8')
    if len(sys.argv) > 2:                                   # the same page, body only: title, one meta line, style, content, scripts
        head, rest = page.split('</head>', 1)
        title = re.search(r'<title>.*?</title>', head, re.S).group(0); style = re.search(r'<style>.*?</style>', head, re.S).group(0)
        body = rest.split('<body>', 1)[1].rsplit('</body>', 1)[0]
        Path(sys.argv[2]).write_text(title + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + style + body.replace('__DATA__', blob), encoding='utf-8')
    print(f"wrote {OUT / 'index.html'}: {len(blob):,} characters of data from commit {commit[0]}; {len(actors)} actors, {len(acts)} acts, {len(ties)} ties, "
          f"{len(lines)} member lines, {len(pieces):,} pieces ({undated} undated left out), {len(notes)} notes; private names: none are read (public tables only)")
    print('acts by day:', dict(sorted(Counter(a['d'] for a in acts).items())))


if __name__ == '__main__':
    main()
