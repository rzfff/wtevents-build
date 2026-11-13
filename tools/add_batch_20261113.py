#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""增量十二轮(2026-11-13):956→960。
+4 新事件:special_202611_d 波兰国家独立日 / special_202611_e 中国空军节 /
          sale_202611_d 德国联邦国防军成立日 / festive_202611 十一月月度贴花
素材:EN 10325/10328/10329/10330 + ZH 2883/2884/2888/2887 全文(newev.txt);
10323 大版本发布文历代无收录先例跳过;10331 电竞/10332·10327 开发/10333 修障跳过。
站长令(2026-11-01):活动内容写细一点。
"""
import json, io, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
P = r'E:\ah\wtevents-build\site\data\events.json'
d = json.load(io.open(P, encoding='utf-8'))
ev = d['events']
exist = {e['id'] for e in ev}

n1 = {
 'id': 'special_202611_d', 'type': 'special',
 'name_zh': '波兰国家独立日:兰诺夫斯基 P-47M-1-RE 返售与贴花物资箱',
 'name_en': "A Decal Trophy and Lanovski's P-47M-1-RE Thunderbolt for Poland's National Independence Day!",
 'start': '2026-11-11T11:00:00Z', 'end': '2026-11-14T11:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From November 11th (11:00 GMT) until November 14th (11:00 GMT)',
 'dm_event': None,
 'vehicles': [
  {'id': 'p47m_1re_lanovski', 'name_zh': '兰诺夫斯基的 P-47M-1-RE 雷电', 'name_en': "Lanovski's P-47M-1-RE",
   'image': '/wtapi/assets/images/p47m_1re_lanovski.png'},
 ],
 'awards': ['「波兰国家独立日」物资箱(五枚往期节日贴花之一:波兰翼盔帽徽/攻击之鹰/波兰凤凰等;集齐五枚改得:20-50% 研发或银狮加成卡/3-5 备用载具/1 天高级账号/「Kotwica 锚」贴花)'],
 'discounts': [
  {'target': "兰诺夫斯基的 P-47M-1-RE 雷电(美 III 级高级战机)", 'item': '4,263 金鹰(限时 30% 折扣);仅本促销期间可购', 'percent': 30},
 ],
 'deadlines': [],
 'tasks': ('使用美国或英国 III 级及以上载具累计 3000 任务分(随机战斗,排除[Assault])→物资箱;'
           '完成后手动领取(昵称→成就→节假日→波兰国家独立日)'),
 'notes': ('1918-11-11 一战结束德军撤出波兰,该国自 1795 年瓜分以来首次复国独立,今为波兰首要国庆日。'
           '兰诺夫斯基=波兰王牌,先后服役皇家空军与美国陆航,座机 P-47M-1-RE 带专属涂装,'
           '8×12.7mm 勃朗宁+HVAR 火箭+250-1000 磅炸弹。'),
 'sources': {'en': ['https://warthunder.com/en/news/10325'], 'zh': ['https://warthunder.com/zh/news/2883']},
}

n2 = {
 'id': 'special_202611_e', 'type': 'special',
 'name_zh': '中国人民解放军空军建军节:贴花物资箱',
 'name_en': 'A Decal Trophy for Chinese Air Force Day!',
 'start': '2026-11-11T12:00:00Z', 'end': '2026-11-14T12:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From November 11th (12:00 GMT) until November 14th (12:00 GMT)',
 'dm_event': None, 'vehicles': [],
 'awards': ['「解放军空军节」物资箱(五枚贴花之一:PLAAF 龙旅徽标/空军节/PLAAF 军旗/空军 V 形臂章;集齐改得:加成卡/备用载具/1 天高级账号/「解放军空军徽标」贴花)'],
 'discounts': [], 'deadlines': [],
 'tasks': ('使用中国 III 级及以上飞机累计 3000 任务分(随机战斗,排除[Assault])→物资箱;完成后手动领取'
           '(昵称→成就→节假日→解放军空军节);贴花在「中国→空军」自定义分类'),
 'notes': ('解放军空军 1949-11-11 正式成立;现役约 40 万人、2,500 余架作战飞机、860 余部地空导弹发射架。'),
 'sources': {'en': ['https://warthunder.com/en/news/10328'], 'zh': ['https://warthunder.com/zh/news/2884']},
}

n3 = {
 'id': 'sale_202611_d', 'type': 'sale',
 'name_zh': '德国联邦国防军成立日:Pz.Sfl.Ic 与四号/70(A) 返售折扣+贴花物资箱',
 'name_en': 'A Decal Trophy and Discounts for Bundeswehr Foundation Day!',
 'start': '2026-11-12T10:00:00Z', 'end': '2026-11-16T10:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From November 12th (10:00 GMT) until November 16th (10:00 GMT)',
 'dm_event': None,
 'vehicles': [
  {'id': 'germ_pz_sfl_ic', 'name_zh': 'Pz.Sfl.Ic', 'name_en': 'Pz.Sfl.Ic',
   'image': '/wtapi/assets/images/germ_pz_sfl_ic.png'},
  {'id': 'germ_panzerjager_iv_70_a', 'name_zh': '四号坦克歼击车/70(A)', 'name_en': 'Panzer IV/70(A)',
   'image': '/wtapi/assets/images/germ_panzerjager_iv_70_a.png'},
 ],
 'awards': ['「联邦国防军成立日」物资箱(四枚贴花之一:联邦国防军日×2/国防军 V 形臂章/国防军指挥部 V 形臂章;集齐改得:加成卡/备用载具/1 天高级账号)'],
 'discounts': [
  {'target': 'Panzer IV/70(A)(德 III 级坦克歼击车)', 'item': '2,086 金鹰(限时折扣返售)', 'percent': None},
  {'target': 'Pz.Sfl.Ic(德 II 级试验轻型歼击车)', 'item': '限时折扣返售(金鹰价见游戏内)', 'percent': None},
 ],
 'deadlines': [],
 'tasks': ('使用德国 III 级及以上载具累计 3000 任务分(随机战斗,排除[Assault])→物资箱;完成后手动领取;'
           'V 形臂章类贴花在「德国→陆军」分类,其余在「节假日」分类'),
 'notes': ('1945 年国防军解散,1955 年中西德联邦国防部成立;11-12 首批新兵宣誓,1956-01-02 正式得名「联邦国防军」;'
           '1957 年征兵制,一年后兵力 20 万。Pz.Sfl.Ic=II 号底盘装 50mm Pak 38 的早期试验车,同级穿深顶级但防护脆;'
           '四号/70(A)=IV 号底盘歼击车,机动比肩中坦、75mm 穿深惊喜,忌对线。'),
 'sources': {'en': ['https://warthunder.com/en/news/10329'], 'zh': ['https://warthunder.com/zh/news/2888']},
}

n4 = {
 'id': 'festive_202611', 'type': 'festive',
 'name_zh': '十一月月度历史贴花(埃米尔·贝尔坦/StuG.Brig 232 等)',
 'name_en': 'Monthly Decals for November!',
 'start': '2026-11-12T11:00:00Z', 'end': '2026-12-11T09:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From November 12th (11:00 GMT) until December 11th (09:00 GMT)',
 'dm_event': None, 'vehicles': [], 'awards': [], 'discounts': [], 'deadlines': [],
 'tasks': ('五枚历史贴花各自任务(III 级及以上载具):①「埃米尔·贝尔坦徽标(后期)」——法国远洋舰艇造成 20000 伤害;'
           '②「Stu.Brig 232 徽标」——德国坦克歼击车击毁 40 名玩家;③「权杖之牌徽标」——意大利地面载具打 20 场(活跃度≥60%);'
           '④「伦敦的复仇」机头艺术(加拿大)——英国轰炸机造成 10 吨基础伤害;⑤「神风特攻战队徽标」——日本飞机击毁 50 名玩家'),
 'notes': ('月度历史贴花系列。①埃米尔·贝尔坦号轻巡洋舰后期徽标:初代 1930 年代徽标含日本鸟居(舰名来源贝尔坦曾旅日),'
           '二战对日冲突后于 1943 年费城改装时改版——美洲豹象征航速、三色剪影纪念自由法国流亡作战;'
           '②第 232 突击炮旅 1942-11-10 于于特博格组建,原定北非后转东线。'),
 'sources': {'en': ['https://warthunder.com/en/news/10330'], 'zh': ['https://warthunder.com/zh/news/2887']},
}

for n in (n1, n2, n3, n4):
    if n['id'] in exist:
        ev[ev.index(next(e for e in ev if e['id'] == n['id']))] = n; print('↻', n['id'])
    else:
        ev.append(n); print('+', n['id'])

d['generated_at'] = '2026-11-13T14:00:00Z'
d['counts'] = {'events': len(ev), 'by_type': dict(Counter(e.get('type') for e in ev)),
               'with_discounts': sum(1 for e in ev if e.get('discounts'))}
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', d['counts']['by_type'])
print('SAVED')
