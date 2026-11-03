#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""增量九轮(2026-11-03):计数不变 946,纯源链修复批。
根因:2026-11-01 批 src() 被传裸字符串而非列表 → '10269' 逐字符炸成 news/1,0,2,6,9 垃圾 URL,
      完整 URL 从未落库(哨兵 ANNOTATE 积压 11EN+10ZH 的真凶)。
本批:①全库清除 /news/1~2位数 垃圾源;②9 事件按列表补挂正确双语源;③周年伞挂蜗牛玩偶联名文(10266/2826)。
铁律再录:src() 的 en/zh 参数必须传列表,传字符串=逐字符爆炸(2026-11-03 实锤)。
"""
import json, io, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
P = r'E:\ah\wtevents-build\site\data\events.json'
d = json.load(io.open(P, encoding='utf-8'))
ev = d['events']
by = {e['id']: e for e in ev}

def src(e, en=None, zh=None):
    """en/zh 必须传列表;逐条校验 id 形态(≥3 位数字)防字符爆炸复发。"""
    s = e.setdefault('sources', {'en': [], 'zh': []})
    if s is None:
        s = e['sources'] = {'en': [], 'zh': []}
    for k, ids in (('en', en), ('zh', zh)):
        for i in (ids or []):
            assert re.fullmatch(r'\d{3,}', i), f'src id 形态可疑: {i!r}(必须列表且完整数字 id)'
            u = f'https://warthunder.com/{k}/news/{i}'
            if u not in s.setdefault(k, []):
                s[k].append(u)

# ---------- A. 清除垃圾源(逐字符爆炸残留:/news/1~2 位数) ----------
# ⚠ 只打 11-01 批污染的 10 个事件——2011-2013 老文章 id 本就是 1~2 位数(news/12·72·90 为真源,勿全库正则误伤)
POLLUTED = {'special_202610_d', 'sale_202610_p', 'sale_202610_k', 'sale_202610_i',
            'sale_202610_j', 'sale_202610_h', 'sale_202610_g', 'festive_202610_b',
            'special_202610_c', 'special_202610_e'}
junk_re = re.compile(r'/news/\d{1,2}$')
removed = 0
for e in ev:
    if e['id'] not in POLLUTED:
        continue
    s = e.get('sources')
    if not isinstance(s, dict):
        continue
    for lang in ('en', 'zh'):
        lst = s.get(lang)
        if isinstance(lst, list):
            keep = [u for u in lst if not junk_re.search(u)]
            removed += len(lst) - len(keep)
            s[lang] = keep
print('垃圾源清除(仅 10 个污染事件):', removed)

# ---------- B. 9 事件补挂正确源(2026-11-01 批的未遂意图) ----------
src(by['sale_202610_g'], ['10269'], ['2828'])   # 特拉法尔加海战纪念
src(by['sale_202610_h'], ['10270'], ['2830'])   # 加拿大涅厄泊日 HMCS Haida
src(by['sale_202610_i'], ['10273'], ['2832'])   # UH-1C XM-30 首飞返售
src(by['sale_202610_j'], ['10274'], ['2833'])   # 虹鱼(黄貂鱼)II 预购
src(by['sale_202610_k'], ['10278'], ['2837'])   # J35A 龙式回归
src(by['festive_202610_b'], ['10286'])          # 万圣节亡命竞速(zh 孪生未确证,勿猜)
src(by['special_202610_c'], ['10283'])          # 核冲突全真测试
src(by['special_202610_e'], ['10275'])          # WTCS 总决赛 Twitch 掉宝
# special_202610_d(槲寄生)与 sale_202610_p(A-20)的正确源已在库,垃圾源已被 A 段清掉

# ---------- C. 周年伞补挂蜗牛玩偶联名文(伞内 deadline 已记载该周边) ----------
src(by['anniversary_202610'], ['10266'], ['2826'])

# ---------- D. meta ----------
d['generated_at'] = '2026-11-03T00:00:00Z'
d['counts'] = {
    'events': len(ev),
    'by_type': dict(Counter(e.get('type') for e in ev)),
    'with_discounts': sum(1 for e in ev if e.get('discounts')),
}
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', d['counts']['by_type'])
print('SAVED')
