"""Semantic scene plan -> temp/edl.json. Times = narration timestamps (whisper words)."""
import json, os, re

def cmn(t):
    return 'downloads/cm/cm_' + re.sub(r'[^A-Za-z0-9]+', '_', t[:55]).strip('_') + '.jpg'


AUD = 884.218776
TG = 'downloads/tg/'
CM = 'downloads/cm/'
MP = 'maps/'
CD = 'graphics/cards/'

S = {  # alias -> (path, kind, defaults)
    'm22': (TG + 'tg_almasdaronline_32922.mp4', 'video', {}),
    'm43': (TG + 'tg_almasirahnews_50943.mp4', 'video', {}),
    'm02': (TG + 'tg_almasdaronline_32902.mp4', 'video', {'mode': 'inset'}),
    'm86': (TG + 'tg_almasdaronline_32886.mp4', 'video', {'crop': [27, 0, 746, 420], 'mode': 'cover', 'fixed': True}),
    'm18': (TG + 'tg_almasdaronline_32918.mp4', 'video', {'mode': 'cover', 'fixed': True}),
    'm19': (TG + 'tg_almasdaronline_32919.mp4', 'video', {}),
    'm68': (TG + 'tg_almasdaronline_32868.mp4', 'video', {}),
    's03': (TG + 'tg_army21ye_3803.mp4', 'video', {}),
    's96': (TG + 'tg_army21ye_3796.mp4', 'video', {}),
    'a45': (TG + 'tg_AnsarAllahMC_333745.mp4', 'video', {}),
    'a25': (TG + 'tg_AnsarAllahMC_333725.mp4', 'video', {}),
    'a22': (TG + 'tg_AnsarAllahMC_333822.mp4', 'video', {}),
    'a05': (TG + 'tg_AnsarAllahMC_333905.mp4', 'video', {}),
    'a02': (TG + 'tg_AnsarAllahMC_333802.mp4', 'video', {}),
    'r48': (TG + 'tg_almasirahnews_50948.mp4', 'video', {}),
    'r05': (TG + 'tg_almasirahnews_50905.mp4', 'video', {}),
    'c_taiz': (cmn('City of Taiz, Yemen.jpg'), 'still', {}),
    'c_taiz2': (cmn('Taiz city from AlQahirah Castle.jpg'), 'still', {}),
    'c_castle': (cmn('The castle above Taiz (8683935588).jpg'), 'still', {}),
    'c_bab': (cmn('Bab al-Mandab Strait.jpg'), 'still', {}),
    'c_bab2': (cmn('Bab-el-Mandeb Seen From Midchannel (cropped).jpg'), 'still', {}),
    'c_uss': (cmn('Flickr - Official U.S. Navy Imagery - USS Enterprise and USS Vicksburg transit the Bab el-Mandeb Strait..jpg'), 'still', {}),
    'c_f15a': (cmn('641, 2024, F-15SA Eagle, Fairford, Saudi-Arabia - 9809 (53999077988).jpg'), 'still', {}),
    'c_f15b': (cmn('Boeing F-15SA Eagle Royal Saudi Air Force 5D4 2291 (53919688252).jpg'), 'still', {}),
    'c_manakha': (cmn('Manakha.jpg'), 'still', {}),
}
for m in ['mapA_mokha', 'mapB_westcoast', 'mapC_dhubab_mokha', 'mapD_taiz', 'mapE_taiz_aden', 'mapF_bab', 'mapG_regional',
          'mapH_sept', 'mapI_kahbub', 'mapJ_8km', 'mapK_dist', 'mapL_pocket', 'mapM_taiz_siege', 'mapN_axes', 'mapO_fronts',
          'mapP_sanaa_hodeidah', 'mapQ_tihama', 'mapR_taiz_sanaa', 'mapT_harad', 'mapU_habashi']:
    S[m] = (MP + m + '.mp4', 'map', {'fixed': True})
for c in ['H_sky_mokha', 'H_masirah_deny', 'P_sources', 'P_bukhaiti', 'T_narratives', 'T_dhubab', 'Q_episode', 'G_guest',
          'E_end', 'Q1_early', 'Q2_service', 'Q3_realistic', 'Q4_air', 'Q5_achieve', 'Q6_intl', 'Q7_command', 'Q8_shift']:
    S[c] = (CD + c + '.png', 'card', {})
for c in ['N_100', 'N_324', 'N_1122', 'N_100_324']:
    S[c] = (CD + c + '.mp4', 'map', {'fixed': True})

# overlay helpers
ALM = 'المصدر أونلاين (تلغرام) · 5 أكتوبر 2026'
ALM4 = 'المصدر أونلاين (تلغرام) · 4 أكتوبر 2026'
ALM3 = 'المصدر أونلاين (تلغرام) · 3 أكتوبر 2026'
MAS = 'قناة المسيرة (تلغرام) · 5 أكتوبر 2026'
AAM3 = 'أنصار الله (تلغرام) · 3 أكتوبر 2026'
AAM4 = 'أنصار الله (تلغرام) · 4 أكتوبر 2026'
CMS = 'Wikimedia Commons'
HOU = 'رواية إعلام الحوثيين'
GOVM = 'مشاهد بثّتها القوات الحكومية'


def cr(t): return ['credit', t, 0, None]
def lc(t, a=0.3, b=None): return ['loc', t, a, b]
def lb(t): return ['label', t, 0, None]
def ar(t): return ['archive', t, 0, None]
def sec(t): return ['section', t, 0.2, 4.2]


M43 = [cr(MAS), lb('لقطات جوية بثّتها قناة المسيرة')]
M02 = [cr(ALM), lb(GOVM), lc('ضمن عملية «فجر اليمن»')]

P = [
    # ---------------- PART 1: narration ----------------
    (0.00, 'm43', 40, M43 + [['hook', 'المخا|إعلان حكومي بالسيطرة.. ونفي حوثي', 0.0, None]], 'hook: aerial city footage + title'),
    (3.74, 'm22', 0, [cr(ALM + ' · تصوير عبدالناصر الصديق'), lc('المخا · بحسب الناشر')], 'Reuters/government: forces took Mokha'),
    (7.30, 'mapA_mokha', 3.0, [], 'Mokha located'),
    (10.48, 'H_sky_mokha', 0, [], 'could not verify independently (Reuters) - real headline'),
    (17.58, 'H_masirah_deny', 0, [], 'Ansar Allah rejected government account'),
    (22.20, 'mapB_westcoast', 0, [], 'welcome; west coast and around Taiz'),
    (29.64, 'c_taiz', 0, [cr(CMS), ar('صورة أرشيفية · تعز 2013')], 'military calculations of both sides'),
    (35.54, 'c_bab', 0, [cr(CMS), ar('صورة أرشيفية · باب المندب 2018')], 'battle and navigation security in Bab al-Mandab'),
    (42.06, 'c_f15a', 0, [cr(CMS), ar('صورة أرشيفية · مقاتلة F-15SA سعودية · 2024'), sec('أولاً: ماذا أُعلن؟')], 'coalition announced broad op with air cover'),
    (46.22, 'm02', 26, M02, 'intensive air cover'),
    (49.48, 'N_100', 0, [], '100 fighter jets'),
    (54.52, 'N_324', 0, [], '324 targets, high value'),
    (59.88, 'm02', 36, M02, 'high value targets (strike footage)'),
    (63.36, 'm02', 44, M02, 'government forces announced'),
    (66.12, 'N_1122', 0, [], '1122 targeting operations'),
    (70.86, 'm43', 33.9, [cr(MAS), lb('لقطات بثّتها قناة المسيرة'), lc('لافتة طريق ذوباب')], 'Giants & Homeland Shield in Dhubab'),
    (73.78, 'mapC_dhubab_mokha', 0, [], 'advance from Dhubab before Mokha announcement'),
    (79.80, 'P_sources', 0, [], 'numbers attributed to who announced them'),
    (84.72, 'P_bukhaiti', 0, [], 'Bukhaiti rejected news (no verbatim found)'),
    (92.02, 's03', 10, [cr('الإعلام الحربي الحوثي · بيان 4 أكتوبر 2026'), lb(HOU), lc('يحيى سريع · متحدث قوات الحوثيين')], 'deterrent capabilities'),
    (98.10, 'a45', 14, [cr(AAM3), lb(HOU), lc('دخان من منشأة لأرامكو في الرياض · بحسب الناشر')], 'strikes on vital facilities in Saudi'),
    (102.00, 'a25', 1, [cr(AAM3), lb('صور أقمار اصطناعية نشرها إعلام الحوثيين')], 'vital facilities (satellite)'),
    (105.86, 'm02', 0, M02 + [sec('ثانياً: الحسابات العسكرية')], 'militarily: dense air cover'),
    (110.76, 'm43', 24.2, [cr(MAS), lb('لقطات بثّتها قناة المسيرة'), lc('طريق ساحلي مفتوح')], 'open coastal areas'),
    (115.98, 'c_castle', 0, [cr(CMS), ar('صورة أرشيفية · مرتفعات تعز 2013')], 'mountain heights allow fortification'),
    (122.52, 'm19', 0, [cr(ALM), lb('رواية القوات الحكومية'), lc('ألغام تُركت في إحدى جبهات تعز · بحسب الناشر')], 'reports of Houthi withdrawals'),
    (130.52, 'mapD_taiz', 0, [], 'size and reasons need clearer info'),
    (136.16, 'mapD_taiz', 5.64, [], 'parallel: relative calm N/E of Taiz'),
    (145.34, 'c_taiz2', 0, [cr(CMS), ar('صورة أرشيفية · مدينة تعز 2014'), sec('ثالثاً: جبهات تعز')], 'fighting focused SW countryside'),
    (151.10, 'mapD_taiz', 8.0, [], 'retreat in parts of Jabal Habashi'),
    (158.04, 'm18', 8, [cr(ALM), lb('رواية القوات الحكومية'), lc('كمين في منطقة البيرين غرب تعز')], 'gov attack in al-Birin'),
    (163.06, 'T_narratives', 0, [], 'conflicting news, too early'),
    (170.06, 'mapE_taiz_aden', 0, [], 'open road Taiz-south, supply lines'),
    (182.76, 'a05', 74, [cr(AAM4), lb(HOU), lc('جنوب غرب تعز · بحسب الناشر')], 'Ansar Allah keep highland positions'),
    (188.70, 'a05', 89, [cr(AAM4), lb(HOU)], 'prevent breach of defensive lines'),
    (192.94, 'm02', 10, M02 + [sec('رابعاً: البعد الإقليمي والملاحة')], 'changing scene, land battles'),
    (198.66, 'c_uss', 0, [cr('البحرية الأمريكية · ' + CMS), ar('صورة أرشيفية · عبور باب المندب 2012')], 'regional calculations, sea lanes'),
    (203.40, 'mapF_bab', 0, [], 'gov & coalition: secure coast and strait'),
    (211.28, 'r48', 3, [cr(MAS), lb(HOU), lc('عبدالله صبري · وكيل خارجية سلطة صنعاء')], 'Ansar Allah keep field influence'),
    (216.96, 'r05', 5, [cr(MAS), lb(HOU), lc('محمود الجنيد · المكتب السياسي لأنصار الله')], 'ability to influence the confrontation'),
    (220.40, 'mapG_regional', 0, [], 'regional targets? missiles & drones'),
    (229.90, 'a22', 0, [cr(AAM3), lb('صور أقمار اصطناعية نشرها إعلام الحوثيين')], 'announced threats'),
    (236.04, 'a02', 22, [cr(AAM3), lb(HOU), lc('طريق في تعز · بحسب الناشر')], 'civilians and supplies'),
    (241.00, 'c_bab2', 0, [cr(CMS), ar('صورة أرشيفية · باب المندب 2023')], 'maritime navigation'),
    (247.64, 'm86', 0, [cr(ALM4), lc('رشاد العليمي · رئيس مجلس القيادة الرئاسي')], 'outcome cannot be decided by one statement'),
    (254.76, 'Q_episode', 0, [], 'share your reading'),
    (262.24, 'mapB_westcoast', 1.5, [], 'map of control on west coast'),
    # ---------------- PART 2: interview ----------------
    (272.82, 'G_guest', 0, [], 'guest joins'),
    (278.74, 'm43', 44, M43, 'welcome, rapid developments'),
    (283.26, 'm86', 8, [cr(ALM4), lc('رشاد العليمي')], 'Yemen Dawn, decisive? as Alimi announced'),
    (289.00, 'mapR_taiz_sanaa', 14, [], 'toward Sanaa'),
    (295.78, 'Q1_early', 0, [], 'too early; battles around Taiz'),
    (301.32, 'mapD_taiz', 1.0, [], 'around Taiz'),
    (305.38, 'm02', 20, M02, 'since dawn Yemen Dawn began'),
    (311.36, 'mapH_sept', 0, [], 'Houthi moved from south Hodeidah, Zabid to Bab al-Mandab, Kahbub'),
    (326.72, 'a05', 0, [cr(AAM4), lb(HOU)], 'yesterday Houthi upper hand'),
    (330.00, 'mapE_taiz_aden', 11.5, [], 'took Turbah, cut Taiz-Aden road'),
    (339.12, 'a05', 104, [cr(AAM4), lb(HOU)], 'upper hand yesterday'),
    (347.12, 'a02', 200, [cr(AAM3), lb(HOU)], 'turning point for Houthi'),
    (353.32, 'm22', 8, [cr(ALM), lc('المخا · 5 أكتوبر · بحسب الناشر')], 'today different'),
    (357.50, 'm02', 48, M02, 'volatile field'),
    (361.06, 'c_f15b', 0, [cr(CMS), ar('صورة أرشيفية · F-15SA سعودية · 2024')], 'air cover ~100 aircraft'),
    (367.72, 'mapI_kahbub', 0, [], 'attack from Kahbub mountains'),
    (388.22, 'mapI_kahbub', 20.5, [], 'took Mokha airport'),
    (396.04, 'm43', 33.9, [cr(MAS), lb('لقطات بثّتها قناة المسيرة'), lc('لافتة طريق ذوباب')], 'some call it Dhubab airport'),
    (399.80, 'mapI_kahbub', 32.2, [], 'simple primitive airport'),
    (403.56, 'mapI_kahbub', 36.0, [], 'took Dhubab, moved north'),
    (409.28, 'mapJ_8km', 0, [], '8 km from Mokha'),
    (421.66, 'mapK_dist', 0, [], 'distances 36/34/30 km'),
    (441.58, 'm43', 24.5, [cr(MAS), lb('لقطات بثّتها قناة المسيرة'), lc('أرض ساحلية مفتوحة')], 'open land'),
    (447.20, 'm22', 14, [cr(ALM), lc('الطريق في المخا · بحسب الناشر')], 'little vegetation'),
    (452.72, 'T_dhubab', 0, [], 'Yemeni side statements; Houthi denies'),
    (461.72, 'Q2_service', 0, [], 'strategic service to legitimate forces'),
    (468.04, 'mapL_pocket', 0, [], 'forces in Bab al-Mandab besieged'),
    (482.38, 'a05', 119, [cr(AAM4), lb(HOU)], 'Houthi did not fortify; pulled forces'),
    (491.00, 'mapM_taiz_siege', 0, [], 'reinforce around Taiz from south'),
    (503.14, 'mapN_axes', 5.0, [], 'path long: east to Mafraq, Khalid camp, north'),
    (524.28, 'mapO_fronts', 0, [], 'battles in Hajjah, Dhale, Marib, Jawf, Sanaa'),
    (537.60, 'Q3_realistic', 0, [], 'be realistic, too early'),
    (547.22, 'm86', 14, [cr(ALM4), lc('رشاد العليمي')], 'what does Alimi count on'),
    (555.90, 'm02', 30, M02, 'Sanaa next? air strikes'),
    (561.98, 'c_f15a', 0, [cr(CMS), ar('صورة أرشيفية · مقاتلة F-15SA سعودية · 2024')], 'coalition air strikes', {'z0': 1.12, 'z1': 1.0, 'px': 0.3}),
    (566.23, 'Q4_air', 0, [], 'air strikes will not decide'),
    (576.23, 'mapP_sanaa_hodeidah', 0, [], 'geography Sanaa-Hodeidah'),
    (588.11, 'c_manakha', 0, [cr(CMS), ar('صورة أرشيفية · مناخة على طريق صنعاء–الحديدة · 1986')], 'very difficult road'),
    (597.95, 'a02', 111, [cr(AAM3), lb(HOU), lc('طريق جبلي · بحسب الناشر')], 'hard to move forces'),
    (605.01, 'mapP_sanaa_hodeidah', 4.0, [], 'Houthi took Hodeidah via Tihama plain'),
    (616.23, 'Q5_achieve', 0, [], 'not diminishing achievement'),
    (622.95, 'm43', 46, M43, 'achievement credited'),
    (629.07, 'm86', 20, [cr(ALM4), lc('رشاد العليمي')], 'to Alimi, but early'),
    (633.75, 'mapQ_tihama', 0, [], 'control whole Tihama coast'),
    (641.75, 'mapR_taiz_sanaa', 0, [], 'from Taiz: Janad, Qaidah, Ibb, Samara, Yarim, Dhamar'),
    (659.95, 'm86', 4, [cr(ALM4), lc('رشاد العليمي')], 'political & military messages'),
    (667.47, 'm68', 2, [cr(ALM3), lc('مأرب · موظفو مقهى من أبناء تعز التحقوا بالجبهة · بحسب الناشر')], 'raise morale'),
    (672.13, 'Q6_intl', 0, [], 'requested international help'),
    (679.55, 'mapC_dhubab_mokha', 3.5, [], 'expected steps after Dhubab'),
    (686.03, 'mapH_sept', 11.0, [], 'restore map to before September'),
    (692.55, 'mapN_axes', 0, [], 'retake Mokha, Mafraq, Khalid camp'),
    (704.21, 'm02', 4, M02, 'node giving operational advantage'),
    (709.53, 'mapN_axes', 16.98, [], 'Khawkha districts north to old lines'),
    (720.17, 'mapM_taiz_siege', 4.0, [], 'break siege of Taiz first'),
    (730.39, 'a05', 14, [cr(AAM4), lb(HOU)], 'I mean the Houthis'),
    (737.00, 'mapL_pocket', 1.5, [], 'gov took Dhubab, can Houthi return'),
    (748.53, 'a05', 59, [cr(AAM4), lb(HOU)], 'reorganizing'),
    (756.23, 'mapT_harad', 0, [], 'withdrawing from Harad, Hajjah to Kahbub'),
    (767.73, 'mapU_habashi', 0, [], 'Kahbub under army; Habashi contested'),
    (785.97, 'm18', 15.5, [cr(ALM), lb('رواية القوات الحكومية'), lc('غرب تعز · 5 أكتوبر')], 'fighting'),
    (792.09, 'mapU_habashi', 24.36, [], 'secure Wazi\'iyah, Habashi'),
    (801.79, 'mapN_axes', 6.0, [], 'if Mokha lost, reorganize around Mafraq'),
    (815.95, 'm19', 22, [cr(ALM), lb('رواية القوات الحكومية')], 'may be forced'),
    (820.87, 'c_f15b', 0, [cr(CMS), ar('صورة أرشيفية · F-15SA سعودية · 2024')], 'if air support continues', {'z0': 1.15, 'z1': 1.0, 'px': 0.7}),
    (827.87, 'N_100_324', 0, [], '100 aircraft not sorties, 324 targets'),
    (838.05, 'm02', 6, M02, 'heavy Houthi losses'),
    (844.69, 'm18', 9, [cr(ALM), lb('رواية القوات الحكومية'), lc('البيرين · غرب تعز')], 'forced to reposition / withdraw'),
    (851.77, 's96', 40, [cr('الإعلام الحربي الحوثي · 3 أكتوبر 2026'), lb(HOU), lc('يحيى سريع · متحدث قوات الحوثيين')], 'command and control high'),
    (857.91, 'Q7_command', 0, [], 'determination high; field capabilities'),
    (865.91, 'a05', 4, [cr(AAM4), lb(HOU)], 'field capabilities impose themselves'),
    (869.37, 'Q8_shift', 0, [], 'if momentum continues, shift'),
    (876.27, 'm43', 50, M43, 'early stages'),
    (880.50, 'E_end', 0, [], 'restore map to before September / end card'),
]

GUEST_FROM = 278.74
edl = []
for k, row in enumerate(P):
    t0, key, tin, ov, note = row[:5]
    extra = row[5] if len(row) > 5 else {}
    t1 = P[k + 1][0] if k + 1 < len(P) else AUD
    path, kind, dflt = S[key]
    e = dict(i=k + 1, t0=t0, t1=t1, src=path, kind=kind, tin=tin, note=note, key=key)
    e.update(dflt); e.update(extra)
    ovs = []
    if kind in ('video', 'still'):
        ovs.append(['badge', '', 0, None])
    ovs += ov
    if t0 >= GUEST_FROM and kind in ('video', 'still', 'map') and key not in ('N_100_324',):
        ovs.append(['guest', '', 0.2, None])
    e['ov'] = ovs
    edl.append(e)
    assert t1 > t0, (k, t0, t1)
json.dump(edl, open('temp/edl.json', 'w'), ensure_ascii=False, indent=1)
tot = sum(int(round(e['t1'] * 25)) - int(round(e['t0'] * 25)) for e in edl)
print(len(edl), 'shots; frames', tot, 'want', round(AUD * 25))
long_ = [(e['i'], e['key'], round(e['t1'] - e['t0'], 1)) for e in edl if e['t1'] - e['t0'] > 10 and e['kind'] in ('card', 'still')]
print('long card/still holds:', long_)
missing = sorted({e['src'] for e in edl if not os.path.exists(e['src'])})
print('missing:', missing)
