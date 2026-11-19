"""Later versions on the tie lines: for every tie line and every page it cites, the ARTICLE's own stamps of first publication and of last change, and whether the change falls on a later U.S. Eastern day.

Run from the project root: python3 -I scripts/nv8_tie_versions.py   -> research/nv8_tie_line_versions.tsv

Why: a page saved only in a version changed after its first day may hold passages newer than that day. For chips the report-day screen decides it act by act. For tie lines nothing did, until two readings
(the thirty-sixth and thirty-seventh) each found reports quoted without that warning and the builder counted the fault over every line; the thirty-eighth reading checked this screen against the pages.

Article-level stamps only, in this order of trust:
  1. the header lines PUBLISHED / MODIFIED that the saver wrote at the top of text.txt;
  2. meta tags article:published_time / article:modified_time in body.html;
  3. a JSON-LD object in body.html whose type is an article type AND whose headline or address matches the page's own;
  4. for a page whose own data give a day of change and NO day of first publication: its one visible line "Published <Month> <day>, <year>", read as a date without a time (batch s11i: the forty-fifth
     reading found a think tank's page that the screen had passed over for want of a first day; the builder then ran the corrected screen over every cited page and found a second page of the same site).
     A cited page with a day of change and no first day that this rule cannot read stops the script.
Structured data of other articles on a page (news modules, related links) is not read: a first count that read it flagged pages that were changed on their first day only.
A stamp without a zone is used only when no zoned stamp gives the same moment, is read as UTC, and is marked. A first-publication stamp at exactly midnight UTC is a date without a time: its own date is kept.

How the figure says it (column how_the_figure_says_it), by the rule the thirty-eighth reading accepted with conditions:
  - a line that quotes or dates a report or an announcement carries the warning in its own words ("noted on the line"); the check below finds the words;
  - a line that states a standing fact from a page (a list of supporters for a stated period, a disclosure page, a profile) is listed in this table and covered by one sentence of the figure's note.
A pair that is in neither list stops this script: a new citation must be classed by a person."""
import csv, html, json, re, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo
ROOT = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ROOT / 'scripts'))
ET = ZoneInfo('America/New_York'); P = ROOT / 'research' / 'primary'
ART = {'NewsArticle', 'Article', 'BlogPosting', 'LiveBlogPosting', 'ReportageNewsArticle', 'AnalysisNewsArticle', 'OpinionNewsArticle', 'Report', 'TechArticle', 'ScholarlyArticle'}
STAMP = r'(\d{4}-\d\d-\d\dT[\d:.]+(?:Z|[+-]\d\d:?\d\d)?)'
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
day = lambda d: f"{MON[d.month - 1]} {d.day}, {d.year}"
SITE = {'csis.org': "CSIS's page", 'anthropic.com': "Anthropic's own page", 'cnbc.com': "CNBC's page", 'theregister.com': "The Register's page", 'semafor.com': "Semafor's page", 'huffpost.com': "HuffPost's page", 'fortune.com': "Fortune's page", 'siliconangle.com': "SiliconANGLE's page",
        'infosecurity-magazine.com': "Infosecurity Magazine's page", 'spotlightdelaware.org': "Spotlight Delaware's page", 'aljazeera.com': "Al Jazeera's page", 'chinatalk.media': "ChinaTalk's page", 'whbl.com': "the saved copy of the Reuters dispatch",
        'priscilachauhan.substack.com': "the essay's page", 'leverageshares.com': "the fund issuer's page", 'justdario.com': "the commentator's blog page", 'asiatimes.com': "Asia Times's page", 'nist.gov': "NIST's page", 'transformernews.ai': "Transformer's page"}        # batch s11f: an essay on export controls that MT07 cites for a letter of June 10, 2026 (its author is not named on the line)
# a standing fact of the page, not dated by the page's first publication: listed in the table, no warning on the line
STANDING = {('MT17', 'abc-anthropic-pentagon-0227'): 'the line gives the order by its month, from the report', ('MT18', 'nbc-1108-investigation'): 'the line gives the award by its month', ('MT18', 'cnbc-1111-congress-resign'): 'the line gives the flight by its month',
            ('MT25', 'art-pfa-conservative'): "the group's own page names its co-founder", ('MT43', 'art-f1-cnas-supporters'): 'a list of supporters for a stated period (Oct 2024 to Sep 2025)', ('MT44', 'art-f1-cnas-supporters'): 'a list of supporters for a stated period (Oct 2024 to Sep 2025)',
            ('MT48', 'art-f1-80k-team'): "the group's own page about its people", ('MT48', 'art-f1-80k-donors'): "the group's own page about its donors", ('MT49', 'art-f1-moor-disclosures'): "the firm's own disclosure page", ('MT56', 'art-f1-cnas-schneider'): "the institute's profile page",
            ('MT56', 'art-f1-cnas-supporters'): 'a list of supporters for a stated period (Oct 2024 to Sep 2025)', ('MT58', 'art-f1-tarbell-perlo'): "the center's own page about him"}
# warnings worded before this screen existed: the words of the line that carry them
OLD_NOTE = {('MT69', 'art-own-anthropic-series-h'): 'saved in a version modified on Sept 27 in U.S. Eastern time',
            ('MT74', 'ms-ag-amodei-statement-1021'): 'saved in a version modified on Sept 27, 2026 in U.S. Eastern time', ('MT74', 'art-own-forbesau-white-house-accord-what-it-says'): "Forbes's on Oct 2",
            ('MT74', 'art-own-siliconangle-260930-voluntary-white-house-accord'): "SiliconANGLE's on Oct 1", ('MT74', 'art-own-techstrong-voluntary-super-intelligence-accord'): "Techstrong's on Sept 30", ('MT74', 'art-own-infosecurity-trump-ai-giants-super-intelligence'): "Infosecurity Magazine's on Nov 16",
            ('MT76', 'art-own-spotlightdelaware-1102-openai-probe'): 'in a page changed on Nov 8', ('MT76', 'art-own-techcrunch-261009-anthropic-agents-evals-cut-off'): 'its page was changed on Oct 12',
            ('MT76', 'art-own-anthropic-investigating-incidents-cybersecurity-evals'): 'the three company pages are saved in versions their own data mark as modified on Nov 13, 2026', ('MT76', 'art-own-anthropic-alignment-assessment-cybersecurity-incidents'): 'the three company pages are saved in versions their own data mark as modified on Nov 13, 2026',
            ('MT76', 'art-own-anthropic-improving-alignment-security-efforts'): 'the three company pages are saved in versions their own data mark as modified on Nov 13, 2026'}
norm = lambda s: re.sub(r'[^a-z0-9]+', ' ', html.unescape(s or '').lower()).strip()


def parse(v):
    v = v.strip().replace('Z', '+00:00'); v = re.sub(r'([+-]\d\d)(\d\d)$', r'\1:\2', v)
    try: t = datetime.fromisoformat(v)
    except ValueError: return None, False
    return (t, False) if t.tzinfo else (t.replace(tzinfo=timezone.utc), True)


def stamps(page):
    """{'pub': [(time, where, zoneless)], 'mod': [...]}, the page's address, and its header lines as written."""
    d = P / page; out = {'pub': [], 'mod': []}; title = url = ''; lines = {}
    f = d / 'text.txt'
    if f.exists():
        head = f.read_text(errors='replace')[:900]
        m = re.search(r'^URL:\s*(\S+)', head, re.M); url = m.group(1) if m else ''
        m = re.search(r'^TITLE:\s*(.+)$', head, re.M); title = m.group(1) if m else ''
        for m in re.finditer(r'^(PUBLISHED|MODIFIED):\s*' + STAMP + r'\s*$', head, re.M):
            t, nz = parse(m.group(2))
            if t: out['pub' if m.group(1) == 'PUBLISHED' else 'mod'].append((t, "the saver's header line", nz)); lines[m.group(1)] = m.group(0).strip()
    b = d / 'body.html'
    if b.exists():
        s = b.read_text(errors='replace')
        for k, v in re.findall(r'<meta[^>]+property=["\']article:(published_time|modified_time)["\'][^>]+content=["\']' + STAMP, s):
            t, nz = parse(v)
            if t: out['pub' if k == 'published_time' else 'mod'].append((t, "the page's article meta tag", nz))
        for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', s, re.S):
            try: j = json.loads(m.group(1))
            except Exception: continue
            for o in (j if isinstance(j, list) else j.get('@graph', [j]) if isinstance(j, dict) else []):
                if not isinstance(o, dict): continue
                ty = o.get('@type'); ty = set(ty) if isinstance(ty, list) else {ty}
                if not (ty & ART): continue
                hl = norm(str(o.get('headline') or o.get('name') or '')); me = o.get('mainEntityOfPage'); ou = str(o.get('url') or (me.get('@id', '') if isinstance(me, dict) else me or ''))
                same = (hl and title and (hl[:40] in norm(title) or norm(title)[:40] in hl)) or (ou and url and urlparse(ou).path.rstrip('/') == urlparse(url).path.rstrip('/'))
                if not same: continue
                for key, k in (('datePublished', 'pub'), ('dateModified', 'mod')):
                    if isinstance(o.get(key), str) and re.fullmatch(STAMP, o[key].strip()):
                        t, nz = parse(o[key])
                        if t: out[k].append((t, "the article's own structured data", nz))
        if out['mod'] and not out['pub']:        # rule 4
            vis = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', s)))
            ds = {datetime.strptime(' '.join(m), '%B %d %Y').replace(tzinfo=timezone.utc) for m in re.findall(r'\bPublished\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})', vis)}
            if len(ds) == 1: out['pub'].append((ds.pop(), "the page's visible line 'Published ...' (a date without a time)", False))
    return out, url, lines


def pick(c, first):
    """The earliest first-publication stamp (the latest change stamp); among stamps of the same moment a zoned one is preferred."""
    t = (min if first else max)(x[0] for x in c); same = [x for x in c if x[0] == t]; z = [x for x in same if not x[2]] or same
    return t, z[0][1] + (' (no zone given; read as UTC)' if z[0][2] else '')


def screen():
    import rows_map
    rows = [r for r in rows_map.rows() if r['row_id'].startswith('MT') and not r.get('withdrawn')]; cache = {}; table = []
    for r in rows:
        words = r.get('label') or r.get('what') or ''
        for page in dict.fromkeys(r['src']):
            if page not in cache: cache[page] = stamps(page)
            st, url, lines = cache[page]
            assert st['pub'] or not st['mod'], ('a cited page gives a day of change and no day of first publication that the screen can read: read the page and class it', r['row_id'], page)
            if not st['pub'] or not st['mod']: continue
            (pub, wp), (mod, wm) = pick(st['pub'], True), pick(st['mod'], False)
            midnight = (pub.astimezone(timezone.utc).hour, pub.astimezone(timezone.utc).minute, pub.astimezone(timezone.utc).second) == (0, 0, 0)
            dp = pub.astimezone(timezone.utc).date() if midnight else pub.astimezone(ET).date(); dm = mod.astimezone(ET).date()
            if dm > dp: table.append({'row': r, 'words': words, 'page': page, 'url': url, 'site': urlparse(url).netloc.replace('www.', ''), 'pub': pub, 'mod': mod, 'dp': dp, 'dm': dm, 'wp': wp + ('; midnight UTC, read as a date' if midnight else ''), 'wm': wm, 'lines': lines})
    return rows, cache, table


def item(t):
    """The words by which a line names one such page in its warning."""
    return f"{SITE[t['site']]} of {day(t['dp'])} (changed {day(t['dm'])})"


def main():
    rows, cache, table = screen(); out = []
    got = {(t['row']['row_id'], t['page']) for t in table}
    # controls: the four reports two readings named are found; a live page changed only on its first day is not
    for pg in ('art-own-forbesau-white-house-accord-what-it-says', 'art-own-siliconangle-260930-voluntary-white-house-accord', 'art-own-techstrong-voluntary-super-intelligence-accord', 'art-own-infosecurity-trump-ai-giants-super-intelligence'): assert ('MT74', pg) in got, pg
    assert ('MT74', 'art-own-cnbc-261026-anthropic-ipo-live-updates') not in got, 'the control page that was changed on its first day only is flagged'
    assert ('MT57', 'ms-sg2-officials-50e663') in got and ('MT72', 'ms-ag-csis-commerce-anthropic') in got, 'the two pages with a visible first day only (rule 4) are not found'
    assert not (set(STANDING) - got) and not (set(OLD_NOTE) - got), ('a classed pair is no longer in the screen', set(STANDING) - got, set(OLD_NOTE) - got)
    for t in table:
        k = (t['row']['row_id'], t['page'])
        if k in STANDING: how = 'a standing fact of the page, listed here: ' + STANDING[k]
        elif k in OLD_NOTE: assert OLD_NOTE[k] in t['words'], ('the warning is not in the line', k); how = 'noted on the line'
        else: assert t['site'] in SITE and item(t) in t['words'], ('no warning on the line for this page, and it is not classed as a standing fact', k, item(t) if t['site'] in SITE else t['site']); how = 'noted on the line'
        out.append([t['row']['row_id'], t['page'], t['url'], t['pub'].isoformat(), t['mod'].isoformat(), t['dp'].isoformat(), t['dm'].isoformat(), t['wp'], t['wm'], how])
    with open(ROOT / 'research' / 'nv8_tie_line_versions.tsv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['row_id', 'page', 'address',          # the two parties of a line are in research/nv8_rows.tsv under its row id; they are not repeated here
                     'first_published', 'last_changed', 'first_published_day', 'last_changed_eastern_day', 'where_the_first_stamp_was_read', 'where_the_change_stamp_was_read', 'how_the_figure_says_it']); w.writerows(out)
    c = Counter(o[9].split(':')[0].split(',')[0] for o in out)
    print(f"tie lines {len(rows)} | pages they cite {len(cache)} | with both stamps at article level {sum(1 for v in cache.values() if v[0]['pub'] and v[0]['mod'])} | citations to a page changed on a later day than its first: {len(out)} on {len({o[0] for o in out})} lines, {len({o[1] for o in out})} pages | "
          f"noted on the line {c['noted on the line']} on {len({o[0] for o in out if o[9] == 'noted on the line'})} lines | standing facts listed {c['a standing fact of the page']} on {len({o[0] for o in out if o[9] != 'noted on the line'})} lines | controls: four known reports found, a same-day live page not flagged, two pages with a visible first day only found")


if __name__ == '__main__':
    main()
