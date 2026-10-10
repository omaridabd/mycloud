"""Map specs — Horn of Africa. Coordinates approximate (town centres), for illustration."""
import json, os
from common import RED, BLUE, GOLD, GREEN, GREY, WHITE, ROOT

L = {'adigrat': (39.462, 14.277), 'mekelle': (39.475, 13.497), 'asmara': (38.932, 15.339),
     'addis': (38.74, 9.03), 'bab': (43.35, 12.62)}
ETHC = (58, 64, 80)
ERIC = (78, 58, 62)
HL = {'ETH': ETHC, 'ERI': ERIC}
REG = [('إثيوبيا', 39.5, 8.6, 60), ('إريتريا', 38.4, 16.3, 44), ('البحر الأحمر', 39.9, 18.2, 40),
       ('السودان', 33.8, 15.0, 44), ('جيبوتي', 42.7, 11.0, 32), ('الصومال', 46.3, 7.5, 44), ('اليمن', 45.5, 15.6, 44),
       ('خليج عدن', 47.0, 12.4, 34)]
ERI_C = (180, 60, 70)


def tigray_border():
    """Shared Eritrea–Ethiopia boundary west of 40.05E (Tigray sector), in ring order, west->east."""
    cf = json.load(open(os.path.join(ROOT, 'maps', 'data', 'countries_reg.json')))['features']
    def big_ring(code):
        g = [x for x in cf if x['properties']['ADM0_A3'] == code][0]['geometry']
        rings = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        return max(rings, key=lambda r: len(r[0]))[0]
    eri, eth = big_ring('ERI'), big_ring('ETH')
    es = set((round(x, 3), round(y, 3)) for x, y in eth)
    pts = [tuple(p) for p in eri if (round(p[0], 3), round(p[1], 3)) in es and p[0] <= 40.05]
    if pts[0][0] > pts[-1][0]:
        pts = pts[::-1]
    return pts


BORDER = tigray_border()
DEPTH = 60 / 111.0
BAND = BORDER + [(lo, la - DEPTH) for lo, la in reversed(BORDER)]
LANE = [(33.6, 27.6), (35.6, 24.2), (37.8, 20.6), (39.9, 17.0), (41.8, 14.2), (43.0, 12.95), (43.45, 12.55), (45.2, 12.15)]

SPECS = [
    dict(name='mapA_horn', dur=10, view0=(40.5, 12.5, 26), view1=(39.4, 14.3, 5.5), zoom_t=(1.0, 7.5),
         hl_countries=HL, bglabels=REG,
         pins=[dict(ll=L['adigrat'], name='أديغرات', t=6.5, big=True)],
         title='القرن الإفريقي', sub='إثيوبيا وإريتريا · خط التماس في تيغراي'),
    dict(name='mapB_adigrat', dur=12, view0=(39.1, 14.45, 5.0), view1=(39.25, 14.4, 4.0),
         hl_countries=HL, bglabels=[('إريتريا', 38.5, 15.2, 40), ('إقليم تيغراي', 38.6, 13.75, 36)],
         admin_areas=[dict(name='Tigray', color=(150, 16, 30), alpha=70, t=0.3)],
         pins=[dict(ll=L['adigrat'], name='أديغرات', t=0.8, big=True),
               dict(ll=L['asmara'], name='أسمرة', t=1.6, side='r', color=GREY),
               dict(ll=L['mekelle'], name='مقلي', t=2.0, side='r', color=GREY)],
         chips=[dict(t=3.0, txt='رويترز: قوات إثيوبية وميليشيات متحالفة تدخل أديغرات', col=(30, 70, 140))],
         title='أديغرات', sub='شمال تيغراي · قرب الحدود مع إريتريا'),
    dict(name='mapC_depth', dur=13, view0=(38.4, 14.3, 5.8), view1=(38.5, 14.2, 4.8),
         hl_countries=HL, bglabels=[('إريتريا', 38.2, 15.6, 40), ('إقليم تيغراي', 38.4, 13.2, 36)],
         admin_areas=[dict(name='Tigray', color=(120, 20, 30), alpha=50, t=0.2)],
         bands=[dict(poly=BAND, color=ERI_C, alpha=110, t=1.5)],
         paths=[dict(pts=BORDER, t0=0.4, t1=1.8, color=GOLD, width=6, arrow=False),
                dict(pts=[(38.62, 14.46), (38.62, 14.46 - DEPTH)], t0=3.0, t1=4.2, color=WHITE, width=6,
                     label='60 كم', loff=(-90, 0))],
         chips=[dict(t=5.0, txt='توغّل بعمق 60 كم داخل تيغراي · بحسب تقارير'),
                dict(t=6.5, txt='إريتريا تنفي', col=(70, 70, 80))],
         legend=[(GOLD, 'الحدود الإثيوبية–الإريترية'), (ERI_C, 'نطاق عمق 60 كم (توضيحي)')],
         title='التوغّل الإريتري', sub='بحسب التقارير', src='توضيح لعمق التوغّل فقط · لا يمثّل مواقع محددة للقوات'),
    dict(name='mapD_sequence', dur=14, view0=(39.0, 14.3, 4.2), view1=(39.2, 14.3, 3.4),
         hl_countries=HL, bglabels=[('إريتريا', 38.4, 15.4, 40), ('إقليم تيغراي', 38.5, 13.6, 36)],
         admin_areas=[dict(name='Tigray', color=(120, 20, 30), alpha=50, t=0.2)],
         bands=[dict(poly=BAND, color=ERI_C, alpha=70, t=0.6)],
         pins=[dict(ll=L['adigrat'], name='أديغرات', t=7.5, big=True)],
         chips=[dict(t=1.0, txt='١ · توغّل إريتري بعمق 60 كم (تقارير)'),
                dict(t=3.8, txt='٢ · ضربات بمسيّرات نُسبت للجيش الإثيوبي', col=(150, 90, 10)),
                dict(t=6.6, txt='٣ · قوات إثيوبية تدخل أديغرات (رويترز)', col=(30, 70, 140))],
         title='تسلسل التصعيد', sub='من التوغّل إلى التقدّم البرّي'),
    dict(name='mapE_redsea', dur=14, view0=(40.5, 14.5, 15), view1=(40.8, 14.0, 12), 
         hl_countries={'ETH': ETHC, 'ERI': (110, 60, 66)},
         bglabels=[('إثيوبيا · دولة بلا ساحل', 39.2, 9.3, 44), ('إريتريا', 38.2, 16.0, 38),
                   ('البحر الأحمر', 39.4, 18.6, 40), ('اليمن', 45.0, 15.6, 40), ('جيبوتي', 42.6, 11.3, 30)],
         paths=[dict(pts=LANE, t0=1.5, t1=6.0, color=GOLD, dash=True, width=7, arrow=False),
                dict(pts=[(39.6, 11.0), (40.6, 12.6), (41.4, 13.6)], t0=7.0, t1=9.0, color=BLUE, width=8,
                     label='طموح الوصول إلى البحر', loff=(-60, 70))],
         pins=[dict(ll=L['bab'], name='باب المندب', t=4.0, color=GOLD, side='r')],
         chips=[dict(t=9.5, txt='أديس أبابا: منفذ البحر مسألة استراتيجية', col=(30, 70, 140)),
                dict(t=11.0, txt='أسمرة: تنظر إليه بعين الريبة', col=(150, 30, 40))],
         legend=[(GOLD, 'ممرات الملاحة في البحر الأحمر')],
         title='معركة المنفذ البحري', sub='البعد الأعمق للتصعيد', src='خريطة توضيحية · السهم يرمز للطموح لا لمسار محدد'),
    dict(name='mapF_regions', dur=15, view0=(39.6, 12.4, 10.5), view1=(39.6, 12.4, 9.5),
         hl_countries=HL, bglabels=[('إريتريا', 38.0, 16.0, 36), ('البحر الأحمر', 40.6, 16.9, 34)],
         admin_areas=[dict(name='Tigray', color=(190, 30, 45), alpha=120, t=0.8, label='تيغراي', lab_ll=(38.9, 13.9)),
                      dict(name='Afar', color=(220, 150, 30), alpha=120, t=2.4, label='عفر', lab_ll=(40.9, 12.0)),
                      dict(name='Amhara', color=(40, 110, 210), alpha=120, t=4.0, label='أمهرة', lab_ll=(38.2, 11.4))],
         pins=[dict(ll=L['addis'], name='أديس أبابا', t=0.3, side='r', color=GREY)],
         chips=[dict(t=6.0, txt='توترات داخلية في الأقاليم الثلاثة')],
         title='جبهة الداخل', sub='تيغراي · عفر · أمهرة'),
    dict(name='mapG_scenario', dur=14, view0=(41.0, 15.5, 24), view1=(41.0, 15.0, 20),
         hl_countries={'ETH': (64, 52, 66), 'ERI': (135, 42, 52)}, bglabels=REG,
         paths=[dict(pts=LANE, t0=2.0, t1=6.5, color=RED, dash=True, width=7, arrow=False),
                dict(pts=BORDER, t0=0.5, t1=1.5, color=GOLD, width=7, arrow=False)],
         pins=[dict(ll=L['bab'], name='باب المندب', t=5.0, color=RED, side='r', big=True)],
         chips=[dict(t=7.0, txt='استقرار القرن الإفريقي'), dict(t=8.5, txt='ممرات الملاحة في البحر الأحمر')],
         title='السيناريو الأخطر', sub='حرب مباشرة وشاملة بين الدولتين'),
]
