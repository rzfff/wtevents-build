#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M3 Wayback 快照解析:三代商店 DOM(2016/2021/2022)→ 每快照商品价格表 → data/m3/wb_items.json"""
import os, re, sys, json, html

sys.stdout.reconfigure(encoding='utf-8')
SNAP = 'E:/ah/wtevents-build/data/wayback/snap'
OUT = 'E:/ah/wtevents-build/data/m3/wb_items.json'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html.unescape(s))).strip()

def num(s):
    m = re.search(r'[\d][\d\s.,]*\d|\d', s.replace('\u00a0', ' '))
    if not m:
        return None
    t = m.group(0).replace(' ', '').replace(',', '')
    try:
        v = float(t.rstrip('.'))
        return v
    except Exception:
        return None

def parse_items(raw):
    """按代际切 item 块,返回 [(title, old, new, default)]"""
    gen = None
    if 'product-widget-description__title' in raw:
        gen = '2022'
        blocks = re.split(r'(?=<div[^>]+class="[^"]*showcase__item)', raw)
        t_re = re.compile(r'class="[^"]*product-widget-description__title[^"]*"[^>]*>(.{2,120}?)<', re.S)
        old_re = re.compile(r'class="[^"]*showcase-item-price__old[^"]*"[^>]*>([^<]{1,30})<')
        new_re = re.compile(r'class="[^"]*showcase-item-price__new[^"]*"[^>]*>([^<]{1,30})<')
        def_re = re.compile(r'class="[^"]*showcase-item-price__default[^"]*"[^>]*>([^<]{1,30})<')
    elif 'showcase-item-description__title' in raw:
        gen = '2021'
        blocks = re.split(r'(?=<div[^>]+class="[^"]*showcase__item)', raw)
        t_re = re.compile(r'class="[^"]*showcase-item-description__title[^"]*"[^>]*>(.{2,120}?)<', re.S)
        old_re = re.compile(r'class="[^"]*showcase-item-price__old[^"]*"[^>]*>([^<]{1,30})<')
        new_re = re.compile(r'class="[^"]*showcase-item-price__new[^"]*"[^>]*>([^<]{1,30})<')
        def_re = re.compile(r'class="[^"]*showcase-item-price__default[^"]*"[^>]*>([^<]{1,30})<')
    elif 'shop__anonce' in raw:
        gen = '2016'
        blocks = re.split(r'(?=<div[^>]+class="[^"]*shop__item)', raw)
        t_re = re.compile(r'class="[^"]*shop__anonce[^"]*"[^>]*>(.{2,120}?)<', re.S)
        old_re = re.compile(r'class="[^"]*shop__price--old[^"]*"[^>]*>([^<]{1,30})<')
        new_re = re.compile(r'class="[^"]*shop__price--new[^"]*"[^>]*>([^<]{1,30})<')
        def_re = re.compile(r'class="[^"]*shop__price["\s][^>]*>([^<]{1,30})<')
    else:
        return None, []
    items = []
    for b in blocks[1:]:
        if len(b) > 200000:
            b = b[:200000]
        mt = t_re.search(b)
        if not mt:
            continue
        title = strip_tags(mt.group(1))[:80]
        def grab(rx):
            m = rx.search(b)
            return num(m.group(1)) if m else None
        old, new, dflt = grab(old_re), grab(new_re), grab(def_re)
        items.append({'title': title, 'old': old, 'new': new, 'default': dflt})
    return gen, items

out = {}
gens = {}
fails = 0
for f in sorted(os.listdir(SNAP)):
    m = re.match(r'(\w+)_(\d{14})\.html', f)
    if not m:
        continue
    cat, ts = m.group(1), m.group(2)
    cat = {'warthunderpacks': 'WarThunderPacks', 'WarThunderpacks': 'WarThunderPacks'}.get(cat, cat)
    try:
        raw = open(os.path.join(SNAP, f), encoding='utf-8', errors='ignore').read()
        gen, items = parse_items(raw)
        if gen is None:
            fails += 1
            continue
        gens[gen] = gens.get(gen, 0) + 1
        if items:
            out[f'{cat}_{ts}'] = {'cat': cat, 'gen': gen, 'items': items}
    except Exception as e:
        fails += 1
        print('[warn]', f, e)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
snaps = len(out)
total_items = sum(len(v['items']) for v in out.values())
disc = sum(1 for v in out.values() for i in v['items'] if i['old'] and i['new'] and i['new'] < i['old'])
print(f'快照解析 {snaps} 个(代际 {gens}),商品行 {total_items},折价行 {disc},无法解析 {fails}')
