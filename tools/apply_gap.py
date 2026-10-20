#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M3 补漏应用:extract_gap.json 17 篇 → 并入现有事件(窗口+token/数字重合)或新建;回填 M1 空字段"""
import json, re, sys
from datetime import datetime
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
D = 'E:/ah/wtevents-build/data'

STOP = {'the','and','for','with','from','new','get','your','its','are','was','this','that','you'}

def toks(s):
    return {w for w in re.findall(r'[a-z\u4e00-\u9fff]{3,}', (s or '').lower())} - STOP

def nums(s):
    return set(re.findall(r'\d[\d.,]{2,}\d|\d{3,}', s or ''))

def d(s):
    try:
        return datetime.strptime((s or '')[:10], '%Y-%m-%d').date()
    except Exception:
        return None

import sys as _sys
arts = json.load(open(_sys.argv[1] if len(_sys.argv)>1 else f'{D}/m3/extract_gap.json', encoding='utf-8'))['results']
tm = json.load(open(f'{D}/m2/title_map.json', encoding='utf-8'))
for p in ['E:/ah/wtevents-build/site/data/events.json', 'E:/ah/wtevents-build/data/events_build.json']:
    ev = json.load(open(p, encoding='utf-8'))['events']
    used = Counter()
    merged = created = filled = 0
    for a in sorted(arts, key=lambda x: x.get('start') or '9999'):
        at = toks(a.get('name_en') or '') | toks(a.get('title') or '')
        an = nums(json.dumps(a.get('discounts') or []) + (a.get('tasks') or '') + (a.get('name_en') or ''))
        ad = d(a.get('start'))
        hit = None
        for e in ev:
            et = toks(e.get('name_en') or '') | toks(e.get('name_zh') or '')
            en_ = nums(json.dumps(e.get('discounts') or []) + (e.get('tasks') or '') + (e.get('name_en') or ''))
            ed = d(e.get('start'))
            near = ad and ed and abs((ad - ed).days) <= 10
            if near and ((at & et) or (an & en_)):
                hit = e
                break
        aid = a['aid']
        url = f"https://warthunder.com/{a.get('lang','en')}/news/{aid}"
        if hit is not None:
            # 折叠:补折扣/截止/子活动/来源;回填缺失 end/tasks
            for x in a.get('discounts') or []:
                if not any((x.get('item') or '')[:25] == (y.get('item') or '')[:25] for y in hit.get('discounts', [])):
                    hit.setdefault('discounts', []).append(x)
            hit.setdefault('deadlines', []).extend(a.get('deadlines') or [])
            hit.setdefault('sub_events', []).extend(a.get('sub_events') or [])
            if not hit.get('end') and a.get('end'):
                hit['end'], hit['end_precision'], hit['end_raw'] = a['end'], a.get('end_precision'), a.get('end_raw')
                filled += 1
            if not hit.get('tasks') and a.get('tasks'):
                hit['tasks'] = a['tasks']
            en_s = hit['sources'].setdefault('en', [])
            if en_s is None:
                hit['sources']['en'] = en_s = []
            if isinstance(en_s, str):
                hit['sources']['en'] = en_s = [en_s]
            if url not in en_s:
                en_s.insert(0, url)
            hit['confidence'] = min(1.0, (hit.get('confidence') or 0.5) + 0.1)
            merged += 1
        else:
            ym = (a.get('start') or datetime.utcnow().strftime('%Y%m'))[:7].replace('-', '')
            base = f"{a.get('type') or 'special'}_{ym}"
            used[base] += 1
            eid = base if used[base] == 1 else f"{base}_{chr(96 + used[base])}"
            while any(e['id'] == eid for e in ev):
                eid += 'x'
            ev.append({
                'id': eid, 'type': a.get('type') or 'special',
                'name_zh': None, 'name_en': (a.get('name_en') or a.get('title') or '?')[:80],
                'bp_season': None,
                'start': a.get('start') or a.get('end') or ((tm.get('en_%s'%a['aid']) or {}).get('date')), 'end': a.get('end'),
                'end_precision': a.get('end_precision'), 'end_raw': a.get('end_raw'),
                'dm_event': None, 'vehicles': [],
                'awards': a.get('rewards_text') or [],
                'discounts': a.get('discounts') or [], 'deadlines': a.get('deadlines') or [],
                'sub_events': a.get('sub_events') or [], 'tasks': a.get('tasks'),
                'notes': a.get('notes'),
                'sources': {'en': [url], 'zh': None},
                'confidence': a.get('confidence') or 0.7,
            })
            created += 1
    ev.sort(key=lambda x: (x.get('start') or x.get('end') or '0000'), reverse=True)
    dd = json.load(open(p, encoding='utf-8'))
    dd['events'] = ev
    dd['counts'] = {'events': len(ev), 'by_type': dict(Counter(e['type'] for e in ev)),
                    'with_discounts': sum(1 for e in ev if e.get('discounts'))}
    json.dump(dd, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if 'site' in p else None)
    print(('site' if 'site' in p else 'build'), f'补漏:折叠 {merged} 新建 {created} 回填end {filled} → 总 {len(ev)}')
