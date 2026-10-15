"""Animated map renderer -> mp4 (25 fps, 1920x1080).

Usage: python3 graphics/maps.py [name ...]   (renders all specs from map_specs.py if none given)
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

DATA = os.path.join(ROOT, 'maps', 'data')
OUT = os.path.join(ROOT, 'maps')
_geo = {}


def geo(name):
    if name not in _geo:
        _geo[name] = json.load(open(os.path.join(DATA, name + '_reg.json')))['features']
    return _geo[name]


def rings_of(g):
    if g['type'] == 'Polygon':
        return [g['coordinates']]
    if g['type'] == 'MultiPolygon':
        return g['coordinates']
    return []


def lines_of(g):
    if g['type'] == 'LineString':
        return [g['coordinates']]
    if g['type'] == 'MultiLineString':
        return g['coordinates']
    return []


class Proj:
    """Equirectangular with cos(lat) scaling; view = (lon_c, lat_c, span_lon)."""
    def __init__(self, view, w, h):
        self.lon, self.lat, self.span = view
        self.k = math.cos(math.radians(self.lat))
        self.ppd = w / self.span            # px per degree lon
        self.w, self.h = w, h

    def __call__(self, lon, lat):
        x = self.w / 2 + (lon - self.lon) * self.ppd
        y = self.h / 2 - (lat - self.lat) * self.ppd / self.k
        return x, y


SEA = (9, 22, 40)
LAND = (44, 50, 62)
YEM = (58, 64, 80)


def render_base(view, w, h, spec):
    P = Proj(view, w, h)
    s = w / W
    im = Image.new('RGB', (w, h), SEA)
    d = ImageDraw.Draw(im)
    hlc = spec.get('hl_countries', {spec.get('hl_country', 'YEM'): YEM})
    for f in geo('countries'):
        col = hlc.get(f['properties']['ADM0_A3'], LAND)
        for poly in rings_of(f['geometry']):
            d.polygon([P(*c) for c in poly[0]], fill=col)
    # highlighted governorates
    hl = spec.get('hl_admin', [])
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    for f in geo('admin1'):
        if f['properties']['name'] in hl:
            for poly in rings_of(f['geometry']):
                dl.polygon([P(*c) for c in poly[0]], fill=(150, 16, 30, 150))
    im = Image.alpha_composite(im.convert('RGBA'), lay)
    d = ImageDraw.Draw(im)
    # roads
    if spec.get('roads', True):
        for f in geo('roads'):
            for ln in lines_of(f['geometry']):
                pts = [P(*c) for c in ln]
                d.line(pts, fill=(78, 84, 98), width=max(1, int(1.6 * s)))
    # admin borders (Yemen only)
    for f in geo('admin1'):
        if f['properties']['adm0_a3'] not in spec.get('admin_of', list(hlc)):
            continue
        for poly in rings_of(f['geometry']):
            d.line([P(*c) for c in poly[0]], fill=(96, 104, 122), width=max(1, int(1.3 * s)))
    # coastline / country borders
    for f in geo('countries'):
        dashed = f['properties']['ADM0_A3'] in spec.get('dashed_countries', [])
        for poly in rings_of(f['geometry']):
            pts = [P(*c) for c in poly[0]]
            if dashed:
                for j in range(0, len(pts) - 1, 2):
                    d.line(pts[j:j + 2], fill=(140, 150, 170), width=max(1, int(1.6 * s)))
            else:
                d.line(pts, fill=(140, 150, 170), width=max(1, int(2.2 * s)))
    # big faded labels
    for (txt, lon, lat, sz) in spec.get('bglabels', []):
        x, y = P(lon, lat)
        text_c(d, (x, y), txt, font(int(sz * s), '600SemiBold'), fill=(150, 160, 180, 255))
    return im.convert('RGB')


def vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    v = np.clip(1.25 - 0.75 * (((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2), 0.3, 1)
    return v[..., None]


VIG = None


def lerp(a, b, t):
    return a + (b - a) * t


def view_at(spec, t):
    v0, v1 = spec['view0'], spec.get('view1', spec['view0'])
    z0, z1 = spec.get('zoom_t', (0, spec['dur']))
    e = ease((t - z0) / max(0.01, z1 - z0))
    # interpolate span geometrically
    span = math.exp(lerp(math.log(v0[2]), math.log(v1[2]), e))
    return (lerp(v0[0], v1[0], e), lerp(v0[1], v1[1], e), span)


def arrowhead(d, p0, p1, col, size):
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    pts = [p1, (p1[0] + size * math.cos(a1), p1[1] + size * math.sin(a1)),
           (p1[0] + size * math.cos(a2), p1[1] + size * math.sin(a2))]
    d.polygon(pts, fill=col)


def label_box(d, x, y, txt, f, fg=WHITE, bg=(0, 0, 0, 170), side='l', alpha=1.0, accent=None):
    tw, th, b = tsize(d, txt, f)
    pad = 12
    if side == 'l':
        x1 = x - 22; x0 = x1 - tw - 2 * pad
    elif side == 'r':
        x0 = x + 22; x1 = x0 + tw + 2 * pad
    else:  # centered above
        x0 = x - tw / 2 - pad; x1 = x + tw / 2 + pad; y = y - 46
    y0 = y - th / 2 - 10; y1 = y + th / 2 + 12
    a = int(alpha * 255)
    d.rounded_rectangle([x0, y0, x1, y1], 6, fill=bg[:3] + (int(bg[3] * alpha),))
    if accent:
        d.rectangle([x1 - 5, y0, x1, y1], fill=accent + (a,))
    text_c(d, ((x0 + x1) / 2, (y0 + y1) / 2 + 1), txt, f, fill=fg[:3] + (a,))


def title_bar(d, title, sub, alpha):
    a = int(255 * alpha)
    f1 = font(46, '800ExtraBold'); f2 = font(28, '500Medium')
    tw = tsize(d, title, f1)[0]
    sw = tsize(d, sub, f2)[0] if sub else 0
    wbox = max(tw, sw) + 70
    x1 = W - 60; x0 = x1 - wbox
    d.rectangle([x0, 50, x1, 50 + (150 if sub else 100)], fill=(8, 14, 28, int(215 * alpha)))
    d.rectangle([x1 - 12, 50, x1, 50 + (150 if sub else 100)], fill=RED + (a,))
    text_rtl(d, (x1 - 36, 100), title, f1, fill=WHITE + (a,), anchor='rm')
    if sub:
        text_rtl(d, (x1 - 36, 160), sub, f2, fill=(205, 212, 225, a), anchor='rm')


def chip(d, txt, x_right, y, alpha=1, col=RED):
    f = font(28, '700Bold')
    tw = tsize(d, txt, f)[0]
    a = int(255 * alpha)
    d.rounded_rectangle([x_right - tw - 40, y, x_right, y + 56], 8, fill=col + (int(235 * alpha),))
    text_c(d, (x_right - (tw + 40) / 2, y + 29), txt, f, fill=WHITE + (a,))


def render(spec):
    global VIG
    if VIG is None:
        VIG = vignette()
    name = spec['name']
    dur = spec['dur']
    n = int(round(dur * FPS))
    # union base
    v0, v1 = spec['view0'], spec.get('view1', spec['view0'])
    ctr = ((v0[0] + v1[0]) / 2, (v0[1] + v1[1]) / 2)
    k = math.cos(math.radians(ctr[1]))
    lon_min = min(v0[0] - v0[2] / 2, v1[0] - v1[2] / 2) - 0.05
    lon_max = max(v0[0] + v0[2] / 2, v1[0] + v1[2] / 2) + 0.05
    hs0, hs1 = v0[2] * 9 / 16 * k, v1[2] * 9 / 16 * k
    lat_min = min(v0[1] - hs0 / 2, v1[1] - hs1 / 2) - 0.05
    lat_max = max(v0[1] + hs0 / 2, v1[1] + hs1 / 2) + 0.05
    span_u = lon_max - lon_min
    ppd = W / min(v0[2], v1[2]) * 1.05
    bw = int(span_u * ppd)
    bh = int((lat_max - lat_min) * ppd / k)
    bview = ((lon_min + lon_max) / 2, (lat_min + lat_max) / 2, span_u)
    base = render_base(bview, bw, bh, spec)
    BP = Proj(bview, bw, bh)
    BP.k = k
    BP.h = bh
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, name + '.mp4')
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                           '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                           '-crf', '16', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        vw = view_at(spec, t)
        P = Proj(vw, W, H); P.k = k
        # crop rect in base pixels
        cx, cy = BP(vw[0], vw[1])
        cw = vw[2] * ppd; ch = cw * 9 / 16
        fr = base.resize((W, H), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
        fr = Image.fromarray((np.asarray(fr).astype(np.float32) * VIG).astype(np.uint8)).convert('RGBA')
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        # areas
        for a in spec.get('areas', []):
            al = ease((t - a['t']) / 0.8)
            if al <= 0:
                continue
            pts = [P(*c) for c in a['poly']]
            pulse = 0.85 + 0.15 * math.sin(t * 3)
            d.polygon(pts, fill=a['color'] + (int(a.get('alpha', 110) * al * pulse),))
            d.line(pts + [pts[0]], fill=a['color'] + (int(230 * al),), width=4)
            if a.get('label'):
                xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
                label_box(d, sum(xs) / len(xs), sum(ys) / len(ys), a['label'], font(30, '700Bold'),
                          side='c', alpha=al, bg=(0, 0, 0, 150))
        # rings
        for r in spec.get('rings', []):
            al = ease((t - r['t']) / 0.8)
            if al <= 0:
                continue
            x, y = P(*r['ll'])
            rad = r['km'] / 111.0 * P.ppd / P.k * ease((t - r['t']) / 1.2)
            d.ellipse([x - rad, y - rad, x + rad, y + rad], outline=r.get('color', GOLD) + (int(230 * al),), width=4)
            if r.get('label'):
                label_box(d, x, y - rad, r['label'], font(28, '700Bold'), side='c', alpha=al, accent=GOLD)
        # paths
        for p in spec.get('paths', []):
            if t < p['t0']:
                continue
            e = ease((t - p['t0']) / max(0.01, p['t1'] - p['t0']))
            pts = [P(*c) for c in p['pts']]
            seg = [0]
            for a_, b_ in zip(pts, pts[1:]):
                seg.append(seg[-1] + math.dist(a_, b_))
            L = seg[-1] * e
            draw = [pts[0]]
            for j in range(1, len(pts)):
                if seg[j] <= L:
                    draw.append(pts[j])
                else:
                    f_ = (L - seg[j - 1]) / max(1e-6, seg[j] - seg[j - 1])
                    draw.append((lerp(pts[j - 1][0], pts[j][0], f_), lerp(pts[j - 1][1], pts[j][1], f_)))
                    break
            col = p.get('color', RED)
            wdt = p.get('width', 9)
            if len(draw) >= 2:
                if p.get('dash'):
                    acc = 0
                    for a_, b_ in zip(draw, draw[1:]):
                        sl = math.dist(a_, b_); s0 = 0
                        while s0 < sl:
                            s1 = min(sl, s0 + 22)
                            if int((acc + s0) // 22) % 2 == 0:
                                d.line([(lerp(a_[0], b_[0], s0 / sl), lerp(a_[1], b_[1], s0 / sl)),
                                        (lerp(a_[0], b_[0], s1 / sl), lerp(a_[1], b_[1], s1 / sl))], fill=col + (255,), width=wdt)
                            s0 = s1
                        acc += sl
                else:
                    d.line(draw, fill=(0, 0, 0, 120), width=wdt + 6, joint='curve')
                    d.line(draw, fill=col + (255,), width=wdt, joint='curve')
                if p.get('arrow', True) and e > 0.05:
                    arrowhead(d, draw[-2], draw[-1], col + (255,), wdt * 3.2)
            if p.get('label') and e >= 1:
                al = ease((t - p['t1']) / 0.5)
                mx, my = pts[len(pts) // 2] if len(pts) > 2 else ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
                ox, oy = p.get('loff', (0, 0))
                label_box(d, mx + ox, my + oy, p['label'], font(30, '700Bold'), side='c', alpha=al,
                          accent=col, bg=(0, 0, 0, 190))
        # pins
        for pn in spec.get('pins', []):
            al = ease((t - pn['t']) / 0.5)
            if al <= 0:
                continue
            x, y = P(*pn['ll'])
            col = pn.get('color', RED)
            big = pn.get('big', False)
            r0 = 13 if big else 9
            if pn.get('pulse', big):
                ph = ((t - pn['t']) % 1.6) / 1.6
                rr = r0 + 40 * ph
                d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=col + (int(200 * (1 - ph) * al),), width=4)
            d.ellipse([x - r0 - 4, y - r0 - 4, x + r0 + 4, y + r0 + 4], fill=(255, 255, 255, int(255 * al)))
            d.ellipse([x - r0, y - r0, x + r0, y + r0], fill=col + (int(255 * al),))
            if pn.get('name'):
                f = font(36 if big else 28, '800ExtraBold' if big else '700Bold')
                label_box(d, x, y, pn['name'], f, side=pn.get('side', 'l'), alpha=al,
                          accent=col if big else None, bg=(0, 0, 0, 185))
        # title, chips, legend
        if spec.get('title'):
            title_bar(d, spec['title'], spec.get('sub'), ease(t / 0.6))
        yy = 230 if spec.get('sub') else 180
        for c_ in spec.get('chips', []):
            if t >= c_['t']:
                chip(d, c_['txt'], W - 60, yy, ease((t - c_['t']) / 0.5), c_.get('col', RED))
                yy += 70
        if spec.get('legend'):
            ly = H - 70 - 52 * len(spec['legend'])
            d.rounded_rectangle([W - 520, ly - 20, W - 60, H - 90], 10, fill=(0, 0, 0, 170))
            for j, (col, txt) in enumerate(spec['legend']):
                yj = ly + 52 * j + 10
                d.rectangle([W - 110, yj - 12, W - 80, yj + 12], fill=col + (255,))
                text_rtl(d, (W - 130, yj), txt, font(26, '600SemiBold'), anchor='rm')
        src = spec.get('src', 'خريطة توضيحية · المواقع تقريبية')
        text_rtl(d, (W - 60, H - 40), src, font(22, '500Medium'), fill=(190, 198, 212, 220), anchor='rm')
        fr = Image.alpha_composite(fr, lay).convert('RGB')
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()
    print('rendered', out, n, 'frames')


if __name__ == '__main__':
    from map_specs import SPECS
    names = sys.argv[1:]
    for s in SPECS:
        if not names or s['name'] in names:
            render(s)
