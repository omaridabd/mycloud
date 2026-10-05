"""Transparent 1920x1080 overlay PNGs (cached by kind+text)."""
import hashlib, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

OUT = os.path.join(ROOT, 'graphics', 'ov')
os.makedirs(OUT, exist_ok=True)


def _new():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def badge(d, _):
    f = font(30, '800ExtraBold')
    t1, t2 = 'اليمن', '5 أكتوبر 2026'
    w1 = tsize(d, t1, f)[0]
    f2 = font(26, '600SemiBold')
    w2 = tsize(d, t2, f2)[0]
    x = 50
    d.rectangle([x, 44, x + w2 + 36, 96], fill=(8, 14, 28, 215))
    text_c(d, (x + (w2 + 36) / 2, 70), t2, f2)
    d.rectangle([x + w2 + 36, 44, x + w2 + 36 + w1 + 40, 96], fill=RED + (255,))
    text_c(d, (x + w2 + 36 + (w1 + 40) / 2, 70), t1, f)


def credit(d, txt):
    f = font(24, '600SemiBold')
    t = 'المصدر: ' + txt
    tw = tsize(d, t, f)[0]
    d.rectangle([50, H - 92, 50 + tw + 32, H - 50], fill=(0, 0, 0, 165))
    text_c(d, (50 + (tw + 32) / 2, H - 71), t, f, fill=(235, 238, 245, 255))


def loc(d, txt):
    f = font(32, '700Bold')
    tw = tsize(d, txt, f)[0]
    x1 = W - 60
    d.rectangle([x1 - tw - 50, H - 118, x1, H - 56], fill=(8, 14, 28, 220))
    d.rectangle([x1 - 10, H - 118, x1, H - 56], fill=RED + (255,))
    text_c(d, (x1 - 10 - (tw + 40) / 2, H - 87), txt, f)


def label(d, txt):
    f = font(28, '700Bold')
    tw = tsize(d, txt, f)[0]
    x1 = W - 60
    d.rounded_rectangle([x1 - tw - 40, 44, x1, 98], 8, fill=(200, 22, 38, 225))
    text_c(d, (x1 - (tw + 40) / 2, 71), txt, f)


def archive(d, txt):
    f = font(28, '700Bold')
    tw = tsize(d, txt, f)[0]
    x1 = W - 60
    d.rounded_rectangle([x1 - tw - 40, 44, x1, 98], 8, fill=(40, 48, 66, 230))
    text_c(d, (x1 - (tw + 40) / 2, 71), txt, f, fill=GOLD + (255,))


def hook(d, txt):
    l1, l2 = txt.split('|')
    f1 = font(84, '900Black'); f2 = font(54, '700Bold')
    w1 = tsize(d, l1, f1)[0]; w2 = tsize(d, l2, f2)[0]
    x1 = W - 90
    d.rectangle([x1 - w1 - 70, 700, x1, 830], fill=(8, 14, 28, 225))
    d.rectangle([x1 - 16, 700, x1, 830], fill=RED + (255,))
    text_rtl(d, (x1 - 42, 765), l1, f1, anchor='rm')
    d.rectangle([x1 - w2 - 70, 840, x1, 930], fill=RED + (235,))
    text_rtl(d, (x1 - 35, 885), l2, f2, anchor='rm')


def section(d, txt):
    f = font(46, '800ExtraBold')
    tw = tsize(d, txt, f)[0]
    x1 = W - 60
    d.rectangle([x1 - tw - 70, 150, x1, 236], fill=(8, 14, 28, 230))
    d.rectangle([x1 - 14, 150, x1, 236], fill=RED + (255,))
    text_c(d, (x1 - 14 - (tw + 56) / 2, 193), txt, f)


def guest(d, _):
    f = font(26, '700Bold'); f2 = font(22, '500Medium')
    t1, t2 = 'اللواء د. فايز الدويري', 'خبير عسكري · مداخلة صوتية'
    w = max(tsize(d, t1, f)[0], tsize(d, t2, f2)[0]) + 50
    d.rectangle([50, 110, 50 + w, 196], fill=(8, 14, 28, 200))
    d.rectangle([50, 110, 58, 196], fill=RED + (255,))
    text_rtl(d, (50 + w - 20, 138), t1, f, anchor='rm')
    text_rtl(d, (50 + w - 20, 174), t2, f2, fill=(190, 198, 212, 255), anchor='rm')


KINDS = dict(badge=badge, credit=credit, loc=loc, label=label, archive=archive, hook=hook, section=section, guest=guest)


def get(kind, txt=''):
    h = hashlib.md5(f'{kind}|{txt}'.encode()).hexdigest()[:10]
    p = os.path.join(OUT, f'{kind}_{h}.png')
    if not os.path.exists(p):
        im, d = _new()
        KINDS[kind](d, txt)
        im.save(p)
    return p
