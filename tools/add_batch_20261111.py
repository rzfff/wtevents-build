#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""增量十一轮(2026-11-11):948→951。
+3 新事件:2026_the_great_war_nov 一战停战纪念日一战风云复刻(marathon,福克 D.VII/SPAD S.XIII 首开解锁)
          /sale_202611_c He 219 A-7 首飞纪念日返售 30% 折扣 /special_202611_c 挪威空军成立纪念贴花
素材源:EN 10316/10318/10322 + ZH 2874/2876/2879 全文(2026-11-11 经服务器抓取);
查重零命中(Great War 仅 2025 愚人节首秀版在册、He 219/挪威空军均无历史条目);
积压裁决:ANNOTATE 9EN+9ZH 全为 development/video 类按先例不收录(本批即其清零后的真增量)。
站长令(2026-11-01):活动内容写细一点——全字段充实。
"""
import json, io, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
P = r'E:\ah\wtevents-build\site\data\events.json'
d = json.load(io.open(P, encoding='utf-8'))
ev = d['events']
exist = {e['id'] for e in ev}

# ---------- A. 一战风云复刻(marathon) ----------
n1 = {
    'id': '2026_the_great_war_nov', 'type': 'marathon',
    'name_zh': '一战停战纪念日:「一战风云」限时复刻,福克 D.VII 与 SPAD S.XIII 开放解锁',
    'name_en': 'The Great War Returns With New Obtainable Aircraft to Mark November 11th!',
    'start': '2026-11-11T11:00:00Z', 'end': '2026-11-18T11:00:00Z', 'end_precision': 'hour',
    'end_raw': 'From November 11th until November 18th (11:00 GMT);北京时间 11 月 11 日 19:00 至 11 月 18 日 19:00',
    'dm_event': None,
    'vehicles': [
        {'id': 'fokker_d7', 'name_zh': '福克 D.VII', 'name_en': 'Fokker D.VII',
         'image': '/wtapi/assets/images/fokker_d7.png'},
        {'id': 'spad_13', 'name_zh': 'SPAD S.XIII', 'name_en': 'SPAD S.XIII',
         'image': '/wtapi/assets/images/spad_13.png'},
    ],
    'awards': ['达成指定阶段:福克 D.VII(德国)/SPAD S.XIII(法国)永久保留', '上轮活动装甲载具(德缴加福德等)同窗再次解锁'],
    'discounts': [],
    'deadlines': [],
    'tasks': ('「一战风云」活动模式中参加战斗并完成阶段任务,解锁对应阶段奖励;'
              '阶段奖励含一战载具,达成指定阶段的两架新战机可永久保留在账户中。'),
    'notes': ('为纪念一战停战纪念日(11 月 11 日)限时复刻「一战风云」模式:重返 1918 年西线法兰德斯战场,'
              '协约国 vs 同盟国,可指挥史上首批实战坦克、驾双翼机空战、亲自操控齐柏林飞艇轰炸地面,'
              '堑壕与无人区还原一战地形。上轮(2025-04 愚人节首秀)中福克 D.VII 与 SPAD S.XIII 标注'
              '「不可获得、将登 Aces of Thunder」,本轮首次开放解锁——错过上轮装甲载具的玩家也可补齐。'
              '福克 D.VII=公认一战德军最优秀战斗机,金属框架高抗过载,1918 年列装产量超 3000 架,'
              '2 挺中口径机枪带射击协调器;SPAD S.XIII 为法军一战名机。'),
    'sources': {'en': ['https://warthunder.com/en/news/10318'],
                'zh': ['https://warthunder.com/zh/news/2876']},
}

# ---------- B. He 219 A-7 首飞纪念返售(sale) ----------
n2 = {
    'id': 'sale_202611_c', 'type': 'sale',
    'name_zh': 'He 219 A-7 首飞纪念日:游戏内限时 30% 折扣返售',
    'name_en': 'The He 219 A-7 Returns with a Discount for the Anniversary of its First Flight!',
    'start': '2026-11-06T11:00:00Z', 'end': '2026-11-10T11:00:00Z', 'end_precision': 'hour',
    'end_raw': 'From November 6th (11:00 GMT) until November 10th (11:00 GMT)',
    'dm_event': None,
    'vehicles': [
        {'id': 'he_219a_7', 'name_zh': 'He 219 A-7', 'name_en': 'He 219 A-7',
         'image': '/wtapi/assets/images/he_219a_7.png'},
    ],
    'awards': [],
    'discounts': [
        {'target': 'He 219 A-7(德国 IV 级高级重型战斗机)',
         'item': '2,086 金鹰(限时 30% 折扣价);仅本促销期间可购买', 'percent': 30},
    ],
    'deadlines': [],
    'tasks': '',
    'notes': ('He 219「枭」夜间战斗机于 1942-11-06 首飞——设计师 Robert Lusser 曾与 Willy Messerschmitt '
              '共事 Bf 109,后转 Heinkel 参与喷气式 He 280 与 He 219,后者为其设计生涯收官之作; '
              '未获帝国航空部青睐仅量产 268 架。游戏内:IV 级重型战斗机,4×30mm+2×20mm 机炮火力凶悍, '
              '爬升快、生存性好、带机载雷达(同期罕见),机动性平庸;位置=德国>空战>高级载具。'),
    'sources': {'en': ['https://warthunder.com/en/news/10316'],
                'zh': ['https://warthunder.com/zh/news/2874']},
}

# ---------- C. 挪威皇家空军成立纪念贴花(special) ----------
n3 = {
    'id': 'special_202611_c', 'type': 'special',
    'name_zh': '挪威皇家空军成立纪念日:第 330 中队徽标贴花',
    'name_en': 'A Decal Marking the Anniversary of the Founding of the Royal Norwegian Air Force!',
    'start': '2026-11-10T12:00:00Z', 'end': '2026-11-13T12:00:00Z', 'end_precision': 'hour',
    'end_raw': 'From November 10th (12:00 GMT) until November 13th (12:00 GMT)',
    'dm_event': None, 'vehicles': [],
    'awards': ['「挪威皇家空军第 330 中队徽标」(Emblem of the No. 330 squadron RNoAF)贴花'],
    'discounts': [],
    'deadlines': [],
    'tasks': ('使用瑞典 III 级及以上飞机参战,累计 3,000 任务点即得贴花(随机战斗均可,排除[Assault]模式;'
              '完成后需手动领取:机库→昵称→成就→节假日→挪威空军成立日;贴花在自定义「节假日」页签下)。'),
    'notes': ('挪威航空始于 1912 年,独立空军 1944-11-10 正式成立——时值国王流亡英国、挪籍飞行员 '
              '编入皇家空军作战(第 330 中队即挪威人驾驶);战后挪威成北约创始国,以美制战机巡逻 '
              '对苏边境。游戏内挪威载具线在瑞典科技树内,故任务要求用瑞典飞机。'),
    'sources': {'en': ['https://warthunder.com/en/news/10322'],
                'zh': ['https://warthunder.com/zh/news/2879']},
}

for n in (n1, n2, n3):
    if n['id'] in exist:
        ev[ev.index(next(e for e in ev if e['id'] == n['id']))] = n
        print('↻', n['id'])
    else:
        ev.append(n)
        print('+', n['id'])

# ---------- D. meta ----------
d['generated_at'] = '2026-11-11T00:00:00Z'
d['counts'] = {
    'events': len(ev),
    'by_type': dict(Counter(e.get('type') for e in ev)),
    'with_discounts': sum(1 for e in ev if e.get('discounts')),
}
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', d['counts']['by_type'])
print('SAVED')
