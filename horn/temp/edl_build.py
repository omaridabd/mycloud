"""Scene plan -> temp/edl.json. Times are narration seconds (full_words.json timeline)."""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
AUDIO_LEN = 337.35
SHIFT_AT, SHIFT = 198.4, -0.242   # splice of patched sentence (c04) shortened the timeline after ~198 s
def T(t):
    return round(t + (SHIFT if t > SHIFT_AT else 0), 3)

def cm(prefix):
    g = sorted(glob.glob('downloads/cm/cm_' + prefix + '*'))
    if not g:
        raise SystemExit('missing ' + prefix)
    return g[0]
TROOPS = cm('Eritrean_troops_leaving')
MOURN = cm('A_day_of_mourning')
REMEM = cm('Tigray_remembers')
IDP = cm('IDPs_in_Tigray')
FIGHT = cm('Former_Tigray_fighters')
ADI1 = cm('Adigrat_Street'); ADI2 = cm('Adigrat_Ethiopia_49088955653'); BUS = cm('Bus_to_Adigrat')
ESC = cm('Tigray_Escarpment'); TLAND = cm('Tigray_Landscape_53009331742')
UNSC1 = cm('UN_Security_Council_2018'); UNSC2 = cm('UN_Security_Council_Nov_16_2023'); UNSC3 = cm('Inside_the_UN_Security_Council')
ASSAB = cm('Assab_Eritrea'); BAB = cm('Bab_Al_Mandeb_Strait_between'); AFAR = cm('ET_Afar_asv2018_01_img46'); GOND = cm('ET_Gondar_asv2018_02')
G = 'downloads/gen/'; M = 'maps/'; C = 'graphics/cards/'
VOA = 'VOA (صوت أمريكا) · ملكية عامة · ويكيميديا'
def cr(path):
    m = json.load(open('downloads/cm/meta.json')).get(path, {})
    a = (m.get('artist') or '').strip().replace('\n', ' ')[:40]
    lic = m.get('lic', '')
    return f'{a} · {lic} · ويكيميديا كومنز' if a else f'{lic} · ويكيميديا كومنز'
BADGE = ('badge', '', 0, None)
AI = ('ai', '', 0, None)
def arch(txt): return ('archive', txt, 0.2, None)
def cap(txt, a=0.4, b=None): return ('cap', txt, a, b)
def credit(txt): return ('credit', txt, 0.3, None)

S = []
def add(t0, src, kind, tin=0, ov=(), **kw):
    S.append(dict(t0=T(t0), src=src, kind=kind, tin=tin, ov=list(ov), **kw))

# ---- hook
add(0.0, G + 'ai5_flashes.mp4', 'video', 0, [AI, ('hook', '60 كم|توغّل إريتري داخل تيغراي · بحسب تقارير', 0.3, None)], fixed=True)
add(4.2, TROOPS, 'video', 137, [arch('مشاهد أرشيفية · قوات إريترية في تيغراي · 2023'), credit(VOA)])
add(8.46, M + 'mapA_horn.mp4', 'map', 2.6, fixed=True)
add(15.5, G + 'ai6_storm.mp4', 'video', 0, [AI, cap('القرن الإفريقي على حافة حرب شاملة؟', 0.4)], fixed=True)
# ---- channel intro
add(20.54, C + 'intro.png', 'card')
# ---- news peg
add(27.74, C + 'reuters.png', 'card')
add(34.5, M + 'mapB_adigrat.mp4', 'map', 0, fixed=True)
add(46.24, ADI1, 'still', 0, [BADGE, ('loc', 'أديغرات · صورة أرشيفية', 0.3, None), credit(cr(ADI1))])
add(51.58, ADI2, 'still', 0, [BADGE, ('loc', 'أديغرات · صورة أرشيفية', 0.3, None), credit(cr(ADI2))], z0=1.08, z1=1.0)
add(57.74, ESC, 'still', 0, [BADGE, ('loc', 'إقليم تيغراي', 0.3, None), credit(cr(ESC))])
add(61.02, M + 'mapC_depth.mp4', 'map', 0, fixed=True)
add(69.86, G + 'ai1_drone.mp4', 'video', 0, [AI, cap('ضربات بمسيّرات نُسبت للجيش الإثيوبي', 0.5)], fixed=True)
add(74.0, TLAND, 'still', 0, [BADGE, ('loc', 'إقليم تيغراي', 0.3, None), credit(cr(TLAND))])
add(76.76, M + 'mapD_sequence.mp4', 'map', 0, fixed=True)
# ---- politics
add(85.2, UNSC1, 'still', 0, [('loc', 'مجلس الأمن الدولي · صورة أرشيفية', 0.3, None), credit(cr(UNSC1))])
add(89.58, UNSC2, 'still', 0, [cap('إثيوبيا تحذّر مجلس الأمن من التوغّل الإريتري', 0.3, 5.6), cap('«حق الدفاع عن النفس»', 5.9)], z0=1.0, z1=1.1, px=0.4)
add(98.92, ASSAB, 'still', 0, [BADGE, ('loc', 'عصب، إريتريا · صورة فضائية أرشيفية', 0.3, None), cap('إريتريا تنفي الاتهامات', 0.4), credit(cr(ASSAB))])
add(107.06, C + 'positions.png', 'card')
# ---- first section
add(116.3, C + 'sec1.png', 'card')
add(119.74, C + 'p1.png', 'card')
add(125.26, TROOPS, 'video', 52, [arch('مشاهد أرشيفية · تيغراي · 2023'), credit(VOA)])
add(131.36, C + 'p2.png', 'card')
add(136.0, G + 'ai1_drone.mp4', 'video', 0.2, [AI], fixed=True)
add(140.74, TLAND, 'still', 0, [BADGE, credit(cr(TLAND))], z0=1.12, z1=1.02, px=0.3)
add(144.34, C + 'p3.png', 'card')
add(149.0, G + 'ai2_convoy.mp4', 'video', 0, [AI], fixed=True)
add(154.04, BUS, 'still', 0, [BADGE, ('loc', 'الطريق إلى أديغرات · صورة أرشيفية', 0.3, None), credit(cr(BUS))])
add(157.44, C + 'p4.png', 'card')
add(162.5, G + 'ai4_ridge.mp4', 'video', 0, [AI], fixed=True)
add(167.5, FIGHT, 'video', 84, [arch('مشاهد أرشيفية · تيغراي · 2023'), credit(VOA)])
# ---- second section
add(171.64, C + 'sec2.png', 'card')
add(174.58, C + 'notborder.png', 'card')
add(183.4, M + 'mapE_redsea.mp4', 'map', 0, fixed=True)
add(197.0, BAB, 'still', 0, [('loc', 'مضيق باب المندب · البحر الأحمر', 0.3, None), credit(cr(BAB))])
add(203.5, G + 'ai3_ship.mp4', 'video', 0, [AI], fixed=True)
add(208.5, UNSC3, 'still', 0, [credit(cr(UNSC3))], z0=1.1, z1=1.0)
add(214.06, IDP, 'video', 282.5, fixed=True, ov= [arch('مشاهد أرشيفية · تيغراي · 2023'), credit(VOA)])
add(220.92, M + 'mapF_regions.mp4', 'map', 0, fixed=True)
add(235.92, AFAR, 'still', 0, [BADGE, ('loc', 'إقليم عفر · صورة أرشيفية', 0.3, None), credit(cr(AFAR))])
add(238.9, GOND, 'still', 0, [BADGE, ('loc', 'إقليم أمهرة · صورة أرشيفية', 0.3, None), credit(cr(GOND))])
# ---- scenarios
add(242.28, C + 'scen1.png', 'card')
add(253.4, C + 'scen2.png', 'card')
add(258.44, G + 'ai5_flashes.mp4', 'video', 0, [AI], fixed=True)
add(263.44, C + 'scen3.png', 'card')
add(269.84, M + 'mapG_scenario.mp4', 'map', 0, fixed=True)
# ---- conclusion
add(282.2, C + 'summary.png', 'card')
add(292.0, G + 'ai6_storm.mp4', 'video', 0, [AI], fixed=True)
add(297.0, G + 'ai3_ship.mp4', 'video', 0, [AI, cap('طموح البحر الأحمر', 1.6)], fixed=True)
add(302.0, REMEM, 'video', 66, [arch('مشاهد أرشيفية · تيغراي · 2023'), credit(VOA)])
add(308.64, C + 'end.png', 'card', z1=1.02)

for i, s in enumerate(S):
    s['i'] = i
    s['t1'] = S[i + 1]['t0'] if i + 1 < len(S) else AUDIO_LEN
    assert s['t1'] > s['t0'], s
json.dump(S, open('temp/edl.json', 'w'), ensure_ascii=False, indent=1)
for s in S:
    print(s['i'], s['t0'], round(s['t1'] - s['t0'], 2), s['kind'], os.path.basename(s['src']))
