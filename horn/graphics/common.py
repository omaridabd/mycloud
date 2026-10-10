"""Shared drawing helpers: fonts, RTL Arabic text, palette, backgrounds."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, 'graphics', 'fonts')
W, H = 1920, 1080
FPS = 25

KUFI = {w: os.path.join(FD, f'NotoKufiArabic_{w}.ttf') for w in
        ['400Regular', '500Medium', '600SemiBold', '700Bold', '800ExtraBold', '900Black']}
PLEX = {w: os.path.join(FD, f'IBMPlexSansArabic_{w}.ttf') for w in
        ['400Regular', '500Medium', '600SemiBold', '700Bold']}

RED = (200, 22, 38)
DRED = (120, 10, 20)
NAVY = (10, 18, 36)
NAVY2 = (18, 32, 62)
WHITE = (255, 255, 255)
GOLD = (236, 178, 46)
GREY = (170, 178, 192)
BLUE = (40, 120, 220)
GREEN = (34, 170, 90)

_fc = {}


def font(size, w='700Bold', fam='kufi'):
    k = (size, w, fam)
    if k not in _fc:
        p = (KUFI if fam == 'kufi' else PLEX)[w]
        _fc[k] = ImageFont.truetype(p, size, layout_engine=ImageFont.Layout.RAQM)
    return _fc[k]


def tsize(d, txt, f):
    b = d.textbbox((0, 0), txt, font=f, direction='rtl', language='ar')
    return b[2] - b[0], b[3] - b[1], b


def text_rtl(d, xy_right, txt, f, fill=WHITE, anchor='ra', **kw):
    """Draw Arabic text with its right edge at x (anchor 'ra' = right/ascender)."""
    d.text(xy_right, txt, font=f, fill=fill, anchor=anchor, direction='rtl', language='ar', **kw)


def text_c(d, xy, txt, f, fill=WHITE, anchor='mm', **kw):
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, direction='rtl', language='ar', **kw)


def wrap(d, txt, f, maxw):
    words = txt.split()
    lines, cur = [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if tsize(d, t, f)[0] <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def navy_bg(seed=0):
    """Dark navy gradient with subtle grid and vignette."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = 1 - np.sqrt(((x - W * 0.55) / W) ** 2 + ((y - H * 0.4) / H) ** 2)
    g = np.clip(g, 0, 1)
    base = np.zeros((H, W, 3), np.float32)
    for i, (a, b) in enumerate(zip(NAVY, NAVY2)):
        base[..., i] = a + (b - a) * g
    grid = ((x % 60 < 1.2) | (y % 60 < 1.2)).astype(np.float32) * 10
    base += grid[..., None] * np.array([0.6, 0.8, 1.0])
    vig = np.clip(1.15 - 0.6 * (((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2), 0.35, 1)
    base *= vig[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')


def red_bar(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=RED)


def shadow(im, radius=12, alpha=150):
    """Return an RGBA shadow layer from an RGBA image's alpha."""
    a = im.split()[-1].filter(ImageFilter.GaussianBlur(radius))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: v * alpha // 255))
    return sh


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)
