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


def guest_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    kicker(d, 'قراءة عسكرية', y=200)
    text_rtl(d, (W - 160, 360), 'اللواء الدكتور فايز الدويري', font(96, '900Black'), anchor='ra')
    d.rectangle([W - 160 - 10, 520, W - 160, 600], fill=RED)
    text_rtl(d, (W - 200, 560), 'خبير عسكري واستراتيجي', font(52, '600SemiBold'), fill=(205, 212, 226), anchor='rm')
    text_rtl(d, (W - 160, 700), 'مداخلة صوتية · 5 أكتوبر 2026', font(38, '500Medium'), fill=(160, 170, 188), anchor='ra')
    # sound-wave motif
    import math
    for i in range(60):
        h = 30 + 90 * abs(math.sin(i * 0.55) * math.cos(i * 0.17))
        x = 200 + i * 16
        d.rounded_rectangle([x, 760 - h / 2, x + 8, 760 + h / 2], 4, fill=(200, 22, 38, 200))
    return save(im, name)


def end_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    text_c(d, (W / 2, 250), 'تحوّل في مراحله الأولى', font(92, '900Black'))
    d.rectangle([W / 2 - 100, 330, W / 2 + 100, 340], fill=RED)
    pf = font(40, '600SemiBold')
    rows = ['الحكومة تعلن السيطرة على المخا وذوباب · والحوثيون ينفون',
            'لا تحقق مستقلاً من الأرقام المعلنة حتى الآن',
            'المعارك مستمرة في تعز والساحل الغربي']
    y = 430
    for r in rows:
        text_c(d, (W / 2, y), r, pf)
        y += 90
    sf = font(26, '500Medium')
    text_c(d, (W / 2, 820), 'المصادر: سكاي نيوز عربية · الجزيرة نت · العربي الجديد · وكالة سبأ · المصدر أونلاين · قناة المسيرة · رويترز (عبر وسائل إعلام)', sf, fill=(170, 180, 198))
    text_c(d, (W / 2, 880), 'شاركونا قراءتكم في التعليقات', font(40, '700Bold'), fill=GOLD)
    return save(im, name)


def question_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    kicker(d, 'سؤال الحلقة', y=180)
    qf = font(70, '800ExtraBold')
    text_rtl(d, (W - 160, 330), 'تغيّر طويل الأمد في خريطة السيطرة', qf, anchor='ra')
    text_rtl(d, (W - 160, 440), 'على الساحل الغربي؟', qf, anchor='ra')
    text_rtl(d, (W - 160, 600), 'أم أن التحركات المضادة قد تغيّر المشهد من جديد؟', font(54, '600SemiBold'),
             fill=(205, 212, 226), anchor='ra')
    cf = font(38, '700Bold')
    t = 'شاركونا قراءتكم في التعليقات'
    cw = tsize(d, t, cf)[0]
    d.rounded_rectangle([W - 160 - cw - 60, 780, W - 160, 856], 12, fill=RED)
    text_c(d, (W - 160 - (cw + 60) / 2, 818), t, cf)
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
    headline_card('H_sky_mokha', 'سكاي نيوز عربية', '5 أكتوبر 2026',
                  'القوات الحكومية اليمنية تعلن السيطرة على مدينة المخا',
                  ['«القوات تمكنت، بإسناد جوي، من السيطرة على مدينة المخا الواقعة على ساحل البحر الأحمر غربي اليمن»',
                   '— مصدر عسكري لوكالة الأنباء اليمنية «سبأ»'],
                  chip_txt='رويترز: تعذّر التحقق بشكل مستقل من حجم التقدم')
    headline_card('H_masirah_deny', 'قناة المسيرة', '5 أكتوبر 2026',
                  'مصدر عسكري ينفي مزاعم العدو بخصوص ذوباب وباب المندب', [], label='رواية الحوثيين')
    points_card('P_sources', 'أرقام منسوبة إلى مصادرها', 'من أعلن ماذا؟',
                ['100 طائرة مقاتلة و324 هدفاً — وزارة الدفاع السعودية',
                 '1122 عملية استهداف — المتحدث باسم القوات المسلحة اليمنية',
                 'السيطرة على المخا — مصدر عسكري لوكالة سبأ'],
                'سكاي نيوز عربية · الجزيرة نت · 5 أكتوبر 2026', note='لا تحقق مستقلاً من هذه الأرقام')
    points_card('P_bukhaiti', 'محمد البخيتي · قيادي في أنصار الله', 'الموقف الحوثي بحسب ما نُقل عنه',
                ['رفض الأنباء عن تقدم القوات الحكومية',
                 'التأكيد على امتلاك الجماعة «قدرات رادعة»',
                 'التحذير من ضربات قد تستهدف منشآت حيوية داخل السعودية'],
                'تصريحات متداولة · 4–5 أكتوبر 2026', note='لم نعثر على النص الحرفي للتصريح')
    two_col('T_narratives', 'روايتان متباينتان من تعز',
            ('الرواية الحكومية', (30, 80, 160), ['كمين في منطقة البيرين غرب تعز', 'فرار عناصر حوثية من إحدى الجبهات'],
             'المصدر أونلاين · 5 أكتوبر'),
            ('رواية الحوثيين', RED, ['«دحر تحشيدات العدو السعودي» من التربة والشمايتين وسامع'],
             'قناة المسيرة · 4 أكتوبر'),
            foot='من المبكر الجزم بحدود هذه التحركات')
    two_col('T_dhubab', 'ذوباب: إعلان ونفي',
            ('إعلان الحكومة', (30, 80, 160), ['السيطرة على مطار ذوباب ومواقع استراتيجية', 'تأمين الطريق بين ذوباب والمخا'],
             'وكالة سبأ · 5 أكتوبر'),
            ('رد الحوثيين', RED, ['مصدر عسكري ينفي «مزاعم العدو» بخصوص ذوباب وباب المندب'], 'قناة المسيرة · 5 أكتوبر'),
            foot='لم يتسنَّ التحقق بصورة مستقلة')
    question_card('Q_episode')
    guest_card('G_guest')
    end_card('E_end')
    QK = 'اللواء د. فايز الدويري · خبير عسكري'
    quote_card('Q1_early', QK, 'من المبكر أن نقول ذلك.. المعارك تتركز بصورة أساسية حول تعز', 'فايز الدويري')
    quote_card('Q2_service', QK, 'إذا أخذنا بتصريحات الجانب اليمني، فهذا يقدّم خدمة استراتيجية رئيسية للقوات الشرعية',
               'فايز الدويري', note='الحوثيون ينفون')
    quote_card('Q3_realistic', QK, 'يجب أن نكون واقعيين.. الحديث مبكر جداً عن حسم المعركة بصورة نهائية', 'فايز الدويري')
    quote_card('Q4_air', QK, 'الضربات الجوية لن تحسم المعركة.. لكنها تسهّل المعركة', 'فايز الدويري')
    quote_card('Q5_achieve', QK, 'لا أقلل من إنجازهم.. هذا إنجاز تحوّل يُسجَّل لرشاد العليمي', 'فايز الدويري')
    quote_card('Q6_intl', QK, 'يبعث رسائل سياسية وعسكرية متزامنة.. وبالأمس طلب مساعدة دولية لمساعدة القوات اليمنية',
               'فايز الدويري', note='بحسب الضيف')
    quote_card('Q7_command', QK, 'القيادة والسيطرة في جماعة الحوثي بمستوى عالٍ.. لكن القدرات الميدانية تفرض ذاتها', 'فايز الدويري')
    quote_card('Q8_shift', QK, 'إذا استمرت القوات الحكومية بهذا الزخم يمكن أن نتحدث عن تحوّل.. لكنه في مراحله الأولى', 'فايز الدويري')
    counter('N_100', [(100, 'طائرة مقاتلة\nشاركت في الهجمات', 0.3)], 6.5, 'المصدر: وزارة الدفاع السعودية · 5 أكتوبر 2026')
    counter('N_324', [(324, 'هدفاً «عالي القيمة»\nدُمّرت بحسب الإعلان', 0.3)], 10, 'المصدر: وزارة الدفاع السعودية · 5 أكتوبر 2026')
    counter('N_1122', [(1122, 'عملية استهداف\nفي صعدة والجوف وتعز والساحل', 0.3), (1747, 'عنصراً حوثياً\n«تم تحييدهم» بحسب البيان', 1.4)],
            7, 'المصدر: المتحدث باسم القوات المسلحة اليمنية (الحكومة) · 5 أكتوبر 2026', title='بيان القوات الحكومية')
    counter('N_100_324', [(100, 'طائرة\n«لا نقول 100 طلعة»', 0.3), (324, 'هدفاً عالي القيمة\nصباح 5 أكتوبر', 1.2)],
            11, 'أرقام وزارة الدفاع السعودية كما استشهد بها الضيف', title='كثافة الإسناد الجوي')
    print('cards done')
