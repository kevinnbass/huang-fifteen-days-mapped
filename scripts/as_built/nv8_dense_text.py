"""Third extraction, for pages whose article text is not in <article>/<main> or in <p> tags: the densest block of the saved HTML."""
import gzip, json, re
from bs4 import BeautifulSoup, NavigableString
INLINE = {'p', 'br', 'span', 'a', 'b', 'i', 'em', 'strong', 'blockquote', 'h2', 'h3', 'h4', 'u', 'font', 'li', 'ul', 'ol', 'figure', 'figcaption', 'sup', 'sub', 'q', 'cite', 'mark', 'small'}


def read(path):
    raw = open(path, 'rb').read()
    return gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw


def article_body(raw):
    """The longest articleBody string anywhere in the page's embedded data."""
    h = raw.decode('utf-8', 'replace'); best = ''
    for m in re.finditer(r'"articleBody"\s*:\s*"((?:[^"\\]|\\.)*)"', h):
        try:
            s = json.loads('"' + m.group(1) + '"')
        except Exception:
            continue
        s = re.sub(r'<[^>]+>', ' ', s)
        if len(s) > len(best):
            best = s
    return re.sub(r'[ \t]+', ' ', best).strip()


def densest(raw):
    soup = BeautifulSoup(raw, 'lxml')
    for t in soup(['script', 'style', 'noscript', 'svg', 'head']):
        t.decompose()
    best, score = None, 0
    for el in soup.find_all(True):
        if el.name in INLINE or el.name in ('html',):
            continue
        s = 0
        for c in el.children:
            if isinstance(c, NavigableString):
                s += len(c.strip())
            elif c.name in ('p', 'blockquote', 'span', 'b', 'i', 'em', 'strong', 'font', 'u', 'h2', 'h3'):
                x = c.get_text(' ', strip=True)
                s += len(x) if len(x) >= 40 or c.name not in ('span',) else 0
        if s > score:
            best, score = el, s
    if best is None:
        return ''
    parts = []
    for c in best.children:
        if isinstance(c, NavigableString):
            x = c.strip()
        elif c.name in INLINE or c.name in ('div', 'section'):
            x = re.sub(r'\s+', ' ', c.get_text(' ', strip=True)) if c.name not in ('div', 'section') or len(c.get_text(strip=True)) < 600 else ''
        else:
            x = ''
        if x:
            parts.append(re.sub(r'\s+', ' ', x))
    return '\n'.join(parts)


def best_text(path):
    raw = read(path); a = article_body(raw); d = densest(raw)
    return ('structured data (articleBody)', a) if len(a) >= max(300, 0.6 * len(d)) else ('the densest text block of the saved HTML', d)
