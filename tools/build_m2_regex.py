#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M2 正则预抽层:对 data/articles2/*.html 直接抽 pubdate 无关的机械字段(日期句/价格对/折扣%/金鹰价/题注),
产出 data/m2/hints.json 供 AI 批次加速与校验。"""
import os, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
SRC = 'E:/ah/wtevents-build/data/articles2'
OUT = 'E:/ah/wtevents-build/data/m2/hints.json'

MON = {m: i + 1 for i, m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'])}

def ordnum(s):
    return int(re.sub(r'\D', '', s) or 0)

def en_dates(txt):
    """返回 [(s_raw, e_raw)] 英文区间句"""
    out = []
    pats = [
        r'From ([A-Z][a-z]+) (\d{1,2}\w{0,2}) \((\d\d:\d\d) GMT\) until ([A-Z][a-z]+) (\d{1,2}\w{0,2}) \((\d\d:\d\d) GMT\)',
        r'from ([A-Z][a-z]+) (\d{1,2}\w{0,2}) to ([A-Z][a-z]+) (\d{1,2}\w{0,2})',
        r'Beginning on: ([A-Z][a-z]+) (\d{1,2}\w{0,2})(?:,| \()?(\d\d:\d\d)? ?GMT\)?',
        r'Ending on: ([A-Z][a-z]+) (\d{1,2}\w{0,2})(?:,| \()?(\d\d:\d\d)? ?GMT\)?',
        r'until ([A-Z][a-z]+) (\d{1,2}\w{0,2})(?: \((\d\d:\d\d) GMT\))?',
    ]
    for p in pats:
        for m in re.finditer(p, txt):
            out.append(m.group(0)[:140])
    return out

def zh_dates(txt):
    out = []
    for m in re.finditer(r'(\d{1,2})月(\d{1,2})日 ?(\d\d:\d\d)?至(\d{1,2})月(\d{1,2})日 ?(\d\d:\d\d)?', txt):
        out.append(m.group(0)[:100])
    for m in re.finditer(r'(\d{4})年(\d{1,2})月(\d{1,2})日[至—-]{1,3}(\d{4})?年?(\d{1,2})月(\d{1,2})日', txt):
        out.append(m.group(0)[:100])
    return out

hints = {}
n = 0
for f in os.listdir(SRC):
    if not f.endswith('.html'):
        continue
    raw = open(os.path.join(SRC, f), encoding='utf-8', errors='ignore').read()
    txt = re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)\b.*?</\1>', ' ', raw, flags=re.S | re.I))
    h = {'size': len(raw)}
    d = en_dates(txt)
    if d:
        h['en_date_sents'] = d[:6]
    zd = zh_dates(txt)
    if zd:
        h['zh_date_sents'] = zd[:6]
    # 价格对(HTML 结构层)
    pairs = re.findall(r'class="[^"]*t-strikethrough-text[^"]*"[^>]*>\s*([\d., ]+)\s*<.*?class="[^"]*t-forex-text[^"]*"[^>]*>\s*([\d., ]+)\s*<', raw, flags=re.S)
    if pairs:
        h['price_pairs'] = [(a.strip(), b.strip()) for a, b in pairs[:14]]
    # 折扣 %
    pcts = re.findall(r'(?<!\d)(\d{1,2})%(?:\s*(?:discount|off))?', txt)
    pcts += re.findall(r'-(\d{1,2})%(?!\d)', txt)
    if pcts:
        from collections import Counter
        h['percents'] = dict(Counter(pcts))
    # 金鹰价
    ge = re.findall(r'(\d[\d,]{2,9})\s*(?:Golden Eagles|金鹰)', txt)
    if ge:
        h['ge_prices'] = sorted({g.replace(',', '') for g in ge})[:12]
    # 题注车名
    caps = re.findall(r'class="[^"]*e-figure__caption[^"]*"[^>]*>(.{2,80})<', raw)
    if caps:
        h['captions'] = [re.sub(r'<[^>]+>', '', c).strip() for c in caps[:16]]
    if len(h) > 1:
        hints[f[:-5]] = h
    n += 1
json.dump(hints, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('articles scanned', n, 'with hints', len(hints))
