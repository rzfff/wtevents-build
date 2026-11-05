#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""增量十轮(2026-11-05):946→948。
+2 新事件:sale_202611_b 号角Mk1B最优构型+JAS39-5 预购 / special_202611_b 意大利国家统一日
+festive_202610_b 补挂 zh 源 2843(首轮滞后官方文,窗口与在册一致)+奖励细节充实
素材源:EN 10307/10308 全文(2026-11-04)+哨兵 11-05;查重零命中(Olifant/JAS39-5/2026 意统一日均无)
站长令(2026-11-01):活动内容写细一点——全字段充实。
"""
import json, io, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
P = r'E:\ah\wtevents-build\site\data\events.json'
d = json.load(io.open(P, encoding='utf-8'))
ev = d['events']
by = {e['id']: e for e in ev}

def src(e, en=None, zh=None):
    """en/zh 必须传列表(铁律:传字符串=逐字符爆炸)。"""
    s = e.setdefault('sources', {'en': [], 'zh': []})
    if s is None:
        s = e['sources'] = {'en': [], 'zh': []}
    for k, ids in (('en', en), ('zh', zh)):
        for i in (ids or []):
            assert re.fullmatch(r'\d{3,}', i), f'src id 形态可疑: {i!r}'
            u = f'https://warthunder.com/{k}/news/{i}'
            if u not in s.setdefault(k, []):
                s[k].append(u)

# ---------- A. 新事件 1:预购双礼包 ----------
n1 = {
    'id': 'sale_202611_b', 'type': 'sale',
    'name_zh': '号角 Mk.1B 最优构型与 JAS 39-5 礼包开启预售',
    'name_en': 'Pre-orders: Olifant Mk.1B Optimering and JAS39-5',
    'start': '2026-11-04', 'end': None, 'end_precision': 'none',
    'end_raw': '预售自 11-04 起,随下个大版本实装截止(未公布固定结束时间)',
    'dm_event': None,
    'vehicles': [
        {'id': 'uk_olifant_optimering', 'name_zh': '号角 Mk.1B 最优构型', 'name_en': 'Olifant Mk.1B Optimering',
         'image': '/wtapi/assets/images/uk_olifant_optimering.png'},
        {'id': 'saab_jas39e', 'name_zh': 'JAS39-5', 'name_en': 'JAS39-5',
         'image': '/wtapi/assets/images/saab_jas39e.png'},
    ],
    'awards': ['预购赠品:「战象」称号+「战象」贴花(号角包)', '「聪明的战斗机」称号+「皇家狮鹫」贴花(JAS 39-5 包)'],
    'discounts': [
        {'target': 'Olifant Mk.1B Optimering Pack(英 VI 级高级坦克,南非号角系列)',
         'item': '$59.99:含本车+15 天高级账号+2000 金鹰+预购称号与贴花', 'percent': None},
        {'target': 'JAS39-5 Pack(瑞典 VIII 级高级战机,鹰狮预生产型)',
         'item': '$79.99:含本机+30 天高级账号+3000 金鹰+预购称号与贴花', 'percent': None},
    ],
    'tasks': [],
    'notes': ('号角 Mk.1B 最优构型=百年 Centurion 平台南非末代进化:全新焊接炮塔正面强化+弹药泄压板+热成像,'
              '105mm 炮可发 DM63 APFSDS(与 Mk.2 同炮),机动均衡;软肋=乘员舱布置局促+侧向易起火。'
              'JAS 39-5=鹰狮预生产型:高速+鸭翼高机动,RB99 主动雷达弹开长程 interception,中距半主动、'
              '近距全向红外齐备,对地挂激光制导炸弹/电视制导导弹,翼下可挂额外干扰弹吊舱。'
              '⚠ 官方声明:实装前性能可能调整。'),
    'sources': {'en': ['https://warthunder.com/en/news/10307'],
                'zh': ['https://warthunder.com/zh/news/2866']},
}

# ---------- B. 新事件 2:意大利国家统一日 ----------
n2 = {
    'id': 'special_202611_b', 'type': 'special',
    'name_zh': '意大利国家统一日与武装部队日:Leoncello 双车五折+贴花战利品箱',
    'name_en': "A Decal Trophy and Discounts for Italy's National Unity and Armed Forces Day",
    'start': '2026-11-04T11:00:00Z', 'end': '2026-11-07T11:00:00Z', 'end_precision': 'hour',
    'end_raw': 'From November 4th (11:00 GMT) until November 7th (11:00 GMT)',
    'dm_event': None, 'vehicles': [],
    'awards': ['「意大利国家统一与武装部队日」战利品箱(四选一历史贴花:国庆日/意大利之心/神射手帽章/意大利统一;集齐四枚则改得加成器/备用载具/1 天高级账号)'],
    'discounts': [
        {'target': 'P40 "G.C. Leoncello"(意 II 级)', 'item': '金鹰购买 5 折(现价 575 金鹰);限量约 100 辆的稀有中型坦克', 'percent': 50},
        {'target': 'M43 "G.C. Leoncello"(意 III 级)', 'item': '金鹰购买 5 折(现价 650 金鹰);意大利战役中谢尔曼杀手,HEAT 弹穿深可观', 'percent': 50},
    ],
    'deadlines': [],
    'tasks': ('任意 III 级及以上意大利载具攒 3000 任务点→战利品箱(随机战斗均可,排除[Assault]模式;'
              '完成后需在 机库→成就→节假日 手动领取)'),
    'notes': ('意大利国家统一日=纪念一战奥匈投降、意大利收复特伦托与的里雅斯特完成统一(1919 年起庆祝);'
              'P40/M43 "G.C. Leoncello" 为历年同日返售传统车(2021/2022/2024/2025 版本均在册)。'),
    'sources': {'en': ['https://warthunder.com/en/news/10308'],
                'zh': ['https://warthunder.com/zh/news/2868']},
}

exist = {e['id'] for e in ev}
for n in (n1, n2):
    if n['id'] in exist:
        ev[ev.index(next(e for e in ev if e['id'] == n['id']))] = n  # upsert:重跑时以脚本为准
        print('↻', n['id'])
    else:
        ev.append(n)
        print('+', n['id'])

# ---------- C. 万圣节竞速:补 zh 源 + 奖励细节充实(窗口不变,2843=首轮滞后官方文) ----------
f = by['festive_202610_b']
src(f, zh=['2843'])
f['awards'] = [
    '「不祥之地」头像边框(陆战竞速「穿越黑暗森林」获 750 分)',
    '「绿色幽灵」联队徽标(空战竞速「猎杀魔女」获 750 分)',
    '「Boo!」贴花(任意 III 级+载具,随机战斗活跃度≥70% 得 3000 分)',
    '「魔女的大锅」装饰挂件物资箱(陆战竞速 500 分;杀人狂大砍刀/食人族斧头/女巫帽/杀人狂面具四选一)',
    '「聚魂棺」贴花物资箱(空战竞速 300 分;死神/蜗牛杀人狂/愤怒黑猫/脑洞大开等往期万圣节贴花)',
]

# ---------- D. meta ----------
d['generated_at'] = '2026-11-05T00:00:00Z'
d['counts'] = {
    'events': len(ev),
    'by_type': dict(Counter(e.get('type') for e in ev)),
    'with_discounts': sum(1 for e in ev if e.get('discounts')),
}
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', d['counts']['by_type'])
print('SAVED')
