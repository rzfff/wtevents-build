#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M2 候选清单阶段A:从 sitemap 缓存筛事件相关文章(EN 前缀精确 + ZH 拼音前缀 + 无 slug 老格式待定)
排除 M1 已抓取的 125 篇(已在 /tmp/we/art 缓存与 extract 结果中)。"""
import json, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
DATA = 'E:/ah/wtevents-build/data'
os.makedirs(f'{DATA}/m2', exist_ok=True)

def sm(p):
    txt = open(p, encoding='utf-8', errors='ignore').read()
    return [(m.group(1).strip(), m.group(2)[:10]) for m in
            re.finditer(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', txt)]

en = sm('E:/ah/tmp-wt/sm-en-full.xml')
zh = sm('E:/ah/tmp-wt/sm-zh-full.xml')

done_ids = {q['en_id'] for q in json.load(open(f'{DATA}/fetch_queue.json', encoding='utf-8')) if q['en_id']}
done_zh = set()
for q in json.load(open(f'{DATA}/fetch_queue.json', encoding='utf-8')):
    for u in q['zh']:
        m = re.search(r'/news/(\d+)', u)
        if m:
            done_zh.add(int(m.group(1)))
print('M1 已处理: en', len(done_ids), 'zh', len(done_zh))

EN_PREFIX = ('shop-', 'event-', 'warbonds-', 'special-', 'market-', 'battle-pass-',
             'giveaway-', 'marathon-', 'glorious5-', 'vday-', 'christmas-', 'sale-')
ZH_PREFIX = ('shi-jian-', 'shang-dian-', 'te-shu-', 'shi-chang-', 'ren-wu-jiang-quan-')

def nid(u):
    m = re.search(r'/news/(\d+)', u)
    return int(m.group(1)) if m else None

en_new, en_old = [], []
for u, d in en:
    i = nid(u)
    if not i or i in done_ids:
        continue
    m = re.search(r'/news/\d+-([a-z0-9-]+?)(?:-en)?/?$', u)
    slug = m.group(1) if m else ''
    if slug.startswith(EN_PREFIX):
        en_new.append((i, u, d))
    elif not slug:  # 无 slug 老格式
        en_old.append((i, u, d))

zh_new, zh_old = [], []
for u, d in zh:
    i = nid(u)
    if not i or i in done_zh:
        continue
    m = re.search(r'/news/\d+-([a-z0-9-]+?)-zh/?$', u)
    slug = m.group(1) if m else ''
    if slug.startswith(ZH_PREFIX):
        zh_new.append((i, u, d))
    elif '/zh/news/' in u and not slug:
        zh_old.append((i, u, d))

en_new.sort(); zh_new.sort()
print(f'EN 前缀精确: {len(en_new)}(去重后) | EN 无slug待筛: {len(en_old)} | ZH 拼音精确: {len(zh_new)} | ZH 无slug待筛: {len(zh_old)}')

with open(f'{DATA}/m2/en_new.tsv', 'w', encoding='utf-8', newline='\n') as f:
    for i, u, d in en_new:
        f.write(f'{i}\t{u}\t{d}\n')
with open(f'{DATA}/m2/zh_new.tsv', 'w', encoding='utf-8', newline='\n') as f:
    for i, u, d in zh_new:
        f.write(f'{i}\t{u}\t{d}\n')
json.dump([{'id': i, 'url': u, 'd': d} for i, u, d in en_old], open(f'{DATA}/m2/en_old_pool.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump([{'id': i, 'url': u, 'd': d} for i, u, d in zh_old], open(f'{DATA}/m2/zh_old_pool.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('M2 阶段A 产物落 data/m2/')
