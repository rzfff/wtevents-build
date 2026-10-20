#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合并 skeleton + datamine + 官方中文名 + AI 批量抽取结果 → site/data/events.json"""
import json, os, re, sys, glob
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

def load(p):
    return json.load(open(p, encoding='utf-8'))

skeleton = load(f'{DATA}/skeleton.json')
event_vehicles = load(f'{DATA}/event_vehicles.json')
dm_match = load(f'{DATA}/dm_match.json')
zh_official = load(f'{DATA}/zh_official.json')
queue = load(f'{DATA}/fetch_queue.json')
qmap = {q['key']: q for q in queue}

# AI 抽取结果
ext = {}
for p in sorted(glob.glob(f'{DATA}/extract/batch*.json')):
    try:
        d = load(p)
        for r in d.get('results', []):
            ext[r['key']] = r
    except Exception as e:
        print('[warn] 坏批次文件', p, e)
print('AI 抽取结果:', len(ext), '条')

SEC_TYPE = {'battlepass': 'battlepass', '1april': 'april', 'world_war': 'worldwar'}

events = []
stats = {'no_end': 0, 'no_zh': 0, 'no_dm': 0}
for s in skeleton:
    r = ext.get(s['key']) or {}
    # 类型:agent 判定优先(regular),其余按 section
    t = r.get('type') or SEC_TYPE.get(s['section'])
    if not t:
        t = 'anniversary' if re.search(r'anniversar|\d+y[ea]rs|reach(es)? its|birthday', s['title'], re.I) else 'special'
    if s['section'] == 'battlepass':
        t = 'battlepass'
    dm = dm_match.get(s['key'])
    veh = event_vehicles.get(dm, []) if dm else []
    # 中文名:官方(menu.csv) > zh 新闻(agent 确认)
    off = zh_official.get(dm or '', {})
    name_zh = off.get('name_zh') or r.get('name_zh') or None
    if name_zh:
        name_zh = name_zh.strip().replace('​', '')
        name_zh = re.sub(r'["”]?\s*(涂鸦|贴花|涂装|喷漆|装饰)+\s*["”]?$', '', name_zh)
        name_zh = re.sub(r'^["“]\s*|\s*["”]$', '', name_zh).strip()
    if s['section'] == 'battlepass' and not name_zh:
        m = re.search(r'"([^"]+)"', s['title'])
        name_zh = f'战斗通行证 第 {s["bp_season"]} 季'
    src = {}
    if s.get('news_url'):
        src['en'] = s['news_url']
    if r.get('zh_id'):
        for u in qmap.get(s['key'], {}).get('zh', []):
            if f"/{r['zh_id']}" in u:
                src['zh'] = u
                break
    if s.get('wiki_vehicles'):
        src['wiki'] = 'https://wiki.warthunder.com' + s['wiki_vehicles']
    start = r.get('start_override') or s['start']
    end = r.get('end') or None
    if not end:
        stats['no_end'] += 1
    if not name_zh:
        stats['no_zh'] += 1
    if not dm:
        stats['no_dm'] += 1
    conf = 0.35 + (0.3 if end else 0) + (0.15 if name_zh else 0) + (0.2 if dm else 0)
    conf = min(1.0, max(conf, r.get('confidence') or 0))
    e = {
        'id': s['key'],
        'type': t,
        'name_zh': name_zh,
        'name_en': s['title'],
        'bp_season': s.get('bp_season'),
        'start': start,
        'end': end,
        'end_precision': r.get('end_precision'),
        'end_raw': r.get('end_raw'),
        'dm_event': dm,
        'vehicles': veh,
        'awards': s.get('awards') or [],
        'discounts': r.get('discounts') or [],
        'deadlines': r.get('deadlines') or [],
        'sub_events': r.get('sub_events') or [],
        'tasks': r.get('tasks'),
        'notes': r.get('notes'),
        'sources': src,
        'confidence': round(conf, 2),
    }
    events.append(e)

events.sort(key=lambda x: (x['start'] or '0000'), reverse=True)
from collections import Counter
out = {
    'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'build': 'm1',
    'counts': {
        'events': len(events),
        'by_type': dict(Counter(e['type'] for e in events)),
        'with_vehicles': sum(1 for e in events if e['vehicles']),
        'with_zh_name': sum(1 for e in events if e['name_zh']),
        'with_end': sum(1 for e in events if e['end']),
    },
    'events': events,
}
os.makedirs(f'{ROOT}/site/data', exist_ok=True)
json.dump(out, open(f'{ROOT}/site/data/events.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(out, open(f'{DATA}/events_build.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
size = os.path.getsize(f'{ROOT}/site/data/events.json')
print(f"events.json: {len(events)} 条, {size/1024:.0f} KB")
print('counts:', json.dumps(out['counts'], ensure_ascii=False))
print('缺 end:', stats['no_end'], '缺中文名:', stats['no_zh'], '无 datamine 车辆:', stats['no_dm'])
