"""Shared render and tokens for the figure: warm paper background, spaced-caps kicker, bold title, grey subtitle,
legend chips, footnote under a rule. Row ids ride only in an HTML comment.
The page grows to fit its content; the PNG is cut at the measured height."""
import io
from pathlib import Path
import re
import struct
import zlib
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / 'figures'
BG = '#f7f4ee'; INK = '#191b1a'; MUTED = '#666960'; GRID = '#e3dfd5'; AXIS = '#c3c2b7'; CARD = '#efece4'
BLUE = '#2a78d6'; ORANGE = '#eb6834'; AQUA = '#1baf7a'; YELLOW = '#eda100'; RED = '#e34948'
BLUE250 = '#86b6ef'; GRAY = '#b2b4aa'; LGRAY = '#dcd9cf'; PURPLE = '#7b5cd6'
PARTY_D = '#2f5da8'; PARTY_R = '#b93129'
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def money(v):
    v = float(v)
    if v >= 1e6: return f'${v/1e6:,.1f}M' if v < 100e6 else f'${v/1e6:,.0f}M'
    return f'${v:,.0f}'


def day(d, year=False):
    """'2026-07-07' -> 'Jul 7'; '2026-05' -> 'May 2026'."""
    p = d.split('-')
    if len(p) == 2: return f'{MONTHS[int(p[1]) - 1]} {p[0]}'
    s = f'{MONTHS[int(p[1]) - 1]} {int(p[2])}'
    return f'{s}, {p[0]}' if year else s


def legend(items):
    return '<div class="legend">' + ''.join(f'<span><i class="sw" style="background:{c}"></i>{esc(t)}</span>' for c, t in items) + '</div>'


def cite(ids):
    return '<!-- rows: ' + ' '.join(sorted(set(ids))) + ' -->'


def shell(title, kicker, subtitle, body, footnote, width, extra_css=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(re.sub("<[^>]+>", "", title))}</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;width:{width}px;background:{BG}}}
body{{padding:46px 60px 34px;font-family:Arial,Helvetica,sans-serif;color:{INK}}}
.kicker{{font-size:17px;letter-spacing:2.8px;text-transform:uppercase;color:{MUTED};font-weight:bold}}
h1{{font-size:46px;letter-spacing:-1.4px;margin:12px 0 10px;line-height:1.07;max-width:{width - 160}px}}
.subtitle{{font-size:22px;line-height:1.35;color:{MUTED};margin:0 0 16px;max-width:{min(width - 220, 1900)}px}}
.legend{{display:flex;gap:26px;font-size:18px;color:{INK};margin:0 0 14px;flex-wrap:wrap}}
.legend span{{display:inline-flex;align-items:center;gap:9px}}.sw{{width:18px;height:18px;border-radius:4px;display:inline-block}}
.footnote{{margin-top:30px;border-top:1px solid #cdcfc6;padding-top:12px;font-size:15px;line-height:1.45;color:{MUTED}}}
.footnote b{{color:{INK}}}svg{{display:block}}text{{font-family:Arial,Helvetica,sans-serif}}{extra_css}
</style></head><body><div class="kicker">{esc(kicker)}</div><h1>{title}</h1><p class="subtitle">{subtitle}</p>{body}<div class="footnote">{footnote}</div></body></html>'''


def _png_chunk(f, kind, data):
    f.write(struct.pack('>I', len(data))); f.write(kind); f.write(data); f.write(struct.pack('>I', zlib.crc32(data, zlib.crc32(kind)) & 0xffffffff))


def save_png_bands(im, path, band=64):
    """Write an RGB picture as a PNG, losslessly, with the row filter chosen band by band (Nov 19, 2026).
    The library chooses a filter for every row by a rule of thumb. For this figure, dense small text on a flat ground, two fixed choices do better: no filter where the text is densest (the status text at the
    foot) and the filter Up elsewhere. For every band of rows both are tried: each candidate is compressed alone at level 9 and the smaller is fed to ONE zlib stream at level 9. The file holds the chunks
    IHDR, IDAT and IEND. The pixels are never changed: the written file is decoded again and compared with the picture, band by band, before this returns."""
    import numpy as np
    assert im.mode == 'RGB'; W, H = im.size; stride = W * 3; co = zlib.compressobj(9, zlib.DEFLATED, 15, 9, zlib.Z_DEFAULT_STRATEGY); picks = [0, 0]; prev = None
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n'); _png_chunk(f, b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)); buf = bytearray()
        for y in range(0, H, band):
            a = np.frombuffer(im.crop((0, y, W, min(H, y + band))).tobytes(), dtype=np.uint8).reshape(-1, stride); n = a.shape[0]
            up = a.copy(); up[1:] = a[1:] - a[:-1]                 # bytes wrap at 256, as the filter is defined; the first row of the picture has no row above and stays as it is
            if prev is not None: up[0] = a[0] - prev
            prev = a[-1].copy()
            c0 = np.concatenate([np.zeros((n, 1), np.uint8), a], axis=1).tobytes(); c2 = np.concatenate([np.full((n, 1), 2, np.uint8), up], axis=1).tobytes()
            use_up = len(zlib.compress(c2, 9)) < len(zlib.compress(c0, 9)); picks[use_up] += 1; buf += co.compress(c2 if use_up else c0)
            if len(buf) >= 1 << 23: _png_chunk(f, b'IDAT', bytes(buf)); buf = bytearray()
        buf += co.flush(); _png_chunk(f, b'IDAT', bytes(buf)); _png_chunk(f, b'IEND', b'')
    lim = Image.MAX_IMAGE_PIXELS; Image.MAX_IMAGE_PIXELS = None
    try:
        with Image.open(path) as chk:
            chk.load(); assert chk.mode == 'RGB' and chk.size == im.size, (chk.mode, chk.size)
            for y in range(0, H, 4096): assert chk.crop((0, y, W, min(H, y + 4096))).tobytes() == im.crop((0, y, W, min(H, y + 4096))).tobytes(), ('the PNG does not decode to the picture', y)
    finally: Image.MAX_IMAGE_PIXELS = lim
    print('png written in bands', Path(path).name, Path(path).stat().st_size, 'bytes | bands without a filter', picks[0], '| with the filter Up', picks[1], '| decoded again: the same pixels')


# Figures whose PNG is written with a palette of at most 256 colours (save_png_palette below). Take a name out of this set and its PNG is written in true colour again (the map's by save_png_bands).
PALETTE_PNG = {'nv8-fifteen-days-mapped'}


def save_png_palette(im, path, colours=256, band=2000):
    """Write an RGB picture as a PNG of the same size with a palette of at most 256 colours (Nov 23, 2026).
    The map figure's true-colour PNG had reached the largest size its host accepts for one file (100 MiB), and records that the builder owes could no longer be added to it. The figure is flat inks on flat
    grounds: about 99 in 100 of its pixels have one of a few hundred colours, and the rest are the blended edges of letters and lines. Half of the palette is the most frequent colours, kept exactly. The other
    half is chosen one colour at a time, by turns: the colour whose pixels are, taken together, furthest from the palette; and the colour of at least 16 pixels that is furthest from it, so that an ink used
    for a few dots only keeps its own colour. Every other colour goes to the nearest palette colour. Nothing is dithered and no pixel moves. The written file is decoded again and compared with the mapped
    picture before this returns; the share of pixels altered and the largest change are printed and returned, and the build stops if any pixel would change by more than 48 levels or more than 1 pixel in 50 would change. The builder chose this without the figure's owner; the set PALETTE_PNG above undoes it."""
    import numpy as np
    assert im.mode == 'RGB' and 2 <= colours <= 256; W, H = im.size
    packed = lambda y: np.frombuffer(im.crop((0, y, W, min(H, y + band))).convert('RGBX').tobytes(), dtype='<u4') & 0xFFFFFF        # one number per pixel: red + 256 green + 65,536 blue
    counts = np.zeros(1 << 24, np.int64)
    for y in range(0, H, band): counts += np.bincount(packed(y), minlength=1 << 24)
    total = int(counts.sum()); assert total == W * H
    distinct = np.flatnonzero(counts); cn = counts[distinct]; C = np.stack([distinct & 255, (distinct >> 8) & 255, (distinct >> 16) & 255], axis=1).astype(np.int64)
    order = np.lexsort((distinct, -cn)); d2 = np.full(len(distinct), 1 << 40, np.int64); near = np.zeros(len(distinct), np.int64); chosen = []
    def take(j):                                                   # colour j joins the palette; every colour nearer to it than to its palette colour so far moves to it
        dj = ((C - C[j]) ** 2).sum(axis=1); m = dj < d2; d2[m] = dj[m]; near[m] = len(chosen); chosen.append(int(j))
    for j in order[:colours // 2]: take(j)
    big = cn >= 16
    while len(chosen) < colours and d2.max() > 0:
        if len(chosen) % 2 and (d2[big] > 0).any(): take(int(np.argmax(np.where(big, d2, 0))))
        else: take(int(np.argmax(d2 * cn)))
    pal = C[chosen]; err = np.abs(C - pal[near]).max(axis=1); altered = int(cn[err > 0].sum()); over = int(cn[err > 16].sum())
    lut = np.zeros(1 << 24, np.uint8); lut[distinct] = near; idx = np.empty((H, W), np.uint8)
    for y in range(0, H, band): idx[y:y + band] = lut[packed(y)].reshape(-1, W)
    flat = np.zeros(768, np.uint8); flat[:len(chosen) * 3] = pal.astype(np.uint8).ravel()
    q = Image.fromarray(idx); q.putpalette(flat.tolist()); assert q.mode == 'P'; q.save(path, compress_level=9)
    lim = Image.MAX_IMAGE_PIXELS; Image.MAX_IMAGE_PIXELS = None
    try:
        with Image.open(path) as chk:
            chk.load(); assert chk.mode == 'P' and chk.size == im.size and bytes(chk.getpalette()[:len(chosen) * 3]) == pal.astype(np.uint8).tobytes(), (chk.mode, chk.size)
            for y in range(0, H, band): assert (np.asarray(chk.crop((0, y, W, min(H, y + band)))) == idx[y:y + band]).all(), ('the PNG does not decode to the mapped picture', y)
    finally: Image.MAX_IMAGE_PIXELS = lim
    out = {'bytes': Path(path).stat().st_size, 'colours': len(chosen), 'colours_in_the_picture': int(len(distinct)), 'pixels': total, 'pixels_altered': altered, 'largest_change': int(err.max()), 'pixels_changed_by_more_than_16': over}
    print('png written with a palette', Path(path).name, out['bytes'], 'bytes |', len(chosen), 'colours of', len(distinct), '| pixels altered', altered, f'({100 * altered / total:.3f}%) | largest change in one channel',
          out['largest_change'], '| pixels changed by more than 16 levels', over, f'({100 * over / total:.4f}%) | decoded again: the same picture')
    assert out['largest_change'] <= 48 and altered * 50 <= total, ('the palette would change the picture by more than its bound', out)
    return out


def render(stem, document, width):
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / (stem + '.html'); path.write_text(document, encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': width, 'height': 900}, device_scale_factor=2)
        pg.goto(path.as_uri(), wait_until='networkidle'); pg.evaluate('document.fonts.ready')
        ov = pg.evaluate('({w:document.documentElement.scrollWidth,h:Math.ceil(document.documentElement.scrollHeight)})')
        assert ov['w'] <= width, (stem, 'content wider than the page', ov)
        clipped = pg.evaluate('''() => [...document.querySelectorAll('[data-fit]')].filter(e => e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1).map(e => e.textContent.slice(0, 60))''')
        assert not clipped, (stem, 'text overflows its box', clipped)
        # The picture is taken in tiles and joined: one screenshot of a page taller or wider than about 16,000 device
        # pixels comes back with blank bands (found Nov 14, 2026 on a figure 20,832 pixels tall).
        TW, TH = min(width, 3400), 1600; pg.set_viewport_size({'width': TW, 'height': TH})
        im = Image.new('RGB', (width * 2, ov['h'] * 2), 'white')
        for y in range(0, ov['h'], TH):
            for x in range(0, width, TW):
                w_, h_ = min(TW, width - x), min(TH, ov['h'] - y)
                tile = Image.open(io.BytesIO(pg.screenshot(clip={'x': x, 'y': y, 'width': w_, 'height': h_}, full_page=True))).convert('RGB')
                assert tile.size == (w_ * 2, h_ * 2), (stem, 'a tile of the picture has the wrong size', (x, y), tile.size)
                im.paste(tile, (x * 2, y * 2))
        b.close()
    # The map figure's host refuses a file of 100 MiB or more. From Nov 19 to Nov 22, 2026 its true-colour PNG was written band by band (save_png_bands above: the same pixels, about 5% smaller than the
    # library writes it), a stopgap that was used up by Nov 21. Since Nov 23, 2026 it is written with a palette of 256 colours (save_png_palette above), about half the size; the builder chose that
    # without the figure's owner, and the set PALETTE_PNG undoes it. The JPG below is made from the true-colour picture in either case.
    if stem in PALETTE_PNG: save_png_palette(im, FIGURES / (stem + '.png'))
    elif stem == 'nv8-fifteen-days-mapped': save_png_bands(im, FIGURES / (stem + '.png'))
    else: im.save(FIGURES / (stem + '.png'))
    # A JPEG can have no side over 65,500 pixels. The map passed that height on Nov 17, 2026 (83,628 pixels): its JPG is then the PNG scaled down to the limit, and the PNG stays the full image.
    if max(im.size) > 65500:
        k = 65500 / max(im.size); small = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS); small.save(FIGURES / (stem + '.jpg'), quality=92); print('jpg scaled to', small.size, 'from', im.size)
    else:
        im.save(FIGURES / (stem + '.jpg'), quality=92)
    print('rendered', stem, im.size)
