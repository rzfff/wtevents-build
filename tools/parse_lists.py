#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M2 阶段B:解析列表页 → title_map(news_id → title/date/lang);筛无 slug 老池;产出最终抓取队列。"""
import os, re, sys, json
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
DATA = 'E:/ah/wtevents-build/data'
L = f'{DATA}/lists'

MON = {m: i + 1 for i, m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'])}
tmap = {}
for f in os.listdir(L):
    lang = 'en' if f.startswith('en_') else 'zh'
    raw = open(os.path.join(L, f), encoding='utf-8', errors='ignore').read()
    # 卡片块:定位每个链接+紧随标题/日期
    for m in re.finditer(r'href="(/(?:en|zh)/news/([0-9]+)[^"]*)"', raw):
        url, nid = m.group(1), m.group(2)
        seg = raw[m.end():m.end() + 2500]
        t = re.search(r'class="[^"]*widget__title[^"]*"[^>]*>([^<]+)<', seg)
        dt = re.search(r'(\d{1,2}) ([A-Z][a-z]+) (\d{4})', seg) or re.search(r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日', seg)
        date = None
        if dt:
            try:
                if lang == 'en':
                    date = f'{dt.group(3)}-{MON[dt.group(2).lower()]:02d}-{int(dt.group(1)):02d}'
                else:
                    date = f'{dt.group(1)}-{int(dt.group(2)):02d}-{int(dt.group(3)):02d}'
            except Exception:
                pass
        key = f'{lang}_{nid}'
        if key not in tmap:
            tmap[key] = {'title': (t.group(1).strip() if t else ''), 'date': date, 'lang': lang}
print('title_map 条目:', len(tmap), '(en', sum(1 for v in tmap.values() if v['lang'] == 'en'), '/ zh', sum(1 for v in tmap.values() if v['lang'] == 'zh'), ')')
json.dump(tmap, open(f'{DATA}/m2/title_map.json', 'w', encoding='utf-8'), ensure_ascii=False)

# ---------- 筛无 slug 老池 ----------
KW = re.compile(r'sale|discount|\d+\s*%|offer|marathon|event|quest|festiv|annivers|birthday|holiday|christmas|winter|summer|april|fool|craft|celebrat|operation|store|golden eagle|premium|deal|giveaway|win a |get a |for free|打折|折扣|折|活动|事件|马拉松|节日|周年|庆典|愚人|任务|奖券|市场|商店|兑换|免费|领取', re.I)

def filt(pool_file, out_file):
    pool = json.load(open(pool_file, encoding='utf-8'))
    keep = [x for x in pool if KW.search(tmap.get(str(x['id']), {}).get('title') or '')]
    with open(out_file, 'w', encoding='utf-8', newline='\n') as f:
        for x in keep:
            f.write(f"{x['id']}\t{x['url']}\t{x['d']}\n")
    print(os.path.basename(pool_file), '池', len(pool), '→ 命中', len(keep))
    return keep

en_old = filt(f'{DATA}/m2/en_old_pool.json', f'{DATA}/m2/en_old_kept.tsv')
zh_old = filt(f'{DATA}/m2/zh_old_pool.json', f'{DATA}/m2/zh_old_kept.tsv')

# ---------- 合成最终抓取队列(排除 M1 已有) ----------
q1 = json.load(open(f'{DATA}/fetch_queue.json', encoding='utf-8'))
done_en = {q['en_id'] for q in q1 if q['en_id']}
done_zh = set()
for q in q1:
    for u in q['zh']:
        m = re.search(r'/news/(\d+)', u)
        if m:
            done_zh.add(int(m.group(1)))

enq = [(int(l.split('\t')[0]), l.split('\t')[1].strip()) for l in open(f'{DATA}/m2/en_new.tsv', encoding='utf-8').read().splitlines() if l.strip()]
enq += [(int(l.split('\t')[0]), l.split('\t')[1].strip()) for l in open(f'{DATA}/m2/en_old_kept.tsv', encoding='utf-8').read().splitlines() if l.strip()]
zhq = [(int(l.split('\t')[0]), l.split('\t')[1].strip()) for l in open(f'{DATA}/m2/zh_new.tsv', encoding='utf-8').read().splitlines() if l.strip()]
zhq += [(int(l.split('\t')[0]), l.split('\t')[1].strip()) for l in open(f'{DATA}/m2/zh_old_kept.tsv', encoding='utf-8').read().splitlines() if l.strip()]
seen = set()
with open(f'{DATA}/m2/fetch2_en.tsv', 'w', encoding='utf-8', newline='\n') as fe, open(f'{DATA}/m2/fetch2_zh.txt', 'w', encoding='utf-8', newline='\n') as fz:
    for i, u in enq:
        if i in done_en or i in seen:
            continue
        seen.add(i)
        fe.write(f'{i}\t{u}\n')
    for i, u in zhq:
        if i in done_zh or (i, 'zh') in seen:
            continue
        seen.add((i, 'zh'))
        fz.write(u + '\n')
print('最终队列: EN', sum(1 for _ in open(f'{DATA}/m2/fetch2_en.tsv', encoding='utf-8')), '/ ZH', sum(1 for _ in open(f'{DATA}/m2/fetch2_zh.txt', encoding='utf-8')))
