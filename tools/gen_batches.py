#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M2 批次生成:实际有文本的文章 → fetch2_all.json + 每批 hints 切片 + 批次范围清单"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
DATA = 'E:/ah/wtevents-build/data'
TXT = f'{DATA}/text2'
hints = json.load(open(f'{DATA}/m2/hints.json', encoding='utf-8'))
tmap = json.load(open(f'{DATA}/m2/title_map.json', encoding='utf-8'))

def load_tsv(p):
    out = {}
    for l in open(p, encoding='utf-8'):
        p_ = l.rstrip('\n').split('\t')
        if len(p_) >= 2:
            out[int(p_[0])] = p_[1]
    return out

enq = load_tsv(f'{DATA}/m2/fetch2_en.tsv')
all_arts = []
for f in sorted(os.listdir(TXT)):
    m = re.match(r'(en|zh)_(\d+)\.txt', f)
    if not m:
        continue
    lang, aid = m.group(1), int(m.group(2))
    t = tmap.get(f'{lang}_{aid}') or tmap.get(str(aid), {})
    url = enq.get(aid) if lang == 'en' else f"https://warthunder.com/zh/news/{aid}"
    all_arts.append({'aid': aid, 'lang': lang, 'title': t.get('title') or '', 'date': t.get('date'), 'url': url, 'txt': f'text2/{f}'})
all_arts.sort(key=lambda a: (a['lang'] != 'en', a['aid']))
json.dump(all_arts, open(f'{DATA}/m2/fetch2_all.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('可用文章:', len(all_arts), '(en', sum(1 for a in all_arts if a['lang'] == 'en'), '/ zh', sum(1 for a in all_arts if a['lang'] == 'zh'), ')')

B = 30
os.makedirs(f'{DATA}/m2/batch_hints', exist_ok=True)
nb = (len(all_arts) + B - 1) // B
for i in range(nb):
    sl = all_arts[i * B:(i + 1) * B]
    hh = {f"{a['lang']}_{a['aid']}": hints.get(f"{a['lang']}_{a['aid']}", {}) for a in sl}
    json.dump({'articles': sl, 'hints': hh}, open(f"{DATA}/m2/batch_hints/b{i:02d}.json", 'w', encoding='utf-8'), ensure_ascii=False)
print('批次数:', nb)
for i in range(nb):
    a0, a1 = i * B, min((i + 1) * B, len(all_arts))
    print(f'B{i:02d} [{a0}:{a1}]')
