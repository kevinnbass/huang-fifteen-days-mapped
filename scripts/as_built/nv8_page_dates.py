"""The day of a saved news page, read from the page itself, with the words it was read from.

Used by scripts/nv8_articles.py so that a piece dated after Nov 12, 2026 is not counted (Kevin, 2026-11-15: "don't add the pieces
dates 13 and 14"). Rules, in order; the first that applies gives the day, and the basis names it:
  read by hand a day read in the page and entered below with the words it was read from;
  read in the saved copy
               a page whose metadata and text carry no stamp: the day read in its saved HTML or PDF (the date under the headline, the
               publication time in the page's data), listed with the exact words in research/nv8_page_days_read.tsv;
  post         a post on X: the stamp in its saved record, as a U.S. Eastern day;
  yesterday, hours ago
               a hand-saved FT page prints "Published YESTERDAY" or "Published 17 HOURS AGO" beside the browser's print time
               (this computer's clock, U.S. Central): the day that works out to, U.S. Eastern;
  stamp line   what the page itself prints. A hand-saved page (a PDF printed from the publisher's site) is read from the stamps near its
               top, before its header: "Published NOV 12 2026", "Nov. 12, 2026", "Updated Nov. 13, 2026 11 01 am ET". A fetched page
               with no stamp in its metadata is read from a stamp that follows Published, Updated or Posted in its text.
               ONE POLICY FOR ALL PAGES: the day of first publication where the page shows one; where it shows only "Updated", the day
               of the version saved (so an article shown only as updated after Nov 12 is not counted, whenever it first ran);
  header stamp the publication stamp the page's own metadata carries, as a U.S. Eastern day where it has a time and an offset;
  address      the page's address carries its day (/2026/11/13/, /20250227_);
  page time    a licensed partner's copy carries one time of its own (its zone is not stated; the day is taken as given);
  title        an official transcript whose title carries its day;
  none         no day could be read: the page stays undated (and is counted).
The first date found in the text of a fetched web page is not used: it is often a banner or another article's teaser."""
import json, re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT = Path(__file__).resolve().parent.parent; R = ROOT / 'research'; P = R / 'primary'
ET = ZoneInfo('America/New_York')
MON = {m: i for i, m in enumerate(('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'), 1)}


def eastern_day(s):
    """The U.S. Eastern calendar day of a publication stamp as a page gives it: converted when the stamp carries a time and an offset,
    the day as given when it does not; '' when there is no stamp, '?' when one is there and cannot be read."""
    s = (s or '').strip()
    if not s:
        return ''
    try:
        d = datetime.fromisoformat(s.replace('Z', '+00:00'))
        return (d.astimezone(ET) if d.tzinfo else d).date().isoformat()
    except ValueError:
        pass
    m = re.fullmatch(r'(20\d\d)(\d\d)(\d\d)', s)
    if m:
        return '-'.join(m.groups())
    m = re.search(r'\b([A-Za-z]{3})[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d\d)', s)
    if m and m.group(1).lower() in MON:
        y, mo, da = int(m.group(3)), MON[m.group(1).lower()], int(m.group(2))
    else:
        m = re.search(r'\b(\d{1,2})\s+([A-Za-z]{3})[a-z]*\.?,?\s+(20\d\d)', s)
        if not (m and m.group(2).lower() in MON):
            return '?'
        y, mo, da = int(m.group(3)), MON[m.group(2).lower()], int(m.group(1))
    tm = re.search(r'\b(\d{1,2}):(\d\d)(?::\d\d)?\s*([+-])(\d\d):?(\d\d)\b', s[m.end():])
    if tm:
        off = timedelta(hours=int(tm.group(4)), minutes=int(tm.group(5))) * (1 if tm.group(3) == '+' else -1)
        return datetime(y, mo, da, int(tm.group(1)), int(tm.group(2)), tzinfo=timezone(off)).astimezone(ET).date().isoformat()
    return f'{y:04d}-{mo:02d}-{da:02d}'


assert eastern_day('2026-11-13T02:48:24.000+09:00') == '2026-11-12' and eastern_day('Nov 12th 2026') == '2026-11-12' and eastern_day('Nov. 6, 2026 16:03') == '2026-11-06'
assert eastern_day('Thu, 12 Nov 2026 16:40:00 +02:00') == '2026-11-12' and eastern_day('20261110') == '2026-11-10' and eastern_day('2026-11-14T18:30:00-0500') == '2026-11-14'
assert eastern_day('2026-11-13T03:10:00+00:00') == '2026-11-12' and eastern_day('') == '' and eastern_day('yesterday') == '?'


def meta(pid):
    try:
        m = json.loads((P / pid / 'meta.json').read_text())
    except Exception:
        m = {}
    head = {}
    f = P / pid / 'text.txt'
    if f.exists():
        for l in f.read_text(errors='replace').splitlines()[:14]:
            k, _, v = l.partition(':')
            if k in ('URL', 'TITLE', 'PUBLISHED', 'OUTLET') and v.strip():
                head[k] = v.strip()
    url = (m.get('url') if isinstance(m, dict) else '') or head.get('URL', '')
    title = head.get('TITLE') or head.get('OUTLET', '')          # a hand-saved PDF carries its title in the second field
    return url, title[:110], head.get('PUBLISHED') or ''



MONTHS = 'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December'
STAMP = re.compile(rf"(?:(Published|Updated)\s+)?\b((?:{MONTHS})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+20\d\d)", re.I)
PRINTED = re.compile(r'\b(\d{1,2})/(\d{1,2})/(\d\d), (\d{1,2}):(\d\d)\b')
CENTRAL = ZoneInfo('America/Chicago')
# read by hand on 2026-11-15, each with the words on the page
HAND = {
 'art-fc-spf-1030': ('2026-10-30', 'MINISTRY OF HOME AFFAIRS 30 October 2026 @ 11:13 PM'),
 'art-fc-rec-miti-1113': ('2026-11-13', '13 November 2026'),
 'mha-clarification-a': ('2026-10-31', 'Clarification Statement on Wall Street Journal’s Article 31 October 2026'),      # the page's own label; the statement's timing is on the chip
}
# read on 2026-11-15 in the saved copy of each first-census page whose metadata and text carry no stamp (the seventh reading found readable
# dates on pages listed as undated): research/nv8_page_days_read.tsv gives the day, the exact words and where they stand
HAND_READ = {}
_hr = P.parent / 'nv8_page_days_read.tsv'
if _hr.exists():
    import csv as _csv
    for _r in _csv.DictReader(open(_hr, newline='', encoding='utf-8'), delimiter='\t'):
        assert _r['page_id'] not in HAND, _r['page_id']
        HAND_READ[_r['page_id']] = (_r['day'], _r['words_read'])
flat = lambda s: re.sub(r'\s+', ' ', s)


STAMPS = re.compile(rf"(?:\b(Published On|Published|Updated|Posted)\b:?\s+)?\b((?:{MONTHS})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+20\d\d|\d{{1,2}}\s+(?:{MONTHS})\.?,?\s+20\d\d)((?:[ ,]+(?:at\s+)?\d{{1,2}}[: ]\d\d\s*(?:[ap]\.?m\.?)?)?(?:\s*(?:E[SD]?T|IST|UTC|GMT))?)", re.I)
ZONES = {'ist': timedelta(hours=5, minutes=30), 'utc': timedelta(0), 'gmt': timedelta(0)}


def stamp_day(m):
    """The U.S. Eastern day of one stamp: converted where it carries a time and a zone this table knows (IST, UTC); as given otherwise
    (a stamp in Eastern time, or with no time or zone)."""
    d = eastern_day(m.group(2))
    tz = re.search(r'(\d{1,2})[: ](\d\d)\s*([ap])?\.?m?\.?\s*(IST|UTC|GMT)\b', m.group(3) or '', re.I)
    if d in ('', '?') or not tz:
        return d
    h = int(tz.group(1)) % 12 + (12 if (tz.group(3) or '').lower() == 'p' else 0) if tz.group(3) else int(tz.group(1))
    y, mo, da = map(int, d.split('-'))
    return datetime(y, mo, da, h, int(tz.group(2)), tzinfo=timezone(ZONES[tz.group(4).lower()])).astimezone(ET).date().isoformat()


def printed_day(head, keyword_only):
    """(day, words) from the stamps a page prints near its top. The day of first publication where the page shows one ("Published ...", or a
    plain date line that comes before any "Updated"); the day of the version saved where it shows only "Updated ...". With keyword_only
    (a fetched web page, where a bare date is often a banner or a teaser) only a stamp that follows Published, Updated or Posted counts."""
    ms = [m for m in STAMPS.finditer(head) if stamp_day(m) not in ('', '?') and (m.group(1) or not keyword_only)]
    if not ms:
        return '', '', False
    pub = [m for m in ms if (m.group(1) or '').lower().startswith(('published', 'posted'))]
    first = ms[0]
    pick = pub[0] if pub else first
    return stamp_day(pick), flat(pick.group(0)), bool(pick.group(1))


def day_of(pid, url, title, given):
    """(day, basis, the words it was read from). One rule for every page (reading of Nov 15, 2026, lane audit_nv8_s8a): the day of first
    publication where the page shows one, else the day of the version saved. A hand-saved page is read from what it prints, before its
    header (the header of a hand-saved page was typed from a list and was a day off for nine pages)."""
    f = P / pid / 'text.txt'
    if not f.exists():
        f = P / pid / 'text.reextract.txt'
    whole = f.read_text(errors='replace') if f.exists() else ''
    body = whole.split('\n\n', 1)[1] if '\n\n' in whole[:1500] else whole
    if pid in HAND:
        b = P / pid / 'body.html'
        assert flat(HAND[pid][1]) in flat(whole) or (b.exists() and flat(HAND[pid][1]) in flat(re.sub(r'<[^>]+>', ' ', b.read_text(errors='replace')))), pid
        return HAND[pid][0], 'read by hand', HAND[pid][1]
    if pid in HAND_READ:
        b = P / pid / 'body.html'
        raw_ = b.read_bytes() if b.exists() else b''
        if raw_[:2] == b'\x1f\x8b':                       # a body stored compressed
            import gzip
            raw_ = gzip.decompress(raw_)
        assert flat(HAND_READ[pid][1]) in flat(whole) or flat(HAND_READ[pid][1]) in flat(raw_.decode('utf-8', 'replace')), pid
        return HAND_READ[pid][0], 'read in the saved copy', HAND_READ[pid][1]
    if 'x.com/' in (url or ''):
        m = re.search(r'"created_at":\s*"([^"]+)"', whole)
        if m:
            return datetime.strptime(m.group(1), '%a %b %d %H:%M:%S %z %Y').astimezone(ET).date().isoformat(), 'post', m.group(1)
    addr = re.search(r'/(20\d\d)/(\d\d)/(\d\d)/|/(20\d\d)(\d\d)(\d\d)_', url or '')
    if pid.startswith('man-'):
        head = flat(body[:3500]); pr = PRINTED.search(head)
        m = re.search(r'Published (YESTERDAY|(\d{1,2}) HOURS? AGO)', head)
        if m and pr:
            when = datetime(2000 + int(pr.group(3)), int(pr.group(1)), int(pr.group(2)), int(pr.group(4)), int(pr.group(5)), tzinfo=CENTRAL)
            if m.group(2):
                return (when - timedelta(hours=int(m.group(2)))).astimezone(ET).date().isoformat(), 'hours ago', f'{m.group(0)}; printed {pr.group(0)}'
            return (when.date() - timedelta(days=1)).isoformat(), 'yesterday', f'{m.group(0)}; printed {pr.group(0)}'
        d, words, keyed = printed_day(head, keyword_only=False)
        known = eastern_day(given) if given.strip() else ('-'.join(x for x in addr.groups() if x) if addr else '')
        near = known in ('', '?') or abs((date.fromisoformat(d) - date.fromisoformat(known)).days) <= 2 if d else False
        if d and (keyed or near):        # a bare date far from the page's header or address is something else (a photo caption gave Oct 21 for one page)
            return d, 'stamp line', words
    if given.strip():
        d = eastern_day(given)
        if d != '?':
            return d, 'header stamp', given
    if addr:
        return '-'.join(x for x in addr.groups() if x), 'address', addr.group(0)
    b = P / pid / 'body.html'
    if b.exists() and re.search(r'itiger\.com|webull\.com', url or ''):
        tt = b.read_text(errors='replace')
        ms = sorted(set(re.findall(r'20\d\d-\d\d-\d\d \d\d:\d\d', tt)))
        if len(ms) == 1:
            return ms[0][:10], 'page time', ms[0]
        ms = sorted(set(re.findall(r'"newsTime":(\d{13})', tt)))
        if len(ms) == 1:
            return datetime.fromtimestamp(int(ms[0]) / 1000, timezone.utc).astimezone(ET).date().isoformat(), 'page time', f'newsTime {ms[0]}'
    m = re.search(rf"\b((?:{MONTHS})\s+\d{{1,2}},\s+20\d\d)\s*$|\b(\d{{1,2}}\s+(?:{MONTHS}))\s*$", title or '', re.I)
    if m and ('Press Conference' in title or 'Speaks to Press' in title or 'News Conference' in title):
        d = eastern_day(m.group(1) or (m.group(2) + ' 2026'))
        if d not in ('', '?'):
            return d, 'title', title[-60:]
    if not pid.startswith('man-'):                       # a fetched page with no stamp in its metadata: a stamp after Published, Updated or Posted in its text
        texts = [flat(body[:8000])]
        if b.exists():
            texts.append(flat(re.sub(r'<[^>]+>', ' ', re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>', ' ', b.read_text(errors='replace'))))[:60000])
        for tx in texts:
            d, words, _ = printed_day(tx, keyword_only=True)
            if d:
                return d, 'stamp line', words
    return ('', 'stamp not read', given) if given.strip() else ('', 'none', '')
