#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-09-28 审计修复:拆分 zh挂接 错配产生的嵌合记录(10 组)+ 修正 2026-12 幽灵条目。
每处修改的依据见 AUDIT_EVIDENCE 注释;只改本地,部署另行执行。"""
import json, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

SITE = 'E:/ah/wtevents-build/site/data/events.json'
BUILD = 'E:/ah/wtevents-build/data/events_build.json'
Z = lambda n: f'https://warthunder.com/zh/news/{n}'
E = lambda n: f'https://warthunder.com/en/news/{n}'

d = json.load(open(SITE, encoding='utf-8'))
events = {e['id']: e for e in d['events']}
log = []
taken = set(events)

def rid(base):
    if base not in taken: taken.add(base); return base
    i = 0
    while True:
        i += 1
        cand = f"{base}_{'abcdefg'[i-1]}"
        if cand not in taken: taken.add(cand); return cand

touched=set()

def sel(eid):
    touched.add(eid)
    return events[eid]

def rm_src(eid, lang, nid, why):
    e = sel(eid); urls = e['sources'].get(lang) or []
    u = (Z if lang == 'zh' else E)(nid)
    if u in urls:
        urls.remove(u); e['sources'][lang] = urls or None
        log.append(f'{eid}: 移除 {lang}/{nid} ({why})')

def add_src(eid, lang, nid, why):
    e = sel(eid); urls = e['sources'].get(lang) or []
    u = (Z if lang == 'zh' else E)(nid)
    if u not in urls:
        urls.append(u); e['sources'][lang] = urls
        log.append(f'{eid}: 挂接 {lang}/{nid} ({why})')

def mk(eid_base, type_, zh, en, start, end, prec, conf, srcs, note=None):
    eid = rid(eid_base)
    events[eid] = {
        'id': eid, 'type': type_, 'name_zh': zh, 'name_en': en, 'bp_season': None,
        'start': start, 'end': end, 'end_precision': prec, 'end_raw': None,
        'dm_event': None, 'vehicles': [], 'awards': [], 'discounts': [],
        'deadlines': [], 'sub_events': [], 'tasks': None, 'notes': note,
        'sources': srcs, 'confidence': conf,
    }
    log.append(f'+ 新建 {eid} [{type_}] {start}→{end} | {(zh or en)[:36]}')
    touched.add(eid)
    return events[eid]

# ---- 1. special_202510_c = Deep Strike(en) + 周年庆商城折扣(zh) 错配 ----------
rm_src('special_202510_c', 'zh', 2357, '周年庆商城折扣≠Deep Strike,周年庆折扣归 anniversary_202510')
sel('special_202510_c')['type'] = 'special'
sel('special_202510_c')['name_zh'] = None
sel('special_202510_c')['confidence'] = 0.8
add_src('anniversary_202510', 'zh', 2357, 'zh/2357=13周年商城折扣= en/9778 中文版')
sel('anniversary_202510')['name_zh'] = '周年庆 Gaijin 商城折扣现已开启！'
sel('anniversary_202510')['end'] = '2025-11-03T11:00:00Z'   # en/9778: 29 Oct→3 Nov 11:00 GMT
sel('anniversary_202510')['confidence'] = 0.9

# ---- 2. special_202411 = KV-7 直播活动(en/9183) + 12周年庆典(zh/1815) 错配 ----
rm_src('special_202411', 'zh', 1815, '12周年庆典开启= en/9178 中文版,应挂 anniversary_202411')
sel('special_202411')['name_zh'] = '开 KV，上刺刀，奖券直播抽彩票！IS-7 周年来报到！'
sel('special_202411')['type'] = 'special'
sel('special_202411')['confidence'] = 0.75
add_src('anniversary_202411', 'zh', 1815, '同上')
sel('anniversary_202411')['name_zh'] = '战争雷霆十二周年庆典活动开启！'
sel('anniversary_202411')['confidence'] = 0.7

# ---- 3. festive_202110_d 万圣节 背上的「祝War Thunder生日快乐」 ----------------
rm_src('festive_202110_d', 'zh', 444, '9周年生日帖≠万圣节')
mk('anniversary_202111_b', 'anniversary', '祝War Thunder生日快乐！', None,
   '2021-11-01T11:00:00Z', '2021-11-08T11:00:00Z', 'hour', 0.6,
   {'en': None, 'zh': [Z(444)]},
   note='9周年庆典(zh 页 2021-11-01;鼠式 11/1 19:00–11/8 19:00 北京时间);en 原文未入库')

# ---- 4. sale_202410_c 12周年商城特卖 背上的 J-35 帖 --------------------------
rm_src('sale_202410_c', 'zh', 1797, 'J-35首飞返售≠12周年特卖')
sel('sale_202410_c')['name_zh'] = '周年庆惊爆特卖，尽在 Gaijin 商城！'
mk('sale_202410_d', 'sale', 'J 35 首飞纪念，A 型限时返售 & 同享折扣！',
   'The J35A Draken Temporarily Returns at a Discount for the Anniversary of its First Flight',
   '2024-10-25T11:00:00Z', '2024-10-28T09:00:00Z', 'hour', 0.8,
   {'en': [E(9160)], 'zh': [Z(1797)]})   # en/9160: from today(10/25) until 10/28 09:00 GMT

# ---- 5. special_202504_e 步兵背包(en) 背上的 欧洲胜利日(zh) -------------------
rm_src('special_202504_e', 'zh', 2079, '胜利日特卖≠Infantry Backpack')
rm_src('special_202504_e', 'zh', 2080, '胜利日80周年≠Infantry Backpack')
sel('special_202504_e')['name_zh'] = None
sel('special_202504_e')['end'] = None; sel('special_202504_e')['end_precision'] = None
sel('special_202504_e')['confidence'] = 0.6   # 原 end 05-07 系 zh 胜利日帖拉长,无英文依据
mk('memorial_202505', 'memorial', '欧洲战场胜利日 80 周年纪念活动隆重开幕！',
   'Celebrate the 80th Anniversary of Victory Day!',
   '2025-05-07T11:00:00Z', None, None, 0.7,
   {'en': [E(9492)], 'zh': [Z(2079), Z(2080)]})   # en/9492 2025-05-07

# ---- 6. special_202307 原子之心(en) 背上的 哈士奇行动(zh) --------------------
rm_src('special_202307', 'zh', 1082, '哈士奇80周年≠原子之心联动')
sel('special_202307')['name_zh'] = None
sel('special_202307')['confidence'] = 0.6
mk('memorial_202307', 'memorial', '哈士奇行动 80 周年纪念贴花及装饰品',
   'A Decal and a 3D Decoration Commemorating 80 years from Operation Husky',
   '2023-07-07T13:00:00Z', '2023-07-10T13:00:00Z', 'hour', 0.85,
   {'en': [E(8349)], 'zh': [Z(1082)]})   # en/8349: 7 Jul 13:00 → 10 Jul 13:00 GMT

# ---- 7. sale_202408_c 欧根亲王号(en) 背上的 狂风+波兰(zh) --------------------
rm_src('sale_202408_c', 'zh', 1666, '狂风首飞50周年≠Prinz Eugen')
rm_src('sale_202408_c', 'zh', 1667, '波兰建军节≠Prinz Eugen')
sel('sale_202408_c')['name_zh'] = None
mk('sale_202408_d', 'sale', '狂风首飞 50 周年纪念，折扣与贴花活动登场！',
   '50th Anniversary of the Tornado’s First Flight: A Special Decal & Discounts',
   '2024-08-14T11:00:00Z', '2024-08-19T07:00:00Z', 'hour', 0.85,
   {'en': [E(9021)], 'zh': [Z(1666)]})   # en/9021 2024-08-14, until 19 Aug 07:00 GMT
mk('memorial_202408_b', 'memorial', '波兰建军纪念日：瓦诺夫斯基座机限时返售，全新贴花登场！',
   'Polish Armed Forces Day: Lanovski’s P-47M-1-RE and a New Decal!',
   '2024-08-15T11:00:00Z', '2024-08-19T09:00:00Z', 'hour', 0.8,
   {'en': [E(9022)], 'zh': [Z(1667)]})   # zh/1667: 至北京时间 8/19 17:00

# ---- 8. festive_202408 建军节(en/9007) 背上的 狂风/波兰/美空降 ---------------
rm_src('festive_202408', 'en', 9021, '狂风50周年≠PLA Day → sale_202408_d')
rm_src('festive_202408', 'en', 9022, '波兰建军节≠PLA Day → memorial_202408_b')
rm_src('festive_202408', 'en', 9024, '美空降兵节≠PLA Day')
sel('festive_202408')['type'] = 'memorial'
mk('memorial_202408_c', 'memorial', None,
   'US Airborne Day: Get Yourself a New Decal & the UH-1C XM-30!',
   '2024-08-16T11:00:00Z', None, None, 0.65,
   {'en': [E(9024)], 'zh': None})

# ---- 9. special_202406 D-Day(en) 背上的 幻影鸢+瑞典(zh);同时挂错 en/8908 ----
rm_src('special_202406', 'zh', 1557, '幻影鸢首飞返售≠D-Day 80')
rm_src('special_202406', 'zh', 1558, '瑞典国防纪念日≠D-Day 80')
sel('special_202406')['name_zh'] = None
sel('special_202406')['confidence'] = 0.8
rm_src('special_202405', 'en', 8908, 'Milan 返售≠法国海军节')
mk('sale_202405_b', 'sale', '幻影“鸢”原型机首飞纪念，稀有载具限时返场！',
   'The Milan Temporarily Returns on the Anniversary of its First Flight!',
   '2024-05-29T13:00:00Z', '2024-05-31T13:00:00Z', 'hour', 0.85,
   {'en': [E(8908)], 'zh': [Z(1557)]})   # zh: 北京时间 5/29 21:00 → 5/31 21:00
mk('memorial_202405', 'memorial', '瑞典国防纪念日贴花活动 + 稀有载具限时返场！',
   'The SAV 20.12.48 and a Decal are Available for Swedish National Security Forces Day!',
   '2024-05-29T14:00:00Z', '2024-05-31T12:00:00Z', 'hour', 0.85,
   {'en': [E(8909)], 'zh': [Z(1558)]})   # zh: 北京时间 5/29 22:00 → 5/31 20:00

# ---- 10. special_202405 法国海军节 背上的 皇家工程兵团(en/8896+zh/1547) -------
rm_src('special_202405', 'zh', 1547, '皇家工程兵团≠法国海军节')
rm_src('special_202405', 'en', 8896, '同上')
mk('memorial_202405_b', 'memorial', '英国皇家工程兵团成立纪念日：百夫长 AVRE 返场！',
   'Anniversary of the Founding of the Corps of Royal Engineers',
   '2024-05-24T11:00:00Z', None, None, 0.7,
   {'en': [E(8896)], 'zh': [Z(1547)]})

# ---- 11. festive_202401 瑞典国防日(en/8691) 背上的 年终双节(zh/1344) ---------
rm_src('festive_202401', 'zh', 1344, '年终双节促销≠瑞典国防日')
sel('festive_202401')['name_zh'] = '瑞典武装部队纪念日：SAV 20.12.48 返售 & 贴花活动！'
mk('sale_202312_b', 'sale', '与战争雷霆一起欢庆年终双节！', None,
   '2023-12-20', None, None, 0.55,
   {'en': None, 'zh': [Z(1344)]})   # zh/1344 2023-12-20;en 原文未入库

# ---- 12. market_202612 幽灵条目:zh/2448 显示日期 2026-12-29 为 warthunder.com
#          zh 页渲染错年,真实日期 2025-12-29(= en/9873,已被 market_202512 收录)---
dup = sel('market_202512')
zsrc = sel('market_202612')
if Z(2448) not in (dup['sources'].get('zh') or []):
    add_src('market_202512', 'zh', 2448, 'zh/2448= en/9873 中文版;zh页显示2026为错年')
if not dup.get('name_zh'):
    dup['name_zh'] = zsrc.get('name_zh')
for x in zsrc.get('discounts') or []:
    if not any((x.get('target'), (x.get('item') or '')[:30]) == ((y.get('target')), (y.get('item') or '')[:30]) for y in dup.get('discounts') or []):
        dup.setdefault('discounts', []).append(x)
dup['confidence'] = 0.75
log.append(f"- 删除 market_202612 (幽灵条目 2026-12-29,并入 market_202512)")
del events['market_202612']

# ---- 校验 + 写盘 ------------------------------------------------------------
errs = []
seen = set()
for eid, e in events.items():
    if eid in seen: errs.append(f'重复id {eid}')
    seen.add(eid)
    if eid in touched and not (e['sources'].get('en') or e['sources'].get('zh')): errs.append(f'{eid} 无来源')
    if e.get('start') and e.get('end') and e['end'][:10] < e['start'][:10]: errs.append(f'{eid} end<start')
if errs:
    print('校验失败:'); [print(' ', x) for x in errs]; sys.exit(1)

out = sorted(list(events.values()), key=lambda x: (x.get('start') or x.get('end') or '0000'), reverse=True)
d['events'] = out
d['generated_at'] = '2026-09-28T00:00:00Z'
d['build'] = 'm2-audit1'
d['counts'] = {
    'events': len(out),
    'by_type': dict(Counter(e['type'] for e in out)),
    'with_vehicles': sum(1 for e in out if e.get('vehicles')),
    'with_zh_name': sum(1 for e in out if e.get('name_zh')),
    'with_end': sum(1 for e in out if e.get('end')),
    'with_discounts': sum(1 for e in out if e.get('discounts')),
    'm2_new': d['counts'].get('m2_new', 736),
}
d['audit_note'] = '2026-09-28 审计修复:拆分 10 组 zh挂接 错配嵌合记录,删除 2026-12 幽灵条目;详见 tools/fix_audit_20260928.py'
json.dump(d, open(SITE, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
d2 = json.loads(json.dumps(d))
json.dump(d2, open(BUILD, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'== 完成: {len(out)} 条 (原 862), 改动 {len(log)} 处 ==')
for x in log: print(' ', x)
