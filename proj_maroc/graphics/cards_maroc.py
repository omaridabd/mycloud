"""Cards for the Morocco / Spain video. Reuses the card primitives in cards.py."""
import os, sys
from PIL import ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import cards as C
import project_cfg as CFG


def headline_es(name, outlet, date, headline_ar, original, quotes_ar, chip_txt=None, label='خبر'):
    """Press headline card: Arabic translation + original Spanish/English headline (LTR) + Arabic quote lines."""
    im = navy_bg()
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 180, 130, W - 180, H - 130
    d.rounded_rectangle([x0 + 10, y0 + 14, x1 + 10, y1 + 14], 18, fill=(0, 0, 0, 120))
    d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(250, 250, 252))
    d.rectangle([x0, y0, x1, y0 + 92], fill=(236, 238, 242))
    text_rtl(d, (x1 - 50, y0 + 46), outlet, font(40, '800ExtraBold'), fill=(20, 24, 34), anchor='rm')
    d.text((x0 + 50, y0 + 46), date, font=font(30, '500Medium'), fill=(90, 96, 110), anchor='lm', direction='rtl', language='ar')
    lf = font(28, '700Bold')
    lw = tsize(d, label, lf)[0]
    d.rounded_rectangle([x1 - 50 - lw - 36, y0 + 118, x1 - 50, y0 + 170], 8, fill=RED)
    text_c(d, (x1 - 50 - (lw + 36) / 2, y0 + 145), label, lf)
    # original headline, LTR, italic-ish grey
    of = font(30, '500Medium', 'plex')
    y = y0 + 200
    words, line, lines = original.split(), '', []
    for w_ in words:
        t = (line + ' ' + w_).strip()
        if d.textlength(t, font=of) > x1 - x0 - 120 and line:
            lines.append(line); line = w_
        else:
            line = t
    lines.append(line)
    for ln in lines:
        d.text((x0 + 60, y), ln, font=of, fill=(110, 116, 130), anchor='la')
        y += 46
    y += 18
    hf = font(52, '800ExtraBold')
    for ln in wrap(d, headline_ar, hf, x1 - x0 - 120):
        text_rtl(d, (x1 - 60, y), ln, hf, fill=(16, 20, 30), anchor='ra')
        y += 84
    y += 16
    qf = font(34, '500Medium', 'plex')
    for q in quotes_ar:
        ys = y
        for ln in wrap(d, q, qf, x1 - x0 - 170):
            text_rtl(d, (x1 - 90, y), ln, qf, fill=(50, 56, 70), anchor='ra')
            y += 54
        d.rectangle([x1 - 66, ys + 6, x1 - 58, y - 8], fill=RED)
        y += 16
    if chip_txt:
        cf = font(28, '700Bold')
        cw = tsize(d, chip_txt, cf)[0]
        d.rounded_rectangle([x0 + 50, y1 - 92, x0 + 50 + cw + 44, y1 - 38], 10, fill=(20, 24, 34))
        text_c(d, (x0 + 50 + (cw + 44) / 2, y1 - 65), chip_txt, cf, fill=GOLD)
    return C.save(im, name)


def guest_card(name):
    import math
    im = navy_bg()
    d = ImageDraw.Draw(im)
    C.kicker(d, 'قراءة عسكرية', y=200)
    text_rtl(d, (W - 160, 360), CFG.EXPERT_NAME, font(96, '900Black'), anchor='ra')
    d.rectangle([W - 170, 520, W - 160, 600], fill=RED)
    text_rtl(d, (W - 200, 560), CFG.EXPERT_ROLE, font(52, '600SemiBold'), fill=(205, 212, 226), anchor='rm')
    text_rtl(d, (W - 160, 700), 'مداخلة صوتية', font(38, '500Medium'), fill=(160, 170, 188), anchor='ra')
    for i in range(60):
        h = 30 + 90 * abs(math.sin(i * 0.55) * math.cos(i * 0.17))
        x = 200 + i * 16
        d.rounded_rectangle([x, 760 - h / 2, x + 8, 760 + h / 2], 4, fill=(200, 22, 38, 200))
    return C.save(im, name)


def ladder_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    C.kicker(d, CFG.EXPERT_NAME, y=110)
    text_rtl(d, (W - 160, 230), 'من التجميع إلى الاستقلال الصناعي', font(62, '800ExtraBold'), anchor='ra')
    steps = ['تجميع المعدات محلياً', 'التصنيع بترخيص', 'نقل التكنولوجيا', 'تطوير وطني مستقل']
    for i, s in enumerate(steps):
        x1 = W - 160 - i * 380
        x0 = x1 - 340
        yb = 940 - i * 110
        a = 120 + i * 45
        d.rounded_rectangle([x0, yb - 220, x1, yb], 14, fill=(min(255, 120 + i * 30), 22, 38, 255) if i == 3 else (30, 60 + i * 20, 110 + i * 25, 255))
        text_c(d, ((x0 + x1) / 2, yb - 170), str(i + 1), font(54, '900Black'))
        for k, ln in enumerate(wrap(d, s, font(34, '700Bold'), 300)):
            text_c(d, ((x0 + x1) / 2, yb - 100 + k * 46), ln, font(34, '700Bold'))
    text_rtl(d, (W - 160, 330), '«هناك فرق أساسي بين هذه المراحل»', font(36, '500Medium'), fill=(190, 198, 212), anchor='ra')
    return C.save(im, name)


def end_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    text_c(d, (W / 2, 230), 'سباق تسلح.. أم أوراق ضغط؟', font(86, '900Black'))
    d.rectangle([W / 2 - 100, 305, W / 2 + 100, 315], fill=RED)
    pf = font(38, '600SemiBold')
    rows = ['IRIFI: خطاب نوايا بمدى معلن 2000 كم · لم يدخل الخدمة بعد',
            'أول F-16 Block 72 للمغرب حلّق في 6 أكتوبر · التسليم لم يُحدَّد',
            'ذخائر EDGE: عقد شراء · أبراج MMI: تسليم مرتقب في 2027',
            'إسبانيا: تفوق بحري ومظلة الناتو']
    y = 410
    for r in rows:
        text_c(d, (W / 2, y), r, pf)
        y += 80
    sf = font(25, '500Medium')
    text_c(d, (W / 2, 800), 'المصادر: لوكهيد مارتن · Harmattan AI · El Español · Libertad Digital · The Objective · Infodefensa · El País (عبر AFP) · Hespress · DVIDS', sf, fill=(170, 180, 198))
    text_c(d, (W / 2, 870), 'شاركونا قراءتكم في التعليقات', font(40, '700Bold'), fill=GOLD)
    return C.save(im, name)


def question_card(name):
    im = navy_bg()
    d = ImageDraw.Draw(im)
    C.kicker(d, 'سؤال الحلقة', y=180)
    qf = font(70, '800ExtraBold')
    text_rtl(d, (W - 160, 330), 'سباق تسلح يعيد رسم خارطة القوى', qf, anchor='ra')
    text_rtl(d, (W - 160, 440), 'في غرب المتوسط؟', qf, anchor='ra')
    text_rtl(d, (W - 160, 600), 'أم مجرد أوراق ضغط لحسم ملفات سيادية عالقة؟', font(54, '600SemiBold'), fill=(205, 212, 226), anchor='ra')
    cf = font(38, '700Bold')
    t = 'شاركونا قراءتكم في التعليقات'
    cw = tsize(d, t, cf)[0]
    d.rounded_rectangle([W - 160 - cw - 60, 780, W - 160, 856], 12, fill=RED)
    text_c(d, (W - 160 - (cw + 60) / 2, 818), t, cf)
    return C.save(im, name)


def build():
    headline_es('H_elespanol', 'El Español · إل إسبانيول', '8 أكتوبر 2026',
                'المغرب يرفع رهانه العسكري بـ IRIFI.. مسيّرة ذاتية قادرة على بلوغ أهداف على بعد 2000 كم',
                'Marruecos eleva su apuesta militar con IRIFI, un dron autónomo capaz de alcanzar objetivos a 2.000 km',
                ['«من الرباط إلى مدريد 764 كم في خط مستقيم»'], chip_txt='ترجمة عربية للعنوان')
    headline_es('H_libertad', 'Libertad Digital', '9 أكتوبر 2026',
                'المغرب يخطو أولى خطواته لتصنيع مسيّرات انتحارية بمدى 2000 كم داخل البلاد',
                'Marruecos da el primer paso para fabricar en el país drones kamikaze con 2.000 km de alcance',
                [], chip_txt='ترجمة عربية للعنوان')
    headline_es('H_lm', 'Lockheed Martin · لوكهيد مارتن', '6 أكتوبر 2026',
                'لوكهيد مارتن تعلن نجاح أول رحلة لأول مقاتلة F-16 Block 72 مخصّصة للمغرب',
                "Lockheed Martin Announces First Flight of Morocco's First F-16 Block 72",
                ['النسخة ذات المقعدين F-16D · غرينفيل، كارولاينا الجنوبية', 'تواصل الطائرة اختبارات الطيران قبل التسليم'],
                label='بيان رسمي')
    headline_es('H_objective', 'The Objective', '7 أكتوبر 2026',
                'المغرب يختبر مقاتلته الجديدة F-16 التي تقلّص الفجوة مع يوروفايتر الإسبانية',
                'Marruecos prueba su nuevo caza F-16 que reduce la brecha con los Eurofighter españoles',
                ['«تقلّص الفجوة التكنولوجية مقارنة بيوروفايتر سلاح الجو الإسباني»'], chip_txt='ترجمة عربية للعنوان')
    headline_es('H_infodefensa', 'Infodefensa', '12 أكتوبر 2026',
                'شركة MMI المغربية ستبدأ تسليم أبراج لمدرعات 8x8 إلى الجيش المغربي في 2027',
                'MMI, empresa marroquí de capital israelí, comenzará a entregar torretas para blindados 8x8 al Ejército de Marruecos en 2027',
                ['«تعتزم البدء في مارس 2027 بتسليم الأبراج» · تصريحات نقلتها رويترز خلال معرض مراكش'], chip_txt='ترجمة عربية للعنوان')
    headline_es('H_elpais', 'El País · عبر وكالة AFP', '12 أكتوبر 2026',
                'سفن حربية مغربية دخلت مياه سبتة الإسبانية في يوليو بحسب «إل باييس»',
                'Buques de guerra de Marruecos entraron en aguas españolas de Ceuta en julio, según El País',
                ['«فرقاطة مغربية واحدة على الأقل وعدة زوارق دورية دخلت المياه الإسبانية دون إذن مسبق»',
                 '«كادت تتسبب في تصادم بين سفن عسكرية للبلدين»'],
                chip_txt='لم نطّلع على النص الأصلي · لا رد مغربي رسمي متاح')
    C.points_card('P_irifi', 'IRIFI · بحسب Harmattan AI', 'مواصفات معلنة',
                  ['مدى معلن يصل إلى 2000 كم',
                   'ملاحة ذاتية لا تعتمد على أنظمة الأقمار الصناعية (GNSS)',
                   'توجيه بصري في المرحلة النهائية',
                   'خطاب نوايا وُقّع في 7 أكتوبر · لا سعر ولا كميات ولا موعد تسليم'],
                  'El Español · Zona Militar · Silicon Valley Maroc', note='مواصفات من الشركة · غير متحقق منها بشكل مستقل')
    C.points_card('P_edge', 'EDGE الإماراتية · عقد 9 أكتوبر 2026', 'ذخائر دقيقة للمسيرات المغربية',
                  ['DESERT STING 16 · سلاح انزلاقي موجّه 23 كغ · مدى حتى 15 كم',
                   'THUNDER P-31 · عُدّة تحوّل قنبلة MK 81 إلى ذخيرة موجّهة · 10–20 كم',
                   'لم تُكشف الكميات ولا قيمة العقد'],
                  'Quwa · Hespress English · Morocco World News')
    C.points_card('P_f16', 'F-16 Block 72', 'ما الذي يضيفه الطراز الجديد؟',
                  ['رادار AESA من طراز APG-83', 'إلكترونيات طيران وإدارة معلومات حديثة',
                   'العمل ضمن منظومات قتالية متكاملة'],
                  'لوكهيد مارتن · وقراءة الضيف')
    C.points_card('P_cards4', 'خلاصة', 'أوراق الرباط الجديدة',
                  ['مقاتلات F-16 Block 72 (25 طائرة مطلوبة)', 'مسيّرات بعيدة المدى (IRIFI قيد التطوير)',
                   'ذخائر إماراتية دقيقة للمسيرات', 'مصانع وخطوط تجميع محلية'],
                  'إعلانات رسمية وتقارير صحفية · أكتوبر 2026')
    C.two_col('T_compare', 'ميزان غير متماثل',
              ('إسبانيا', (30, 80, 160), ['عضو في حلف الناتو', 'تفوق بحري', 'مقاتلات يوروفايتر تايفون'], 'معطيات عامة'),
              ('المغرب', RED, ['25 مقاتلة F-16 Block 72 (طلبية)', 'مسيّرات TB2 وأكنجي ووينغ لونغ 2', 'IRIFI قيد التطوير'],
               'لوكهيد مارتن · Quwa · Harmattan AI'),
              foot='مقارنة نوعية · ليست جرداً كاملاً للقدرات')
    C.quote_card('T_rule', 'قاعدة عسكرية', 'الجيوش لا تبني خططها على النوايا.. بل على القدرات', '')
    question_card('Q_episode')
    guest_card('G_guest')
    end_card('E_end')
    ladder_card('L_ladder')
    QK = CFG.EXPERT_NAME + ' · ' + CFG.EXPERT_ROLE if CFG.EXPERT_NAME != 'خبير عسكري' else CFG.EXPERT_ROLE
    A = CFG.EXPERT_NAME
    qs = {
        'Q1_balance': 'ميزان القوى بين دولتين لا يقاس بعدد الطائرات أو المسيّرات وحدها.. بل بمجموع القدرات الجوية والبحرية والبرية والصناعية والاستخباراتية',
        'Q2_announce': 'لا ينبغي الخلط بين الإعلان عن مشروعات تسلّح وبين تحوّلها إلى قدرات عملية مكتسبة.. فذلك يتطلب سنوات من التدريب والدمج والصيانة',
        'Q3_gap': 'المغرب ليس بحاجة إلى التفوق على إسبانيا في كل المجالات.. قد يكفي تقليص بعض الفوارق لتغيير حسابات الردع',
        'Q4_airpower': 'المقارنة لا يجب أن تُختزل في الخصائص التقنية للطائرة.. فالقوة الجوية تعتمد على التدريب والتسليح والجاهزية والدعم اللوجستي',
        'Q5_noflip': 'تحديث المقاتلات المغربية قد يقلّص بعض الفوارق النوعية.. لكنه لا يعني انقلاباً شاملاً في القوة الجوية',
        'Q6_ai': 'التكامل التقني أصبح عاملاً يأخذه العالم بجدية.. لأنه قد يصنع الفارق بسرعة بين قوتين تقليديتين',
        'Q7_industry': 'المغرب يسعى إلى الانتقال من استيراد السلاح إلى إنتاج جزء من قوته الدفاعية.. وهذا يرتبط باستقلالية القرار العسكري',
        'Q8_ecosystem': 'الصناعة الفعلية لا تعني إنشاء المصانع فقط.. بل بناء منظومة تشمل المهندسين والبحث والتطوير',
    }
    for k, q in qs.items():
        C.quote_card(k, QK, q, A)
    C.counter('N_show', [(200, 'عارض تقريباً', 0.3), (27, 'دولة مشاركة', 1.0)], 7, 'المصدر: منظمو معرض مراكش للطيران · أكتوبر 2026',
              title='معرض مراكش الدولي للطيران 2026')
    C.counter('N_25', [(25, 'مقاتلة F-16 Block 72\nطلبها المغرب', 0.3)], 7, 'المصدر: لوكهيد مارتن · صفقة أُقرّت في 2019')
    print('cards done')


if __name__ == '__main__':
    build()
