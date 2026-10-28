#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""哨兵后处理器:读最新基线 vs events.json,标注哪些新文章真正需要处理。
由 watch.sh 在检测步骤之后调用,输出追加到 watch.log。"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

STATE = '/opt/services/wtevents-ops/watch'
LOG = '/opt/services/wtevents-ops/watch.log'
EVENTS = '/opt/services/wtevents/data/events.json'

def say(msg):
    with open(LOG, 'a') as f:
        f.write(f'{msg}\n')

# 已收录的新闻 ID
d = json.load(open(EVENTS))
collected = set()
for e in d['events']:
    for lang in ('en', 'zh'):
        s = e.get('sources', {}).get(lang, [])
        if isinstance(s, list):
            for u in s:
                if '/news/' in u:
                    aid = u.rstrip('/').split('/')[-1].split('-')[0]
                    collected.add(aid)

# 读当前基线,找不在 events 里的
for lang in ('en', 'zh'):
    p = os.path.join(STATE, f'list_{lang}.txt')
    if not os.path.exists(p):
        continue
    urls = [l.strip() for l in open(p) if l.strip()]
    to_process = []
    for u in urls:
        aid = re.search(r'/(\d+)', u)
        if aid and aid.group(1) not in collected:
            to_process.append(u)
    if to_process:
        say(f'[{lang}] [ANNOTATE] 基线上有 {len(to_process)} 篇不在 events.json 中,需处理:')
        for u in to_process[:5]:
            say(f'  → {u}')
        if len(to_process) > 5:
            say(f'  ... 及另外 {len(to_process)-5} 篇')
