#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M3 Wayback 整合:折价商品运行段 → 既有 sale 事件增补 / 生成 wayback_YYYYMM 事件;幂等(重跑先清 wayback 来源增补)"""
import json, os, re, sys
from datetime import datetime
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')
D3 = 'E:/ah/wtevents-build/data/m3'
wb = json.load(open(f'{D3}/wb_items.json', encoding='utf-8'))

# ---- 1) 折价商品运行段:同商品连续折价快照聚成一段 ----
runs = defaultdict(list)  # (cat, title) -> [(date, old, new)]
for key, v in wb.items():
    date = key.split('_')[-1][:8]
    d = f'{date[:4]}-{date[4:6]}-{date[6:]}'
    for i in v['items']:
        if i['old'] and i['new'] and i['new'] < i['old'] and i['old'] < 5000:
            runs[(v['cat'], i['title'])].append((d, i['old'], i['new']))
segs = []
for (cat, title), lst in runs.items():
    lst.sort()
    # 聚段:相邻快照间隔 ≤45 天算同一段
    cur = [lst[0]]
    for x in lst[1:]:
        if (datetime.strptime(x[0], '%Y-%m-%d') - datetime.strptime(cur[-1][0], '%Y-%m-%d')).days <= 45:
            cur.append(x)
        else:
            segs.append({'cat': cat, 'title': title, 'start': cur[0][0], 'end': cur[-1][0],
                         'old': max(c[1] for c in cur), 'new': min(c[2] for c in cur), 'n': len(cur)})
            cur = [x]
    segs.append({'cat': cat, 'title': title, 'start': cur[0][0], 'end': cur[-1][0],
                 'old': max(c[1] for c in cur), 'new': min(c[2] for c in cur), 'n': len(cur)})
segs.sort(key=lambda s: s['start'])
print('折价运行段:', len(segs), '段(商品×时段)')

TARGET = {'WarThunderPacks': '礼包', 'SpecOffers': '捆绑包', 'GoldenEagles': '金鹰', 'PremiumAccount': '高级账户'}

# ---- 2) 幂等清理:去掉上轮 wayback 增补(discount.note 标记)与 wayback_ 事件 ----
for p in ['E:/ah/wtevents-build/site/data/events.json', 'E:/ah/wtevents-build/data/events_build.json']:
    d = json.load(open(p, encoding='utf-8'))
    for e in d['events']:
        if e.get('discounts'):
            e['discounts'] = [x for x in e['discounts'] if 'Wayback' not in (x.get('note') or '')]
    d['events'] = [e for e in d['events'] if not e['id'].startswith('wayback_')]
    # 挂接或新建
    evs = d['events']
    by_month = defaultdict(list)
    for e in evs:
        if e.get('start'):
            by_month[e['start'][:7]].append(e)
    def toks(s):
        return {w for w in re.findall(r'[a-z\u4e00-\u9fff]{3,}', (s or '').lower())}
    attached = 0
    newevs = []
    for s in segs:
        item_txt = f"{TARGET[s['cat']]} {s['title']} {s['old']:.0f}→{s['new']:.0f}"
        pct = round((1 - s['new'] / s['old']) * 100)
        disc = {'target': TARGET[s['cat']], 'item': item_txt[:70], 'percent': pct,
                'note': f"Wayback 快照 {s['start']}~{s['end']} 共 {s['n']} 次"}
        hit = None
        st = toks(s['title'])
        for e in by_month.get(s['start'][:7], []) + by_month.get(s['end'][:7], []):
            if e['type'] == 'sale' and (toks(e.get('name_en') or '') | toks(e.get('name_zh') or '')) & st:
                hit = e
                break
        if hit is not None and len(hit.get('discounts', [])) < 20:
            hit.setdefault('discounts', []).append(disc)
            attached += 1
        else:
            me = f"wayback_{s['start'][:7].replace('-', '')}"
            for ne in newevs:
                if ne['id'] == me and len(ne['discounts']) < 20:
                    ne['discounts'].append(disc)
                    ne['end'] = max(ne['end'], s['end'])
                    break
            else:
                newevs.append({
                    'id': me, 'type': 'sale', 'name_zh': f"商店促销(Wayback 快照 {s['start'][:7]})",
                    'name_en': f'Store discounts {s["start"][:7]} (Wayback)', 'bp_season': None,
                    'start': s['start'], 'end': s['end'], 'end_precision': 'day', 'end_raw': None,
                    'dm_event': None, 'vehicles': [], 'awards': [], 'discounts': [disc],
                    'deadlines': [], 'sub_events': [], 'tasks': None,
                    'notes': '由 Internet Archive 商店快照自动重建;仅含快照拍到的折价商品',
                    'sources': {'en': [f"https://web.archive.org/web/{s['start'].replace('-', '')}/https://store.gaijin.net/catalog.php?category={s['cat']}"], 'zh': None},
                    'confidence': 0.7,
                })
    d['events'] = sorted(evs + newevs, key=lambda x: (x.get('start') or x.get('end') or '0000'), reverse=True)
    from collections import Counter
    d['counts'] = {'events': len(d['events']), 'by_type': dict(Counter(e['type'] for e in d['events'])),
                   'with_discounts': sum(1 for e in d['events'] if e.get('discounts'))}
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if 'site' in p else None)
    if 'site' in p:
        print(f"Wayback 整合:增补既有 {attached} 条折扣,新建 {len(newevs)} 个快照事件,总事件 {len(d['events'])}")
