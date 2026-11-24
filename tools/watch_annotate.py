#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""哨兵后处理器:读最新基线 vs events.json,标注哪些新文章真正需要处理。
由 watch.sh 在检测步骤之后调用,输出追加到 watch.log。"""
import json, os, re, sys, hashlib
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
# v3.3(2026-11-23): annotate 块内容 md5 门——与上次相同时整块跳过,防同一积压逐日刷屏淹信号(watch.log 曾 808 行/58 块重复)
_pending = []
for lang in ('en', 'zh'):
    p = os.path.join(STATE, f'list_{lang}.txt')
    if not os.path.exists(p):
        continue
    urls = [l.strip() for l in open(p) if l.strip()]
    # v3.2(2026-10-29): 去重 #comments 变体 + 全量列出不再截断(与 watch.sh v3.1 口径对齐)
    seen = set()
    to_process = []
    for u in urls:
        aid = re.search(r'/(\d+)', u)
        if aid and aid.group(1) not in collected:
            base = u.split('#')[0]
            if base not in seen:
                seen.add(base)
                to_process.append(u)
    _pending.append((lang, to_process))

_h = hashlib.md5(json.dumps([(l, t) for l, t in _pending]).encode()).hexdigest()
_hp = os.path.join(STATE, 'annotate.md5')
_prev = open(_hp).read().strip() if os.path.exists(_hp) else None
if _prev == _h:
    sys.exit(0)  # 与上次积压完全相同:静默退出
open(_hp, 'w').write(_h)
for lang, to_process in _pending:
    if to_process:
        say(f'[{lang}] [ANNOTATE] 基线上有 {len(to_process)} 篇不在 events.json 中,需处理:')
        for u in to_process:
            say(f'  → {u}')
