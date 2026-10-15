"""Map specs — Morocco / Spain (coordinates: OpenStreetMap / standard city centres)."""
from common import RED, BLUE, GOLD, GREEN, GREY, WHITE

MOR = (96, 42, 48)
SPA = (42, 58, 96)
POR = (52, 60, 80)
HL = {'MAR': MOR, 'SAH': MOR, 'ESP': SPA}
DASH = ['SAH']

L = {
    'rabat': (-6.8416, 34.0209), 'madrid': (-3.7038, 40.4168), 'marrakech': (-7.9811, 31.6295),
    'casablanca': (-7.5898, 33.5731), 'berrechid': (-7.5873, 33.2655), 'ceuta': (-5.3213, 35.8894),
    'melilla': (-2.9381, 35.2923), 'gibraltar': (-5.3536, 36.1408), 'tangier': (-5.8340, 35.7595),
    'tetouan': (-5.3684, 35.5785), 'algeciras': (-5.4562, 36.1408), 'barcelona': (2.1686, 41.3874),
    'lisbon': (-9.1393, 38.7223), 'seville': (-5.9845, 37.3891), 'bilbao': (-2.9350, 43.2630),
    'valencia': (-0.3763, 39.4699), 'algiers': (3.0588, 36.7538), 'paris': (2.3522, 48.8566),
    'rota': (-6.3497, 36.6200), 'moron': (-5.6150, 37.1747), 'albacete': (-1.8635, 38.9484),
    'las_palmas': (-15.4134, 28.1235),
}
SEA = [('المحيط الأطلسي', -14.0, 37.0, 40), ('البحر المتوسط', 4.5, 38.3, 40)]


SPECS = [
    # 0:00 hook — Rabat→Madrid 764 km, then the 2,000 km ring from Marrakech
    dict(name='mA_hook', dur=26, view0=(-4.6, 36.6, 25.0), view1=(-3.5, 35.2, 52.0), zoom_t=(8.0, 13.5),
         hl_countries=HL, admin_of=[], dashed_countries=DASH, roads=False,
         bglabels=[('المغرب', -6.8, 32.2, 44), ('إسبانيا', -3.2, 39.2, 44)] + SEA,
         pins=[dict(ll=L['rabat'], name='الرباط', t=0.4, big=True), dict(ll=L['madrid'], name='مدريد', t=1.0, big=True, color=BLUE, side='r'),
               dict(ll=L['marrakech'], name='مراكش', t=15.8, big=True),
               dict(ll=L['barcelona'], name='برشلونة', t=19.0, color=BLUE, side='r'), dict(ll=L['lisbon'], name='لشبونة', t=19.6, color=BLUE),
               dict(ll=L['paris'], name='باريس ~2100 كم', t=20.4, color=GREY, side='r')],
         paths=[dict(pts=[L['rabat'], L['madrid']], t0=1.4, t1=3.4, color=WHITE, arrow=False, width=6, label='764 كم', loff=(-90, 0))],
         rings=[dict(ll=L['marrakech'], km=2000, t=9.0, color=RED, label='مدى 2000 كم (معلن)')],
         chips=[dict(t=3.6, txt='المسافة بحسب «إل إسبانيول»', col=(70, 80, 100))],
         title='764 كم.. ودائرة بقطر 4000', sub='الرباط – مدريد · مدى IRIFI المعلن',
         src='خريطة توضيحية · المسافات في خط مستقيم'),
    # Marrakech Air Show location + Rabat/Casablanca
    dict(name='mB_marrakech', dur=14, view0=(-7.0, 32.9, 9.0), view1=(-7.2, 32.95, 6.6), zoom_t=(0, 10),
         hl_countries=HL, admin_of=['MAR'], dashed_countries=DASH,
         bglabels=[('المحيط الأطلسي', -9.6, 32.6, 34)],
         pins=[dict(ll=L['marrakech'], name='مراكش · القاعدة الجوية', t=0.5, big=True),
               dict(ll=L['casablanca'], name='الدار البيضاء', t=1.5, side='r')],
         chips=[dict(t=2.5, txt='الدورة الثامنة · 7–10 أكتوبر 2026')],
         title='معرض مراكش الدولي للطيران', sub='نحو 200 عارض من 27 دولة'),
    # Moroccan defence-industry map: Rabat R&D, Casablanca IRIFI plant, Berrechid WhAP plant
    dict(name='mC_industry', dur=22, view0=(-6.95, 33.75, 3.6),
         hl_countries=HL, admin_of=['MAR'], dashed_countries=DASH,
         bglabels=[('المحيط الأطلسي', -8.6, 34.1, 32)],
         pins=[dict(ll=L['rabat'], name='الرباط · مركز بحث وتطوير (Harmattan AI)', t=0.6, big=True, side='r'),
               dict(ll=L['casablanca'], name='قرب الدار البيضاء · مصنع IRIFI المخطط', t=4.0, big=True, color=GOLD, side='r'),
               dict(ll=L['berrechid'], name='برشيد · تجميع مدرعات WhAP 8x8', t=8.0, big=True, color=BLUE, side='r')],
         chips=[dict(t=11.0, txt='مشروعات معلنة · مراحل مختلفة من التنفيذ', col=(70, 80, 100))],
         title='خريطة الصناعة الدفاعية الناشئة', sub='مشروعات أُعلنت في 2025–2026',
         src='خريطة توضيحية · المواقع تقريبية · Assahifa / Infodefensa / Harmattan AI'),
    # Ceuta naval frictions
    dict(name='mD_ceuta', dur=24, view0=(-5.45, 35.95, 1.6), view1=(-5.38, 35.9, 1.1), zoom_t=(0, 16),
         hl_countries=HL, admin_of=[], dashed_countries=DASH,
         bglabels=[('مضيق جبل طارق', -5.62, 36.03, 30)],
         areas=[dict(poly=[(-5.40, 35.86), (-5.26, 35.86), (-5.22, 35.93), (-5.34, 35.96), (-5.42, 35.92)], color=GOLD, alpha=80, t=4.0,
                     label='مياه سبتة')],
         pins=[dict(ll=L['ceuta'], name='سبتة', t=0.5, big=True, color=BLUE, side='r'),
               dict(ll=L['gibraltar'], name='جبل طارق', t=1.2, color=GREY), dict(ll=L['tangier'], name='طنجة', t=1.6),
               dict(ll=L['tetouan'], name='تطوان', t=2.0), dict(ll=L['algeciras'], name='الجزيرة الخضراء', t=2.4, color=BLUE)],
         chips=[dict(t=6.0, txt='«إل باييس» (عبر AFP): فرقاطة وزوارق مغربية · يوليو–أغسطس 2026'),
                dict(t=9.0, txt='الرواية المغربية الرسمية غير متاحة', col=(70, 80, 100))],
         title='احتكاكات بحرية قرب سبتة', sub='صيف 2026'),
    # West Med balance / Strait
    dict(name='mE_westmed', dur=24, view0=(-4.5, 36.4, 15.0), view1=(-5.0, 36.2, 11.0), zoom_t=(0, 18),
         hl_countries=HL, admin_of=[], dashed_countries=DASH,
         bglabels=[('المغرب', -6.5, 32.6, 40), ('إسبانيا', -3.6, 39.6, 40), ('البحر المتوسط', 1.6, 37.6, 34), ('الجزائر', 1.5, 33.6, 32)],
         pins=[dict(ll=L['gibraltar'], name='مضيق جبل طارق', t=0.5, big=True, color=GOLD),
               dict(ll=L['rota'], name='روتا · قاعدة بحرية', t=3.0, color=BLUE),
               dict(ll=L['moron'], name='مورون · قاعدة جوية', t=3.6, color=BLUE, side='r'),
               dict(ll=L['ceuta'], name='سبتة', t=4.2, color=BLUE, side='r'), dict(ll=L['melilla'], name='مليلية', t=4.6, color=BLUE, side='r'),
               dict(ll=L['rabat'], name='الرباط', t=5.2)],
         chips=[dict(t=6.5, txt='إسبانيا: تفوق بحري ومظلة الناتو', col=(30, 70, 140))],
         title='غرب المتوسط', sub='معادلة تتغير؟'),
]
