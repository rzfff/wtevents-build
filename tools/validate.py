#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M1 校验:结构断言 + 数据体检"""
import json, os, sys, re

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(f'{ROOT}/site/data/events.json', encoding='utf-8'))
ev = d['events']
err, warn = [], []

ids = [e['id'] for e in ev]
if len(ids) != len(set(ids)):
    err.append('id 重复')
VOCAB = {'sale','marathon','craft','battlepass','festive','anniversary','april','worldwar','special','market','memorial'}
for e in ev:
    if e['type'] not in VOCAB:
        err.append(f"{e['id']} 类型非法 {e['type']}")
    if not e.get('name_en') and not e.get('name_zh'):
        err.append(f"{e['id']} 缺名称")
    if not e.get('start') or not re.match(r'^\d{4}-\d{2}-\d{2}', e['start']):
        err.append(f"{e['id']} start 非法 {e.get('start')}")
    if e.get('end') and e['start'] and e['end'] < e['start'][:10] and not e.get('start_override'):
        # end<start 仅当 start_override 场景才可能合法
        err.append(f"{e['id']} end<start ({e['start']} → {e['end']})")
    if e.get('end') and not re.match(r'^\d{4}-\d{2}-\d{2}', e['end']):
        err.append(f"{e['id']} end 非法 {e['end']}")
    for x in e.get('discounts', []):
        if x.get('percent') is not None and not (0 < x['percent'] < 100):
            err.append(f"{e['id']} 折扣率异常 {x}")

bp = [e for e in ev if e["type"] == "battlepass" and e.get("bp_season")]
if len(bp) != 25:
    err.append(f"战令 {len(bp)} != 25")
if sorted(x['bp_season'] for x in bp) != list(range(1, 26)):
    err.append('战令季号不连续')
# M2: 折扣事件健康度
sales = [e for e in ev if e['type'] == 'sale']
empty_sales = [e['id'] for e in sales if not e.get('discounts')]
if empty_sales:
    warn.append(f'sale 事件无折扣明细 {len(empty_sales)} 条: {empty_sales[:6]}')
for e in ev:
    se, sz = e.get('sources', {}).get('en'), e.get('sources', {}).get('zh')
    if isinstance(se, list) and not se and not sz:
        err.append(f"{e['id']} 无任何来源")
    if isinstance(se, list) and not se and isinstance(sz, list) and sz:
        pass  # 纯 zh 事件合法

years = sorted({(e['start'] or e['end'] or '????')[:4] for e in ev})
no_end = [e['id'] for e in ev if not e.get('end')]
no_zh = sum(1 for e in ev if not e.get('name_zh'))
veh_total = sum(len(e.get('vehicles', [])) for e in ev)
imgs = set(os.listdir('E:/ah/wtapi-build/dist/assets/images')) if os.path.isdir('E:/ah/wtapi-build/dist/assets/images') else set()
miss_img = [v['id'] for e in ev for v in e.get('vehicles', []) if v['id'] + '.png' not in imgs]

print(f"事件 {len(ev)} | 年份 {years[0]}–{years[-1]} | 战令 {len(bp)} | 带载具 {sum(1 for e in ev if e.get('vehicles'))} | 载具总数 {veh_total} | 中文名缺失 {no_zh} | 缺 end {len(no_end)}")
print('缺 end 清单:', no_end[:12], '...' if len(no_end) > 12 else '')
print('载具图缺失:', len(miss_img), miss_img[:8])
print('年份分布:', {y: sum(1 for e in ev if (e.get('start') or '').startswith(y)) for y in years})
if warn:
    print('WARN:', warn)
if err:
    print('ERR:')
    [print(' -', x) for x in err]
    sys.exit(1)
print('VALIDATE PASS')
