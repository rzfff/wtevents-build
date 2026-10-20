#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""时区校正:zh 源「北京时间」被原样贴 Z 的事件按 end_raw 原文 -8h(end_raw 是唯一裁判)"""
import json, re, sys
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

def shift(iso, hours=8):
    m = re.match(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}):00Z', iso)
    if not m:
        return iso, False
    dt = datetime.strptime(m.group(1) + ' ' + m.group(2), '%Y-%m-%d %H:%M') - timedelta(hours=hours)
    return dt.strftime('%Y-%m-%dT%H:%M:00Z'), True

# 人工核对过的修正表(end_raw 原文佐证;新增条目按同规则登记在此)
KNOWN = {
    'sale_202312_b': ('2023-12-26T12:00:00Z', '2024-01-02T12:00:00Z'),
    'anniversary_202311': ('2023-11-29T11:00:00Z', '2023-12-04T07:00:00Z'),
}

for p in ['E:/ah/wtevents-build/site/data/events.json', 'E:/ah/wtevents-build/data/events_build.json']:
    d = json.load(open(p, encoding='utf-8'))
    n = 0
    for e in d['events']:
        if e['id'] in KNOWN and '北京' in (e.get('end_raw') or ''):
            e['start'], e['end'] = KNOWN[e['id']]
            n += 1
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if 'site' in p else None)
    print(('site' if 'site' in p else 'build'), 'tz 修正', n, '条')
