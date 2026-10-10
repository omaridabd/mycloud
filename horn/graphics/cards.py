"""Full-frame cards (PNG) and animated stat counters (mp4)."""
import os, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

OUT = os.path.join(ROOT, 'graphics', 'cards')
os.makedirs(OUT, exist_ok=True)


def save(im, name):
    p = os.path.join(OUT, name + '.png')
    im.convert('RGB').save(p)
    return p


def kicker(d, txt, y=120, col=RED):
    f = font(34, '700Bold')
    tw = tsize(d, txt, f)[0]
    d.rectangle([W - 140 - tw - 40, y, W - 140, y + 64], fill=col)
    text_c(d, (W - 140 - (tw + 40) / 2, y + 33), txt, f)


def headline_card(name, outlet, date, headline, quotes, label='خبر', chip_txt=None):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 200, 150, W - 200, H - 150
    d.rounded_rectangle([x0 + 10, y0 + 14, x1 + 10, y1 + 14], 18, fill=(0, 0, 0, 120))
    d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(250, 250, 252))
    d.rectangle([x0, y0, x1, y0 + 92], fill=(236, 238, 242))
    text_rtl(d, (x1 - 50, y0 + 46), outlet, font(40, '800ExtraBold'), fill=(20, 24, 34), anchor='rm')
    d.text((x0 + 50, y0 + 46), date, font=font(30, '500Medium'), fill=(90, 96, 110), anchor='lm',
           direction='rtl', language='ar')
    lf = font(28, '700Bold')
    lw = tsize(d, label, lf)[0]
    d.rounded_rectangle([x0 + 50, y0 + 120, x0 + 50 + lw + 36, y0 + 172], 8, fill=RED)
    text_c(d, (x0 + 50 + (lw + 36) / 2, y0 + 147), label, lf)
    hf = font(58, '800ExtraBold')
    y = y0 + 210
    for ln in wrap(d, headline, hf, x1 - x0 - 120):
        text_rtl(d, (x1 - 60, y), ln, hf, fill=(16, 20, 30), anchor='ra')
        y += 92
    y += 26
    qf = font(36, '500Medium', 'plex')
    for q in quotes:
        lines = wrap(d, q, qf, x1 - x0 - 170)
        ys = y
        for ln in lines:
            text_rtl(d, (x1 - 90, y), ln, qf, fill=(50, 56, 70), anchor='ra')
            y += 58
        d.rectangle([x1 - 66, ys + 6, x1 - 58, y - 8], fill=RED)
        y += 20
    if chip_txt:
        cf = font(30, '700Bold')
        cw = tsize(d, chip_txt, cf)[0]
        d.rounded_rectangle([x0 + 50, y1 - 96, x0 + 50 + cw + 44, y1 - 40], 10, fill=(20, 24, 34))
        text_c(d, (x0 + 50 + (cw + 44) / 2, y1 - 67), chip_txt, cf, fill=GOLD)
    return save(im, name)


def quote_card(name, kick, quote, attrib, note=None):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    kicker(d, kick)
    d.text((W - 150, 360), '”', font=font(300, '900Black'), fill=RED, anchor='rm')
    qf = font(64, '800ExtraBold')
    lines = wrap(d, quote, qf, W - 420)
    y = 330 + max(0, (3 - len(lines))) * 50
    for ln in lines:
        text_rtl(d, (W - 300, y), ln, qf, anchor='ra')
        y += 110
    d.rectangle([W - 300 - 6, y + 30, W - 300, y + 90], fill=RED)
    text_rtl(d, (W - 330, y + 60), attrib, font(36, '600SemiBold'), fill=(200, 208, 222), anchor='rm')
    if note:
        cf = font(28, '700Bold')
        cw = tsize(d, note, cf)[0]
        d.rounded_rectangle([140, H - 140, 140 + cw + 44, H - 84], 10, fill=(60, 66, 82))
        text_c(d, (140 + (cw + 44) / 2, H - 111), note, cf, fill=GOLD)
    return save(im, name)


def points_card(name, kick, title, points, attrib, note=None):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    kicker(d, kick)
    text_rtl(d, (W - 160, 250), title, font(60, '800ExtraBold'), anchor='ra')
    y = 400
    pf = font(46, '600SemiBold')
    for p in points:
        d.ellipse([W - 200, y + 22, W - 176, y + 46], fill=RED)
        for ln in wrap(d, p, pf, W - 480):
            text_rtl(d, (W - 230, y), ln, pf, anchor='ra')
            y += 76
        y += 30
    text_rtl(d, (W - 160, y + 30), attrib, font(32, '500Medium'), fill=(190, 198, 212), anchor='ra')
    if note:
        cf = font(28, '700Bold')
        cw = tsize(d, note, cf)[0]
        d.rounded_rectangle([140, H - 140, 140 + cw + 44, H - 84], 10, fill=(60, 66, 82))
        text_c(d, (140 + (cw + 44) / 2, H - 111), note, cf, fill=GOLD)
    return save(im, name)


def two_col(name, title, right, left, foot=None):
    """right/left = (header, color, [lines], source)."""
    im = navy_bg()
    d = ImageDraw.Draw(im)
    text_c(d, (W / 2, 140), title, font(60, '800ExtraBold'))
    d.rectangle([W / 2 - 80, 190, W / 2 + 80, 198], fill=RED)
    colw = 760
    for i, (hdr, col, lines, src) in enumerate([right, left]):
        x1 = W - 150 - i * (colw + 100)
        x0 = x1 - colw
        d.rounded_rectangle([x0, 260, x1, 900], 16, fill=(14, 24, 46, 235), outline=col, width=3)
        d.rounded_rectangle([x0, 260, x1, 350], 16, fill=col)
        d.rectangle([x0, 320, x1, 350], fill=col)
        text_c(d, ((x0 + x1) / 2, 305), hdr, font(42, '800ExtraBold'))
        y = 400
        lf = font(40, '600SemiBold')
        for ln0 in lines:
            for ln in wrap(d, ln0, lf, colw - 90):
                text_rtl(d, (x1 - 45, y), ln, lf, anchor='ra')
                y += 66
            y += 22
        text_rtl(d, (x1 - 45, 850), src, font(28, '500Medium'), fill=(170, 180, 198), anchor='rm')
    if foot:
        cf = font(30, '700Bold')
        cw = tsize(d, foot, cf)[0]
        d.rounded_rectangle([W / 2 - cw / 2 - 24, 950, W / 2 + cw / 2 + 24, 1008], 10, fill=(60, 66, 82))
        text_c(d, (W / 2, 979), foot, cf, fill=GOLD)
    return save(im, name)


def intro_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    text_c(d, (W / 2, 470), 'من صُلب الواقع', font(150, '900Black'))
    d.rectangle([W / 2 - 140, 600, W / 2 + 140, 612], fill=RED)
    text_c(d, (W / 2, 690), 'حيث نقرأ ما وراء الخبر', font(56, '600SemiBold'), fill=(205, 212, 226))
    return save(im, name)


def section_card(name, num, title, sub):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    text_c(d, (W / 2, 360), num, font(120, '900Black'), fill=RED)
    text_c(d, (W / 2, 540), title, font(100, '900Black'))
    d.rectangle([W / 2 - 120, 650, W / 2 + 120, 660], fill=RED)
    text_c(d, (W / 2, 740), sub, font(44, '600SemiBold'), fill=(190, 198, 212))
    return save(im, name)


def point_card(name, num, title, lines, note=None):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    d.ellipse([W - 400, 250, W - 160, 490], fill=RED)
    text_c(d, (W - 280, 372), num, font(140, '900Black'))
    text_rtl(d, (W - 460, 300), title, font(96, '900Black'), anchor='ra')
    y = 560
    lf = font(52, '600SemiBold')
    for ln0 in lines:
        for ln in wrap(d, ln0, lf, W - 500):
            text_rtl(d, (W - 160, y), ln, lf, fill=(220, 226, 236), anchor='ra')
            y += 84
        y += 20
    if note:
        cf = font(30, '700Bold')
        cw = tsize(d, note, cf)[0]
        d.rounded_rectangle([140, H - 150, 140 + cw + 44, H - 94], 10, fill=(60, 66, 82))
        text_c(d, (140 + (cw + 44) / 2, H - 121), note, cf, fill=GOLD)
    return save(im, name)


def statement_card(name, small, big, sub):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    text_c(d, (W / 2, 330), small, font(56, '700Bold'), fill=(190, 198, 212))
    bf = font(110, '900Black')
    y = 470
    for ln in wrap(d, big, bf, W - 300):
        text_c(d, (W / 2, y), ln, bf)
        y += 150
    d.rectangle([W / 2 - 120, y - 30, W / 2 + 120, y - 20], fill=RED)
    sf = font(56, '800ExtraBold')
    for ln in wrap(d, sub, sf, W - 400):
        text_c(d, (W / 2, y + 60), ln, sf, fill=GOLD)
        y += 90
    return save(im, name)


SCEN = [('السيناريو الأول', 'الاحتواء', 'مواجهة محدودة وضغط دبلوماسي في مجلس الأمن يمنع الانزلاق', GREEN),
        ('السيناريو الثاني', 'حرب استنزاف حدودية', 'اشتباكات متقطعة وضربات بالمسيّرات دون إعلان حرب صريح', GOLD),
        ('السيناريو الثالث · الأخطر', 'حرب مباشرة وشاملة', 'تهديد استقرار القرن الإفريقي وممرات الملاحة في البحر الأحمر', RED)]


def scenario_card(name, active):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    text_c(d, (W / 2, 130), 'إلى أين يتّجه المشهد؟', font(66, '900Black'))
    d.rectangle([W / 2 - 90, 190, W / 2 + 90, 198], fill=RED)
    for i, (k, t, sub, col) in enumerate(SCEN):
        y0 = 250 + i * 262
        on = i == active
        fill = (18, 30, 56, 245) if on else (14, 20, 36, 200)
        d.rounded_rectangle([200, y0, W - 200, y0 + 228], 16, fill=fill, outline=col if on else (60, 66, 82), width=4 if on else 2)
        d.rectangle([W - 220, y0 + 20, W - 206, y0 + 195], fill=col if on else (70, 76, 92))
        a = 255 if on else 110
        text_rtl(d, (W - 250, y0 + 30), k, font(32, '700Bold'), fill=col + (a,), anchor='ra')
        text_rtl(d, (W - 250, y0 + 78), t, font(56, '900Black'), fill=(255, 255, 255, a), anchor='ra')
        text_rtl(d, (W - 250, y0 + 148), sub, font(34, '500Medium', 'plex'), fill=(200, 206, 218, a), anchor='ra')
    return save(im, name)


def reuters_card(name):
    return headline_card(name, 'رويترز', 'تقرير حديث',
                         'قوات حكومية إثيوبية وميليشيات متحالفة معها تدخل مدينة أديغرات الاستراتيجية القريبة من الحدود مع إريتريا',
                         [], label='ميداني', chip_txt='بحسب تقرير لوكالة رويترز')


def summary_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    kicker(d, 'الخلاصة', y=120)
    rows = [('توغّل إريتري بعمق 60 كم', 'بحسب تقارير · إريتريا تنفي'),
            ('ضربات بالمسيّرات', 'نُسبت للجيش الإثيوبي'),
            ('دخول أديغرات', 'قوات إثيوبية وميليشيات متحالفة · رويترز'),
            ('تحذير أمام مجلس الأمن', 'إثيوبيا تتمسّك بحق الدفاع عن النفس'),
            ('في العمق', 'منفذ البحر الأحمر · توترات تيغراي وعفر وأمهرة')]
    y = 250
    for t, s_ in rows:
        d.rectangle([W - 172, y + 18, W - 160, y + 88], fill=RED)
        text_rtl(d, (W - 200, y), t, font(54, '800ExtraBold'), anchor='ra')
        text_rtl(d, (W - 200, y + 76), s_, font(34, '500Medium', 'plex'), fill=(185, 194, 210), anchor='ra')
        y += 150
    return save(im, name)


def end_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    kicker(d, 'سؤال الحلقة', y=150)
    qf = font(70, '900Black')
    y = 290
    for ln in ['هل تتحول المعارك إلى حرب مباشرة وشاملة', 'بين إثيوبيا وإريتريا؟']:
        text_rtl(d, (W - 160, y), ln, qf, anchor='ra'); y += 110
    text_rtl(d, (W - 160, y + 40), 'أم تنجح الضغوط الدولية في احتوائها؟', font(54, '600SemiBold'), fill=(205, 212, 226), anchor='ra')
    cf = font(40, '700Bold')
    t = 'شاركونا آراءكم في التعليقات'
    cw = tsize(d, t, cf)[0]
    d.rounded_rectangle([W - 160 - cw - 60, 700, W - 160, 780], 12, fill=RED)
    text_c(d, (W - 160 - (cw + 60) / 2, 740), t, cf)
    t2 = 'اشترك · فعّل الجرس'
    cw2 = tsize(d, t2, cf)[0]
    d.rounded_rectangle([W - 160 - cw2 - 60, 810, W - 160, 890], 12, fill=(40, 48, 66))
    text_c(d, (W - 160 - (cw2 + 60) / 2, 850), t2, cf, fill=GOLD)
    text_c(d, (W / 2 - 300, 1010), 'من صُلب الواقع', font(30, '700Bold'), fill=(150, 160, 180))
    return save(im, name)


def counter(name, items, dur, src, title=None):
    """items: list of (value, label, start_s). Renders mp4."""
    bg = navy_bg()
    n = int(round(dur * FPS))
    out = os.path.join(OUT, name + '.mp4')
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16',
                           '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    k = len(items)
    for i in range(n):
        t = i / FPS
        im = bg.copy()
        d = ImageDraw.Draw(im)
        if title:
            text_c(d, (W / 2, 170), title, font(52, '800ExtraBold'))
            d.rectangle([W / 2 - 80, 215, W / 2 + 80, 223], fill=RED)
        for j, (val, lab, st) in enumerate(items):
            cx = W / 2 if k == 1 else (W * (0.72 - 0.44 * j / (k - 1)))
            e = ease((t - st) / 1.6)
            if t < st:
                continue
            a = int(255 * ease((t - st) / 0.4))
            v = int(round(val * e))
            text_c(d, (cx, 470), f'{v:,}'.replace(',', '٬') if val >= 10000 else str(v),
                   font(230 if k == 1 else 190, '900Black'), fill=WHITE + (a,))
            d.rectangle([cx - 90, 610, cx + 90, 620], fill=RED + (a,))
            for li, ln in enumerate(lab.split('\n')):
                text_c(d, (cx, 690 + li * 66), ln, font(52 if li == 0 else 38, '700Bold' if li == 0 else '500Medium'),
                       fill=(WHITE if li == 0 else (196, 204, 220)) + (a,))
        text_c(d, (W / 2, H - 110), src, font(30, '500Medium'), fill=(180, 190, 206, 255))
        ff.stdin.write(im.convert('RGB').tobytes())
    ff.stdin.close(); ff.wait()
    return out


if __name__ == '__main__':
    intro_card('intro')
    reuters_card('reuters')
    two_col('positions', 'روايتان متناقضتان',
            ('إثيوبيا', (30, 90, 180), ['وجّهت تحذيراً إلى مجلس الأمن بشأن التوغّل الإريتري', 'تتمسّك بحق الدفاع عن النفس'], 'الموقف الإثيوبي المعلن'),
            ('إريتريا', (170, 30, 45), ['تنفي الاتهامات', 'تعتبرها محاولة لتبرير عدوان إثيوبي محتمل'], 'الموقف الإريتري المعلن'),
            foot='كل طرف يبني ملفاً سياسياً ودبلوماسياً تحسّباً لما هو قادم')
    section_card('sec1', 'أولاً', 'القراءة الميدانية', 'أربع دلالات للتصعيد')
    point_card('p1', '١', 'عمق التوغّل', ['60 كم ليست حادثاً حدودياً عابراً', 'بل وجود عسكري في عمق الأراضي الإثيوبية'], note='إن صحّت التقارير · إريتريا تنفي')
    point_card('p2', '٢', 'سلاح المسيّرات', ['الردّ من الجو أولاً: أقل كلفة', 'لكنه يفتح باب التصعيد'], note='الضربات نُسبت للجيش الإثيوبي')
    point_card('p3', '٣', 'دخول أديغرات', ['من الضربات المحدودة', 'إلى فرض أمر واقع على الأرض'])
    point_card('p4', '٤', 'الميليشيات المتحالفة', ['قوى غير نظامية إلى جانب الجيش', 'ضبطها أصعب · وحساباتها قد لا تتطابق مع حسابات الدولة'])
    section_card('sec2', 'ثانياً', 'التحليل الجيوسياسي', 'ما وراء خطوط التماس')
    statement_card('notborder', 'الخطأ الأكبر: قراءة ما يجري على أنه', 'مجرد خلاف حدودي', 'الملف الأعمق: سعي إثيوبيا إلى منفذ على البحر الأحمر')
    for i in range(3):
        scenario_card(f'scen{i + 1}', i)
    summary_card('summary')
    end_card('end')
