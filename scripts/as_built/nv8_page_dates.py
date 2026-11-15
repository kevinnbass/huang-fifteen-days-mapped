"""The day of a saved news page, read from the page itself, with the words it was read from.

Used by scripts/nv8_articles.py so that a piece dated after Nov 12, 2026 is not counted (Kevin, 2026-11-15: "don't add the pieces
dates 13 and 14"). Rules, in order; the first that applies gives the day, and the basis names it:
  header stamp the publication stamp the page's own metadata carries, as a U.S. Eastern day where it has a time and an offset;
  read by hand a day read in the page and entered below with the words it was read from;
  address      the page's address carries its day (/2026/11/13/, /20250227_);
  post         a post on X: the stamp in its saved record, as a U.S. Eastern day;
  yesterday, hours ago
               a hand-saved FT page prints "Published YESTERDAY" or "Published 17 HOURS AGO" beside the browser's print time
               (this computer's clock, U.S. Central): the day that works out to, U.S. Eastern;
  stamp line   a hand-saved page (a PDF printed from the publisher's site) carries a stamp near its top: "Published NOV 12 2026",
               "Updated Nov. 13, 2026 11 01 am ET", "Nov. 12, 2026". Where a page gives "Updated", that is the day of the version saved;
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
}
flat = lambda s: re.sub(r'\s+', ' ', s)


def day_of(pid, url, title, given):
    """(day, basis, the words it was read from)"""
    if given.strip():
        d = eastern_day(given)
        return ('', 'stamp not read', given) if d == '?' else (d, 'header stamp', given)
    f = P / pid / 'text.txt'
    whole = f.read_text(errors='replace') if f.exists() else ''
    body = whole.split('\n\n', 1)[1] if '\n\n' in whole[:1500] else whole
    if pid in HAND:
        assert flat(HAND[pid][1]) in flat(whole), pid
        return HAND[pid][0], 'read by hand', HAND[pid][1]
    m = re.search(r'/(20\d\d)/(\d\d)/(\d\d)/|/(20\d\d)(\d\d)(\d\d)_', url or '')
    if m:
        g = [x for x in m.groups() if x]
        return '-'.join(g), 'address', m.group(0)
    if 'x.com/' in (url or ''):
        m = re.search(r'"created_at":\s*"([^"]+)"', whole)
        if m:
            return datetime.strptime(m.group(1), '%a %b %d %H:%M:%S %z %Y').astimezone(ET).date().isoformat(), 'post', m.group(1)
    if pid.startswith('man-'):
        head = flat(body[:3000]); pr = PRINTED.search(head)
        m = re.search(r'Published (YESTERDAY|(\d{1,2}) HOURS? AGO)', head)
        if m and pr:
            when = datetime(2000 + int(pr.group(3)), int(pr.group(1)), int(pr.group(2)), int(pr.group(4)), int(pr.group(5)), tzinfo=CENTRAL)
            if m.group(2):
                return (when - timedelta(hours=int(m.group(2)))).astimezone(ET).date().isoformat(), 'hours ago', f'{m.group(0)}; printed {pr.group(0)}'
            return (when.date() - timedelta(days=1)).isoformat(), 'yesterday', f'{m.group(0)}; printed {pr.group(0)}'
        ms = list(STAMP.finditer(head))
        if ms:
            upd = [x for x in ms if (x.group(1) or '').lower() == 'updated']
            x = upd[0] if upd else ms[0]
            d = eastern_day(x.group(2))
            if d not in ('', '?'):
                return d, 'stamp line', x.group(0)
    b = P / pid / 'body.html'
    if b.exists() and re.search(r'itiger\.com|webull\.com', url or ''):
        t = b.read_text(errors='replace')
        ms = sorted(set(re.findall(r'20\d\d-\d\d-\d\d \d\d:\d\d', t)))
        if len(ms) == 1:
            return ms[0][:10], 'page time', ms[0]
        ms = sorted(set(re.findall(r'"newsTime":(\d{13})', t)))
        if len(ms) == 1:
            return datetime.fromtimestamp(int(ms[0]) / 1000, timezone.utc).astimezone(ET).date().isoformat(), 'page time', f'newsTime {ms[0]}'
    m = re.search(rf"\b((?:{MONTHS})\s+\d{{1,2}},\s+20\d\d)\s*$|\b(\d{{1,2}}\s+(?:{MONTHS}))\s*$", title or '', re.I)
    if m and ('Press Conference' in title or 'Speaks to Press' in title or 'News Conference' in title):
        d = eastern_day(m.group(1) or (m.group(2) + ' 2026'))
        if d not in ('', '?'):
            return d, 'title', title[-60:]
    return '', 'none', ''
