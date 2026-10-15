"""Scene plan for audio_maroc.mp3 -> temp/edl.json (times = whisper segment timestamps)."""
import json, os, re

AUD = 642.664490
GUEST_FROM = 286.08   # expert starts speaking (name shown via graphics/project_cfg.py)


def cmn(t):
    return 'downloads/cm/cm_' + re.sub(r'[^A-Za-z0-9]+', '_', t[:55]).strip('_') + '.jpg'


DV = 'downloads/dvids/'
WB = 'downloads/web/'
HS = 'downloads/hes/'
CD = 'graphics/cards/'
S = {
    'reel': (DV + 'dvids_1025700_marrakech_air_show_2026.mp4', 'video', {'fixed': True}),
    'al26': (DV + 'dvids_1006101.mp4', 'video', {}),
    'f16to': (DV + 'dvids_1023753.mp4', 'video', {'fixed': True}),
    'f16rf': (DV + 'dvids_964659.mp4', 'video', {'fixed': True}),
    'star': (DV + 'dvids_img_10002858.jpg', 'still', {}),
    'aero1': (DV + 'dvids_img_10002861.jpg', 'still', {}),
    'aero4': (DV + 'dvids_img_10002865.jpg', 'still', {}),
    'lm': (WB + 'lm_f16_block72_first_flight.jpg', 'still', {}),
    'irifi_d': (WB + 'irifi_desert.webp', 'still', {}),
    'irifi_f': (WB + 'irifi_formation.webp', 'still', {}),
    'hai_team': (WB + 'harmattan_company.png', 'still', {}),
    'hai_strike': (WB + 'harmattan_precision_strike.png', 'still', {}),
    'hai_isr': (WB + 'harmattan_isr.png', 'still', {}),
    'booth': (WB + 'hespress_airshow.jpg', 'still', {}),
    'h_loud': (HS + 'hes_1819201.jpg', 'still', {}),
    'h_uae': (HS + 'hes_1819276.jpg', 'still', {}),
    'h_conf': (HS + 'hes_1819524.jpg', 'still', {}),
    'h_apache': (HS + 'hes_1819681.jpg', 'still', {}),
    'h_china': (HS + 'hes_1819722.jpg', 'still', {}),
    'c_f16c': (cmn('Moroccan F-16C.jpg'), 'still', {}),
    'c_f16al': (cmn('Moroccan air force F-16 flies above Morocco during Exercise African Lion.jpg'), 'still', {}),
    'c_f16pair': (cmn('F-16s Royal Moroccan Air Force 2024.jpg'), 'still', {}),
    'c_f16mas': (cmn('Royal Moroccan Air Force F-16 - 2016 Marrakech Airshow.jpg'), 'still', {}),
    'c_ef1': (cmn('Eurofighter Typhoon C.16-35 14-02 DACT 2017 (32064529133).jpg'), 'still', {}),
    'c_ef2': (cmn('Spanish Air Force - Eurofighter - Volkel - NL (51099700135).jpg'), 'still', {}),
    'c_ef3': (cmn('Eurofighter Typhoon Spanish Air Force.jpg'), 'still', {}),
    'c_frig': (cmn('Moroccan frigate Mohammed VI - 01.jpg'), 'still', {}),
    'c_strait': (cmn('The Strait of Gibraltar separates Europe from Africa (iss074e0425752).jpg'), 'still', {}),
    'c_whap': (cmn('Tata DRDO whap.jpg'), 'still', {}),
    'c_tb2': (cmn('Bayraktar TB2 Ground.jpg'), 'still', {}),
    'c_far': (cmn('US, Morocco celebrate Royal Moroccan Armed Forces 69th Anniversary (9043728).jpg'), 'still', {}),
}
for m in ['mA_hook', 'mB_marrakech', 'mC_industry', 'mD_ceuta', 'mE_westmed']:
    S[m] = ('maps/' + m + '.mp4', 'map', {'fixed': True})
for c in ['H_elespanol', 'H_libertad', 'H_lm', 'H_objective', 'H_infodefensa', 'H_elpais', 'P_irifi', 'P_edge', 'P_f16',
          'P_cards4', 'T_compare', 'T_rule', 'Q_episode', 'G_guest', 'E_end', 'L_ladder', 'Q1_balance', 'Q2_announce',
          'Q3_gap', 'Q4_airpower', 'Q5_noflip', 'Q6_ai', 'Q7_industry', 'Q8_ecosystem']:
    S[c] = (CD + c + '.png', 'card', {})
for c in ['N_show', 'N_25']:
    S[c] = (CD + c + '.mp4', 'map', {'fixed': True})


def cr(t): return ['credit', t, 0, None]
def lc(t, a=0.3, b=None): return ['loc', t, a, b]
def lb(t): return ['label', t, 0, None]
def ar(t): return ['archive', t, 0, None]
def sec(t): return ['section', t, 0.2, 4.2]


DVC = 'DVIDS · وزارة الدفاع الأمريكية (ملكية عامة)'
CMS = 'Wikimedia Commons'
HES = 'هسبريس'
HAI = 'Harmattan AI'
REEL = [cr(DVC), lc('معرض مراكش للطيران · 7 أكتوبر 2026')]
STAR = [cr(DVC), lc('عرض جوي في معرض مراكش 2026')]
REND = ar('تصوّر من الشركة المصنّعة')
ILLF16 = ar('مشاهد توضيحية · مقاتلات F-16 أمريكية')

P = [
    # ---------- PART 1 ----------
    (0.00, 'star', 0, STAR + [['hook', 'المغرب يقلق مدريد|مسيّرة بمدى 2000 كم ومقاتلات F-16 جديدة', 0.0, None]], 'hook: Moroccan star drawn over Marrakech', {'z0': 1.0, 'z1': 1.12}),
    (3.58, 'mA_hook', 0.5, [], '764 km Rabat-Madrid; 2000 km red circle'),
    (15.80, 'irifi_f', 0, [cr(HAI), REND], 'range 2000 km'),
    (19.74, 'reel', 0, REEL, 'not ordinary aircraft'),
    (23.14, 'mA_hook', 19.0, [], 'message reshuffled W-Med calculations'),
    (30.00, 'H_elespanol', 0, [], 'Madrid papers headlines'),
    (33.66, 'H_libertad', 0, [], 'Morocco flexes military muscle'),
    (38.50, 'h_china', 0, [cr(HES), lc('أجنحة معرض مراكش 2026')], 'what did Spaniards see at Marrakech'),
    (41.84, 'h_loud', 0, [cr(HES), lc('عبد اللطيف لوديي · افتتاح المعرض')], 'from buyer to maker'),
    (45.08, 'mC_industry', 2.0, [], 'game-changing maker'),
    (50.02, 'mB_marrakech', 0, [], '10 October curtain fell on Marrakech show'),
    (55.34, 'N_show', 0, [], '200 exhibitors, 27 countries'),
    (59.64, 'h_conf', 0, [cr(HES), lc('معرض مراكش للطيران 2026')], 'echo in Spanish newsrooms'),
    (64.12, 'booth', 0, [cr('Hespress English'), lc('جناح Harmattan AI في معرض مراكش')], 'the surprise was not a traditional deal'),
    (69.18, 'irifi_d', 0, [cr(HAI), REND, lc('IRIFI')], 'IRIFI attack drone developed by Morocco'),
    (75.20, 'hai_team', 0, [cr(HAI), lc('Harmattan AI · شركة فرنسية')], 'with French Harmattan AI'),
    (79.02, 'mC_industry', 4.5, [], 'plans to manufacture locally'),
    (82.00, 'irifi_f', 0, [cr(HAI), REND], 'why the media alarm', {'z0': 1.12, 'z1': 1.0, 'px': 0.7}),
    (84.86, 'mA_hook', 12.0, [], '2000 km puts whole Iberia under the microscope'),
    (92.12, 'P_irifi', 0, [], 'its brain: deep strikes, AI, optical guidance'),
    (98.14, 'hai_strike', 0, [cr(HAI), ar('صورة توضيحية من Harmattan AI · ليست IRIFI')], 'AI + precise optical guidance'),
    (102.52, 'irifi_d', 0, [cr(HAI), REND], 'flies & strikes independently of satellites', {'z0': 1.15, 'z1': 1.0, 'px': 0.3}),
    (109.86, 'al26', 20, [cr(DVC), ar('مشاهد توضيحية · African Lion 26 · 2026')], 'jamming & EW systems'),
    (114.84, 'hai_isr', 0, [cr(HAI), ar('صورة توضيحية من Harmattan AI')], 'ghost that knows its way'),
    (120.44, 'f16to', 35.4, [cr(DVC), ILLF16], 'control is completed in the heights'),
    (124.04, 'c_f16al', 0, [cr(CMS), ar('صورة أرشيفية · F-16 مغربية · 2018')], 'parallel development from the US'),
    (127.22, 'H_lm', 0, [], 'Lockheed Martin announces first flight'),
    (131.66, 'lm', 0, [cr('لوكهيد مارتن'), lc('أول F-16 Block 72 للمغرب · رحلة تجريبية · أكتوبر 2026')], 'F-16 Block 72 for Morocco'),
    (137.00, 'N_25', 0, [], 'fleet of 25'),
    (142.24, 'H_objective', 0, [], 'Spanish paper: narrowing the gap'),
    (149.06, 'c_ef1', 0, [cr(CMS), ar('صورة أرشيفية · يوروفايتر إسبانية · 2017')], 'gap with Spain\'s crown jewel'),
    (154.00, 'c_ef3', 0, [cr(CMS), ar('صورة أرشيفية · يوروفايتر تايفون · 2025')], 'Eurofighter'),
    (158.00, 'reel', 8, REEL, 'story did not end here'),
    (162.42, 'h_uae', 0, [cr(HES), lc('فريق «فرسان الإمارات» في سماء مراكش')], 'agreement with UAE EDGE'),
    (166.98, 'c_tb2', 0, [cr(CMS), ar('صورة أرشيفية توضيحية · Bayraktar TB2 (من طرازات الأسطول المغربي)')], 'arming Moroccan drones'),
    (171.40, 'P_edge', 0, [], 'Desert Sting 16 & Thunder P-31'),
    (180.24, 'c_tb2', 0, [cr(CMS), ar('صورة أرشيفية توضيحية · Bayraktar TB2')], 'surgical, low cost', {'z0': 1.18, 'z1': 1.05, 'px': 0.8}),
    (186.04, 'mC_industry', 8.0, [], 'weapon you make yourself'),
    (190.64, 'H_infodefensa', 0, [], 'Infodefensa follows MMI plans'),
    (198.40, 'c_whap', 0, [cr(CMS), ar('صورة أرشيفية · مدرعة WhAP 8x8 · الهند 2023')], 'turrets for 8x8 by March 2027'),
    (204.40, 'c_far', 0, [cr(DVC), ar('صورة أرشيفية · القوات المسلحة الملكية · 2025')], 'land & air rise'),
    (208.66, 'c_frig', 0, [cr(CMS), ar('صورة أرشيفية · الفرقاطة المغربية «محمد السادس» · يوليو 2026')], 'echo reached hot waters'),
    (213.12, 'H_elpais', 0, [], 'El País: silent dangerous frictions near Ceuta'),
    (220.74, 'mD_ceuta', 2.0, [], 'near Ceuta last summer; each side tests the other'),
    (231.58, 'c_f16pair', 0, [cr(CMS), ar('صورة أرشيفية · F-16 مغربية · 2024')], 'F-16s in the sky'),
    (234.24, 'irifi_f', 0, [cr(HAI), REND], 'smart cross-border drones', {'z0': 1.0, 'z1': 1.1, 'px': 0.2}),
    (237.28, 'P_cards4', 0, [], 'Emirati munitions, factories'),
    (242.60, 'mE_westmed', 3.0, [], 'Spain naval superiority + NATO'),
    (251.30, 'T_rule', 0, [], 'armies plan on capabilities'),
    (255.86, 'c_f16pair', 0, [cr(CMS), ar('صورة أرشيفية · F-16 مغربية · 2024')], 'symmetric deterrence', {'z0': 1.15, 'z1': 1.02, 'px': 0.2}),
    (260.50, 'c_strait', 0, [cr('NASA · ' + CMS), ar('مضيق جبل طارق من محطة الفضاء الدولية · مارس 2026')], 'end of absolute superiority in Gibraltar'),
    (266.88, 'aero4', 0, STAR, 'Rabat options widen'),
    (271.04, 'Q_episode', 0, [], 'arms race or pressure cards'),
    (278.00, 'reel', 2, REEL, 'unresolved sovereign files'),
    # ---------- PART 2: expert (name only, no channel, no interview footage) ----------
    (283.46, 'G_guest', 0, [], 'expert card'),
    (291.36, 'H_libertad', 0, [], 'Spanish media question deserves sober reading', {'z0': 1.06, 'z1': 1.0}),
    (296.20, 'Q1_balance', 0, [], 'balance not measured by aircraft count'),
    (304.78, 'f16rf', 3, [cr(DVC), ar('مشاهد توضيحية · تزوّد بالوقود جواً')], 'intel & logistics capabilities'),
    (311.42, 'T_compare', 0, [], 'Spain: capabilities, NATO'),
    (318.00, 'c_ef2', 0, [cr(CMS), ar('صورة أرشيفية · يوروفايتر إسبانية في تمرين للناتو · 2019')], 'institutional NATO dimension'),
    (322.32, 'lm', 0, [cr('لوكهيد مارتن'), lc('F-16 Block 72 للمغرب')], 'Morocco modernising', {'z0': 1.15, 'z1': 1.0, 'px': 0.3}),
    (328.32, 'booth', 0, [cr('Hespress English'), lc('معرض مراكش 2026')], 'expanding partnerships', {'z0': 1.12, 'z1': 1.0}),
    (331.34, 'mC_industry', 9.0, [], 'developing industrial base'),
    (336.90, 'H_objective', 0, [], 'Spanish press questions', {'z0': 1.06, 'z1': 1.0}),
    (342.50, 'mA_hook', 1.0, [], 'gap between Rabat and Madrid'),
    (349.54, 'Q2_announce', 0, [], 'announcement vs real capability'),
    (356.48, 'al26', 0, [cr(DVC), ar('مشاهد توضيحية · تدريب مغربي-أمريكي · African Lion 26')], 'years of training & integration'),
    (363.82, 'Q3_gap', 0, [], 'no need to outdo Spain everywhere'),
    (372.82, 'mE_westmed', 10.0, [], 'deterrence calculations'),
    (380.40, 'c_ef3', 0, [cr(CMS), ar('صورة أرشيفية · يوروفايتر إسبانية · 2025')], 'Q: closing gap with Eurofighter', {'z0': 1.0, 'z1': 1.12, 'px': 0.7}),
    (386.00, 'c_f16c', 0, [cr(CMS), ar('صورة أرشيفية · F-16 مغربية · 2022')], 'what does it mean'),
    (392.04, 'c_ef1', 0, [cr(CMS), ar('صورة أرشيفية · يوروفايتر إسبانية · 2017')], 'Eurofighter vs RMAF modernisation', {'z0': 1.12, 'z1': 1.0, 'px': 0.3}),
    (399.54, 'c_f16pair', 0, [cr(CMS), ar('صورة أرشيفية · F-16 مغربية · 2024')], 'RMAF modernisation', {'z0': 1.0, 'z1': 1.12, 'px': 0.8}),
    (404.08, 'c_f16mas', 0, [cr(CMS), ar('صورة أرشيفية · F-16 مغربية في معرض مراكش 2016')], 'worries Spanish press'),
    (411.74, 'lm', 0, [cr('لوكهيد مارتن'), lc('أول رحلة تجريبية · F-16 Block 72')], 'first test flight', {'z0': 1.0, 'z1': 1.15, 'px': 0.2}),
    (417.32, 'P_f16', 0, [], 'radar, avionics, integrated systems'),
    (426.08, 'f16to', 36, [cr(DVC), ILLF16], 'bothers Spanish military thinking'),
    (431.74, 'c_ef2', 0, [cr(CMS), ar('صورة أرشيفية · يوروفايتر إسبانية · 2019')], 'Spanish air & land ops', {'z0': 1.15, 'z1': 1.0, 'px': 0.7}),
    (436.16, 'Q4_airpower', 0, [], 'air power = training, logistics'),
    (445.12, 'f16rf', 26, [cr(DVC), ar('مشاهد توضيحية · دعم لوجستي جوي')], 'logistic support'),
    (451.64, 'c_far', 0, [cr(DVC), ar('صورة أرشيفية · القوات المسلحة الملكية · 2025')], 'Royal Armed Forces', {'z0': 1.12, 'z1': 1.0}),
    (455.74, 'Q5_noflip', 0, [], 'no total overturn'),
    (464.88, 'c_whap', 0, [cr(CMS), ar('صورة أرشيفية · مدرعة WhAP 8x8 · 2023')], 'land', {'z0': 1.15, 'z1': 1.0, 'px': 0.6}),
    (468.50, 'c_frig', 0, [cr(CMS), ar('صورة أرشيفية · الفرقاطة «محمد السادس» · 2026')], 'naval', {'z0': 1.0, 'z1': 1.12, 'px': 0.3}),
    (471.28, 'irifi_d', 0, [cr(HAI), REND], 'technology', {'z0': 1.0, 'z1': 1.1, 'px': 0.7}),
    (475.20, 'al26', 24, [cr(DVC), ar('مشاهد توضيحية · African Lion 26')], 'Q: EW readiness & AI'),
    (483.36, 'hai_strike', 0, [cr(HAI), ar('صورة توضيحية من Harmattan AI')], 'AI systems', {'z0': 1.15, 'z1': 1.0, 'px': 0.3}),
    (487.26, 'Q6_ai', 0, [], 'technical integration taken seriously'),
    (495.52, 'al26', 36, [cr(DVC), ar('مشاهد توضيحية · African Lion 26')], 'armies in Africa, Europe, America, Asia'),
    (503.60, 'irifi_f', 0, [cr(HAI), REND], 'can make the difference quickly', {'z0': 1.12, 'z1': 1.0, 'px': 0.5}),
    (511.20, 'H_elespanol', 0, [], 'Spanish press fears', {'z0': 1.06, 'z1': 1.0}),
    (517.78, 'booth', 0, [cr('Hespress English'), lc('جناح Harmattan AI')], 'big space in industrial strategy', {'z0': 1.0, 'z1': 1.15, 'px': 0.6}),
    (526.02, 'mC_industry', 12.0, [], 'industrial strategy'),
    (534.78, 'h_conf', 0, [cr(HES), lc('معرض مراكش للطيران 2026')], 'regional & continental level', {'z0': 1.12, 'z1': 1.0}),
    (541.76, 'h_china', 0, [cr(HES), lc('أجنحة معرض مراكش 2026')], 'integrating technologies', {'z0': 1.0, 'z1': 1.12, 'px': 0.3}),
    (547.50, 'hai_team', 0, [cr(HAI)], 'into military industry', {'z0': 1.12, 'z1': 1.0, 'px': 0.6}),
    (553.34, 'h_loud', 0, [cr(HES), lc('عبد اللطيف لوديي')], 'Q: manufacturing', {'z0': 1.1, 'z1': 1.0}),
    (559.16, 'mC_industry', 16.0, [], 'Moroccan manufacturing direction'),
    (566.92, 'c_ef3', 0, [cr(CMS), ar('صورة أرشيفية · يوروفايتر · 2025')], 'Spanish direction at same level?', {'z0': 1.12, 'z1': 1.0, 'px': 0.4}),
    (572.92, 'Q7_industry', 0, [], 'from import to production'),
    (581.40, 'reel', 6.8, REEL, 'long-term decision independence'),
    (587.22, 'P_cards4', 0, [], 'drones, munitions, components', {'z0': 1.05, 'z1': 1.0}),
    (592.18, 'H_infodefensa', 0, [], 'localising production stages', {'z0': 1.06, 'z1': 1.0}),
    (598.50, 'mC_industry', 9.0, [], 'real military industry'),
    (607.60, 'L_ladder', 0, [], 'assembly vs licence vs transfer vs independent'),
    (616.00, 'c_frig', 0, [cr(CMS), ar('صورة أرشيفية · الفرقاطة «محمد السادس» · 2026')], 'navy', {'z0': 1.12, 'z1': 1.0, 'px': 0.6}),
    (620.68, 'c_f16c', 0, [cr(CMS), ar('صورة أرشيفية · F-16 مغربية · 2022')], 'air force', {'z0': 1.0, 'z1': 1.12}),
    (626.38, 'aero1', 0, STAR, 'strategic autonomy'),
    (631.10, 'Q8_ecosystem', 0, [], 'engineers, R&D'),
    (637.95, 'E_end', 0, [], 'end card'),
]

edl = []
for k, row in enumerate(P):
    t0, key, tin, ov, note = row[:5]
    extra = row[5] if len(row) > 5 else {}
    t1 = P[k + 1][0] if k + 1 < len(P) else AUD
    path, kind, dflt = S[key]
    e = dict(i=k + 1, t0=t0, t1=t1, src=path, kind=kind, tin=tin, note=note, key=key)
    e.update(dflt); e.update(extra)
    ovs = [['badge', '', 0, None]] if kind in ('video', 'still') else []
    ovs += ov
    if t0 >= GUEST_FROM - 3 and key != 'G_guest' and kind in ('video', 'still', 'map'):
        ovs.append(['guest', '', 0.2, None])
    e['ov'] = ovs
    edl.append(e)
    assert t1 > t0, (k, t0, t1)
json.dump(edl, open('temp/edl.json', 'w'), ensure_ascii=False, indent=1)
tot = sum(int(round(e['t1'] * 25)) - int(round(e['t0'] * 25)) for e in edl)
print(len(edl), 'shots; frames', tot, 'want', round(AUD * 25))
print('long holds:', [(e['i'], e['key'], round(e['t1'] - e['t0'], 1)) for e in edl if e['t1'] - e['t0'] > 10])
print('missing:', sorted({e['src'] for e in edl if not os.path.exists(e['src'])}))
