#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML -> 干净正文文本(供 AI 批量抽取)。去 script/style/nav/footer,保留正文与图片题注。"""
import os, re, sys, html as H

sys.stdout.reconfigure(encoding='utf-8')
SRC = sys.argv[1] if len(sys.argv) > 1 else 'E:/ah/wtevents-build/data/articles'
DST = sys.argv[2] if len(sys.argv) > 2 else 'E:/ah/wtevents-build/data/text'

def conv(p):
    s = open(p, encoding='utf-8', errors='ignore').read()
    s = re.sub(r'<script\b.*?</script>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<style\b.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<(nav|footer|header)\b.*?</\1>', ' ', s, flags=re.S | re.I)
    # 评论区/read-more 截断(研究结论:混入他文日期)
    s = re.split(r'class="[^"]*(comments|read-more|widget__comments)', s)[0]
    # 题注与结构行保留为文本行
    s = re.sub(r'<(h[1-6]|figcaption|li|p|div|tr)\b', '\n<', s, flags=re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = H.unescape(s)
    s = re.sub(r'[ \t\u00a0]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n', s)
    lines = [l.strip() for l in s.split('\n')]
    lines = [l for l in lines if l and not re.match(r'^[\s|—•·,.-]+$', l)]
    txt = '\n'.join(lines)
    # 截掉站尾杂讯
    for marker in ('Comments\n', 'Read more\n', 'DISCUSSION'):
        i = txt.find(marker)
        if 0 < i < len(txt) - 5:
            txt = txt[:i]
    return txt.strip()

os.makedirs(DST, exist_ok=True)
n = 0
for f in os.listdir(SRC):
    if not f.endswith('.html'):
        continue
    t = conv(os.path.join(SRC, f))
    if len(t) > 200:
        open(os.path.join(DST, f[:-5] + '.txt'), 'w', encoding='utf-8').write(t)
        n += 1
print('converted', n)
