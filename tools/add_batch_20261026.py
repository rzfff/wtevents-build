#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-10-26 补漏:6 事件(特拉法尔加/加拿大海军/UH-1C/黄貂鱼II预购/14周年/J35A龙式)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

V = lambda id, zh, en: ({'id': id, 'name_zh': zh, 'name_en': en, 'image': f'/wtapi/assets/images/{id}.png'} if zh else {'id': id, 'name_en': en, 'image': f'/wtapi/assets/images/{id}.png'})

NEW = [
 dict(id='sale_202610_g', type='sale',
   name_zh='特拉法尔加海战纪念日舰艇返售与折扣活动开启', name_en='A Decal and Discount on British Ships for the Battle of Trafalgar Anniversary!',
   bp_season=None, start='2026-10-19T12:00:00Z', end='2026-10-26T12:00:00Z', end_precision='hour',
   end_raw='From October 19th (12:00 GMT) until October 26th (12:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[],
   discounts=[
     dict(target='HMS Nelson 礼包(Gaijin 商店)', item='含纳尔逊号(英 VI 级战列舰)+3000 金鹰+30 天高级;79.99→55.99 美元', percent=30),
     dict(target='Fairmile D (5001)(英 III 级近岸艇)', item='910 金鹰;-30%;仅本次促销期间可购', percent=30),
     dict(target='HMS Belfast(英 VII 级轻巡)/HMS Iron Duke(英 V 级战列舰)', item='30% 折扣;商店位:英国>近岸/远洋舰队>高级载具', percent=30)],
   deadlines=[], sub_events=[], tasks=None,
   notes='特拉法尔加海战纪念日(1805-10-21 纳尔逊击败法西联合舰队,英方零战列舰损失);礼包窗口 10/21-10/24 11:00 GMT。', confidence=0.9),

 dict(id='sale_202610_h', type='sale',
   name_zh='纪念加拿大涅厄泊日海达人号限时返场', name_en='Honoring the Canadian Navy with a Discount on HMCS Haida on Niobe Day!',
   bp_season=None, start='2026-10-21T13:00:00Z', end='2026-10-24T13:00:00Z', end_precision='hour',
   end_raw='From October 21st (13:00 GMT) until October 24th (13:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[], discounts=[
     dict(target='HMCS Haida(英 III 级驱逐舰)', item='3416 金鹰;-30%;仅本次促销期间可购;商店位:英国>远洋舰队>高级载具', percent=30)],
   deadlines=[], sub_events=[], tasks=None,
   notes='加拿大海军建军节/涅厄泊日(1910-10-21 巡洋舰 HMCS Niobe 抵达哈利法克斯,加海军成立);Haida 号参加过二战与朝鲜战争。', confidence=0.9),

 dict(id='sale_202610_i', type='sale',
   name_zh='UH-1 首飞纪念日 XM-30 型再次折扣返售', name_en='Discount on the UH-1C XM-30 on the First Flight Anniversary!',
   bp_season=None, start='2026-10-22T11:00:00Z', end='2026-10-26T11:00:00Z', end_precision='hour',
   end_raw='From October 22nd (11:00 GMT) until October 26th (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[], discounts=[
     dict(target='UH-1C XM-30(美直升机)', item='6237 金鹰;-30%;仅本次促销期间可购;商店位:美国>直升机>高级载具', percent=30)],
   deadlines=[], sub_events=[], tasks=None,
   notes='UH-1 休伊首飞纪念(1956-10-20,越战标志性直升机,超 16000 架);XM-30 型可挂 30mm XM140 航炮/M75 榴弹发射器/M134/FFAR/BGM-71C。', confidence=0.9),

 dict(id='sale_202610_j', type='sale',
   name_zh='虹鱼 II 礼包开启预售', name_en='Pre-order: Stingray II — The Upgraded Commando',
   bp_season=None, start='2026-10-22T11:00:00Z', end=None, end_precision='none',
   end_raw='预购开放至下个大版本上线(时间未公布)',
   dm_event=None, vehicles=[],
   awards=['预购专属:「Sting like a ray」称号、「蓝点魟鱼」贴花'],
   discounts=[dict(target='虹鱼 II 礼包(Gaijin 商店,预购)', item='含虹鱼 II(美 VI 级轻坦)+15 天高级+2000 金鹰;59.99 美元(无折扣,预购价)', percent=None)],
   deadlines=[], sub_events=[], tasks=None,
   notes='美系第二辆高级顶级轻坦(指挥官虹鱼改进型):热成像/DM33/105mm 稳定炮/71km/h;弱点=倒车慢;随下个大版本实装。', confidence=0.85),

 dict(id='anniversary_202610', type='anniversary',
   name_zh='战争雷霆十四周年庆即将来袭游戏内折扣现已开启', name_en="In-Game Discounts for War Thunder's 14th Birthday!",
   bp_season=None, start='2026-10-23T11:00:00Z', end='2026-10-28T11:00:00Z', end_precision='hour',
   end_raw='From October 23rd (11:00 GMT) until October 28th (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[],
   discounts=[
     dict(target='全国家载具(银狮/金鹰购买)', item='50% 折扣;不含 Sky Odyssey 和 Heavy Cavalry 大版本新增车', percent=50),
     dict(target='全部改装件/护身符/备用载具', item='50% 折扣(同上排除条款)', percent=50),
     dict(target='高级账号(90/365 天游戏内+180 天商店)', item='50% 折扣', percent=50)],
   deadlines=[], sub_events=[], tasks=None,
   notes='战争雷霆 14 周年(游戏 2012-11-01 上线);官方预告「庆典才刚开始,更多内容即将到来」。', confidence=0.9),

 dict(id='sale_202610_k', type='sale',
   name_zh='龙首飞纪念日 J 35A 同步回归限价加入周年庆折扣', name_en="The J35A Returns with a Discount for the Dragon's First Flight!",
   bp_season=None, start='2026-10-23T13:00:00Z', end='2026-10-28T11:00:00Z', end_precision='hour',
   end_raw='From October 23rd (13:00 GMT) until the end of in-game discounts for War Thunder\'s Birthday, October 28th (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[], discounts=[
     dict(target='J35A 龙式(瑞典 VI 级战机)', item='4545 金鹰(原价 9090);-50%;促销后永久回归原价', percent=50),
     dict(target='Saab J35XS(瑞典 VII 级战机)', item='4635 金鹰;-50%;商店位:瑞典>航空>高级载具', percent=50)],
   deadlines=[], sub_events=[], tasks=None,
   notes='SAAB 35 龙首飞纪念(1955-10-25,双三角翼,首架西欧超音速战机,马赫 2,服役至 2005);J35A 无对抗措施;J35XS 携 12 枚对抗措施+RB27/RB28。', confidence=0.9),
]

for p in ['E:/ah/wtevents-build/site/data/events.json', 'E:/ah/wtevents-build/data/events_build.json']:
    d = json.load(open(p, encoding='utf-8'))
    existing_ids = {e['id'] for e in d['events']}
    for ev in NEW:
        if ev['id'] in existing_ids:
            print(f'WARNING: {ev["id"]} already exists, will overwrite')
    d['events'] = [e for e in d['events'] if e['id'] not in {x['id'] for x in NEW}] + NEW
    d['events'].sort(key=lambda x: (x.get('start') or x.get('end') or '0000'), reverse=True)
    from collections import Counter
    d['counts'] = {'events': len(d['events']), 'by_type': dict(Counter(e['type'] for e in d['events'])),
                   'with_discounts': sum(1 for e in d['events'] if e.get('discounts'))}
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if 'site' in p else None)
    print(p.split('/')[-3], 'total', d['counts']['events'])
print('BATCH_DONE')
