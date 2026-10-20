#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M2 合并去重层 v2:文章抽取 → 分组 → 折叠进 M1 126 条(新闻ID直配+窗口/标题并入)→ 新事件 → events.json"""
import json, os, re, sys, glob
from datetime import datetime, timezone
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
DATA = 'E:/ah/wtevents-build/data'
SITE = 'E:/ah/wtevents-build/site'

def load(p):
    return json.load(open(p, encoding='utf-8'))

def date_today():
    return datetime.now(timezone.utc).date()

cur = load(f'{DATA}/m1_base.json')  # 固定 M1 基线(勿再读 site 产物,防污染)
m1_events = {e['id']: dict(e) for e in cur['events']}
arts = []
for p in sorted(glob.glob(f'{DATA}/m2/extract/*.json')):
    try:
        d = load(p)
        arts += [a for a in d.get('results', []) if a.get('is_event')]
    except Exception as e:
        print('[warn] bad extract', p, e)
print('文章级事件候选:', len(arts), '其中 zh', sum(1 for a in arts if a.get('lang') == 'zh'))

titles = load(f'{DATA}/m2/title_map.json')
def tget(a):
    """M3: title_map 按 lang_id 键(en_xxx/zh_xxx);兼容旧数字键。"""
    aid = str(a.get('aid') or '')
    return titles.get(f"{a.get('lang')}_{aid}") or titles.get(aid) or {}
def a_title(a):
    return a.get('title') or tget(a).get('title') or a.get('name_en') or ''

def toks(s):
    return {w for w in re.findall(r'[a-z\u4e00-\u9fff]{3,}', (s or '').lower())}

def jac(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / max(1, len(A | B))

def contain(a, b):
    A, B = toks(a), toks(b)
    return (A and A <= B) or (B and B <= A)

def d(s):
    try:
        return datetime.strptime((s or '')[:10], '%Y-%m-%d').date()
    except Exception:
        return None

def win(a):
    s = d(a.get('start')) or d(tget(a).get('date') or '')
    e = d(a.get('end')) or s
    return (s, e)

def nwin(w):
    s, e = w
    if s and not e:
        e = s
    if e and not s:
        s = e
    return (s, e)

def overlaps(w1, w2):
    w1, w2 = nwin(w1), nwin(w2)
    if not w1[0] or not w2[0]:
        return False
    return w1[0] <= w2[1] and w2[0] <= w1[1]

def near(w1, w2, days):
    w1, w2 = nwin(w1), nwin(w2)
    for x in (w1[0], w1[1]):
        for y in (w2[0], w2[1]):
            if x and y and abs((x - y).days) <= days:
                return True
    return False

# ---------- 0) M1 事件的新闻 ID 索引 ----------
m1_by_nid = {}
for e in m1_events.values():
    en = e.get('sources', {}).get('en')
    if isinstance(en, str):
        m = re.search(r'/news/(\d+)', en)
        if m:
            m1_by_nid[int(m.group(1))] = e
    elif isinstance(en, list):
        for u in en:
            m = re.search(r'/news/(\d+)', u)
            if m:
                m1_by_nid[int(m.group(1))] = e

# ---------- 1) EN 分组(标题归一键 + 同月作用域 + 倒计时吸收) ----------
STOP = set('''the a an of for and or to in on at up off now new news offer offers discount discounts
store gaijin war thunder online game update get your you with this that from until last chance final
days day week weekend starts started ending ends end soon hurry miss don t extended extension available
buy purchase order today tomorrow back again more some huge big great best top special event events
sale shop is are be it its as by'''.split())
REMIND = re.compile(r'last chance|final|reminder|hurry|don.?t miss|extended|last day|ending soon|closing|only \d+ hours|only \d+ days', re.I)

def key_tokens(s):
    t = toks(s) - STOP
    return t or toks(s)

en_arts = sorted([a for a in arts if a.get('lang') != 'zh'],
                 key=lambda a: (tget(a).get('date') or '9999', a.get('aid') or 0))
def absorb(g, a, w):
    g['arts'].append(a)
    g['start'] = min(g['start'], w[0]) if w[0] and g['start'] else (g['start'] or w[0])
    g['end'] = max(g['end'], w[1]) if w[1] and g['end'] else (g['end'] or w[1])

groups = []
for a in en_arts:
    if (a.get('aid') in m1_by_nid) and m1_by_nid[a['aid']].get('type') != 'sale':
        continue  # M1 已有该文章对应活动(非 sale 的 M1 骨架活动),不重复建组
    w = win(a)
    kt = key_tokens(a_title(a))
    remind = bool(REMIND.search(a_title(a)))
    placed = False
    for g in groups:
        if g['type'] != (a.get('type') or 'special'):
            continue
        gw = (g['start'], g['end'])
        if not (overlaps(w, gw) or near(w, gw, 10)):
            continue
        # 同月作用域(起止月差 ≤1)
        if g['start'] and w[0] and abs((g['start'].year * 12 + g['start'].month) - (w[0].year * 12 + w[0].month)) > 1:
            continue
        gk = key_tokens(g['title'])
        inter = kt & gk
        if inter or remind or (not kt) or (not gk):
            absorb(g, a, w)
            placed = True
            break
    if not placed:
        groups.append({'type': a.get('type') or 'special', 'title': a_title(a) or a.get('name_en') or '?',
                       'start': w[0], 'end': w[1], 'arts': [a]})

# 倒计时/续期孤立组二次吸收:向同类型 14 天内最近的组并(容 1 个共享键即可)
standalone = [g for g in groups if len(g['arts']) == 1 and REMIND.search(g['title'])]
groups = [g for g in groups if g not in standalone]
for g in standalone:
    a = g['arts'][0]
    kt = key_tokens(g['title'])
    best, bd = None, 99
    for t in groups:
        if t['type'] != g['type'] or not t['start'] or not g['start']:
            continue
        dd = abs((t['start'] - g['start']).days)
        if dd < bd and dd <= 14 and (kt & key_tokens(t['title']) or not kt):
            best, bd = t, dd
    if best is not None:
        absorb(best, a, (g['start'], g['end']))
    else:
        groups.append(g)

# 折扣品重叠合并:同类型+窗口重叠+共享≥1个折扣品名前 25 字符
i = 0
while i < len(groups):
    j = i + 1
    merged_flag = False
    while j < len(groups):
        A, B = groups[i], groups[j]
        if A['type'] == B['type'] and overlaps((A['start'], A['end']), (B['start'], B['end'])):
            ia = {((x.get('item') or '')[:25]) for aa in A['arts'] for x in (aa.get('discounts') or [])}
            ib = {((x.get('item') or '')[:25]) for aa in B['arts'] for x in (aa.get('discounts') or [])}
            if ia & ib:
                A['arts'] += B['arts']
                A['start'] = min(A['start'], B['start']) if A['start'] and B['start'] else (A['start'] or B['start'])
                A['end'] = max(A['end'], B['end']) if A['end'] and B['end'] else (A['end'] or B['end'])
                groups.pop(j)
                merged_flag = True
                continue
        j += 1
    i += 1
print('EN 分组(强化归并后):', len(groups), '组')

# ---------- 2) M2 组 → 折叠进 M1 事件(窗口重叠 + 标题相似 + 类型相容) ----------
COMPAT = {'marathon': {'marathon', 'craft', 'festive', 'special'}, 'craft': {'craft', 'marathon', 'special'},
          'sale': {'sale', 'special'}, 'festive': {'festive', 'special', 'marathon'},
          'anniversary': {'anniversary', 'special', 'festive'}, 'battlepass': {'battlepass'},
          'april': {'april'}, 'worldwar': {'worldwar'}, 'special': {'special', 'sale'}, 'market': {'market', 'special'}}
folded = 0
kept = []
for g in groups:
    best, bs = None, 0.0
    gw = (g['start'], g['end'])
    for e in m1_events.values():
        if g['type'] not in COMPAT.get(e['type'], {g['type']}):
            continue
        ew = (d(e.get('start')), d(e.get('end')))
        if not (overlaps(gw, ew) or near(gw, ew, 5)):
            continue
        s = max(jac(g['title'], e.get('name_en') or ''), jac(g['title'], e.get('name_zh') or ''))
        if s > bs:
            best, bs = e, s
    if best is not None and bs >= 0.25:
        # 折叠:并入折扣/截止/来源/子活动
        for a in g['arts']:
            for x in a.get('discounts') or []:
                if not any((x.get('target'), x.get('item', '')[:30]) == (y.get('target'), y.get('item', '')[:30]) for y in best.get('discounts', [])):
                    best.setdefault('discounts', []).append(x)
            for x in a.get('deadlines') or []:
                best.setdefault('deadlines', []).append(x)
            for x in a.get('sub_events') or []:
                best.setdefault('sub_events', []).append(x)
            en_s = best['sources'].setdefault('en', [])
            if isinstance(en_s, str):
                best['sources']['en'] = en_s = [en_s]
            u = f"https://warthunder.com/en/news/{a['aid']}"
            if len(en_s) < 5 and u not in en_s:
                en_s.append(u)
        if g.get('zh_arts'):
            best.setdefault('_m2zh', []).extend(g['zh_arts'])
        folded += 1
    else:
        kept.append(g)
print('折叠进 M1:', folded, '组;独立保留:', len(kept), '组')

# ---------- 3) zh 文章挂接(M1 直配 → 独立组 ±7 天 → M1 事件 ±7 天) ----------
groups = kept
cnt_m1zh = 0
for a in [x for x in arts if x.get('lang') == 'zh']:
    aid = a.get('aid')
    if aid in m1_by_nid:
        m1_by_nid[aid].setdefault('_m2zh', []).append(a)
        cnt_m1zh += 1
        continue
    w = win(a)
    zt = toks(a.get('name_zh') or a_title(a))
    znum = {n for n in re.findall(r'\d[\d.,]{2,}\d|\d{3,}', json.dumps(a.get('discounts') or []) + (a.get('tasks') or '') + (a.get('name_zh') or '') + a_title(a))}
    best, bd = None, 99
    for g in groups:
        if g['type'] not in COMPAT.get(a.get('type') or g['type'], {g['type']}):
            continue
        gt = toks(g['title'])
        gnum = {n for n in re.findall(r'\d[\d.,]{2,}\d|\d{3,}', json.dumps([x for x in g['arts']]) + g['title'])}
        # 闸门(跨语言):latin 词交集 或 数字指纹交集(价格/分数),否则不许挂(防嵌合)
        if not ((zt & gt) or (znum & gnum)):
            continue
        gw = (g['start'], g['end'])
        dd = 99
        for x in (w[0], w[1]):
            for y in (gw[0], gw[1]):
                if x and y:
                    dd = min(dd, abs((x - y).days))
        if dd < bd:
            best, bd = g, dd
    if best is not None and bd <= 7:
        best.setdefault('zh_arts', []).append(a)
    else:
        for e in m1_events.values():
            if not e.get('name_zh') and (a.get('type') in COMPAT.get(e['type'], set()) or not a.get('type')):
                ew = (d(e.get('start')), d(e.get('end')))
                if near(w, ew, 4):
                    et = toks((e.get('name_en') or '') + (e.get('name_zh') or ''))
                    enum_ = {n for n in re.findall(r'\d[\d.,]{2,}\d|\d{3,}', json.dumps(e.get('discounts') or []) + (e.get('tasks') or '') + (e.get('name_en') or ''))}
                    if (zt & et) or (znum & enum_):
                        e.setdefault('_m2zh', []).append(a)
                        cnt_m1zh += 1
                        break
        else:
            groups.append({'type': a.get('type') or 'special', 'title': a.get('name_zh') or a_title(a) or '?',
                           'start': w[0], 'end': w[1], 'arts': [], 'zh_arts': [a]})
print('zh 直配 M1:', cnt_m1zh)

# ---------- 4) M1 事件吸收 _m2zh(补中文名) ----------
for e in m1_events.values():
    zl = e.pop('_m2zh', [])
    if zl and not e.get('name_zh'):
        for a in zl:
            t = re.sub(r'^\[[^\]]*\]\s*', '', (a.get('name_zh') or a.get('title') or '').strip())
            t = re.sub(r'\s*[-–—]\s*(新闻|战争雷霆).*$', '', t)
            if t:
                e['name_zh'] = t
                zs = e['sources'].setdefault('zh', [])
                if zs is None:
                    e['sources']['zh'] = zs = []
                if isinstance(zs, str):
                    e['sources']['zh'] = zs = [zs]
                if len(zs) < 3:
                    zs.append(f"https://warthunder.com/zh/news/{a['aid']}")
                break

# ---------- 5) 组 → 新事件 ----------
def clean_title(t):
    t = re.sub(r'^\[(Shop|Event|Special|Market|Warbonds|[^\]]*)\]\s*', '', (t or '').strip())
    t = re.sub(r'^(Shop|Event|Special|Market|Warbonds)\s*[-–—]\s*', '', t)
    t = re.sub(r'\s*[-–—]\s*(News|新闻).*$', '', t)
    t = re.sub(r'\s*[-–—]\s*War Thunder$', '', t)
    t = re.sub(r'\s*\((?:offer is over|updated)[^)]*\)\s*$', '', t, flags=re.I)
    return t.strip() or '?'

new_events = []
used = Counter()
dropped = 0
for g in groups:
    if not g['arts'] and not g.get('zh_arts'):
        continue
    # 战令 2020-12 前不存在:误判降级为 special
    if g['type'] == 'battlepass' and g['start'] and g['start'] < date_today().replace(year=2020, month=12, day=1):
        g['type'] = 'special'
    announce = g['arts'][0] if g['arts'] else (g.get('zh_arts') or [None])[0]
    discs, dls, subs, rw = [], [], [], []
    seen_d = set()
    for src in (g['arts'] + g.get('zh_arts', [])):
        for x in (src or {}).get('discounts') or []:
            k = (x.get('target'), (x.get('item') or '')[:30])
            if k not in seen_d:
                seen_d.add(k)
                discs.append(x)
        dls += (src or {}).get('deadlines') or []
        subs += (src or {}).get('sub_events') or []
        rw += (src or {}).get('rewards_text') or []
    start = (announce or {}).get('start') or (g['start'].isoformat() if g['start'] else None)
    end = (announce or {}).get('end') or (g['end'].isoformat() if g['end'] else None)
    if not start and end:
        start = end
    if not start and not end and not discs and not rw:
        dropped += 1
        continue
    # 史前噪声:2012-06 前无折扣无奖励的条目丢弃
    if start and start[:7] < '2012-06' and not discs and not rw:
        dropped += 1
        continue
    name_zh = None
    for a in g.get('zh_arts', []):
        t = re.sub(r'^\[[^\]]*\]\s*', '', (a.get('name_zh') or a.get('title') or '').strip())
        t = re.sub(r'\s*[-–—]\s*(新闻|战争雷霆).*$', '', t)
        if t:
            name_zh = t
            break
    ym = (g['start'] or g['end'] or date_today()).strftime('%Y%m')
    base = f"{g['type']}_{ym}"
    used[base] += 1
    eid = base if used[base] == 1 else f"{base}_{chr(96 + used[base])}"
    while eid in m1_events:
        eid += 'x'
    zh_only = not g['arts']
    new_events.append({
        'id': eid, 'type': g['type'],
        'name_zh': name_zh,
        'name_en': None if (zh_only and name_zh) else clean_title((announce or {}).get('name_en') or g['title']),
        'bp_season': None,
        'start': start, 'end': end,
        'end_precision': (announce or {}).get('end_precision'),
        'end_raw': (announce or {}).get('end_raw'),
        'dm_event': None, 'vehicles': [],
        'awards': sorted(set(rw))[:12],
        'discounts': discs, 'deadlines': dls, 'sub_events': subs,
        'tasks': next((a.get('tasks') for a in g['arts'] if a.get('tasks')), None),
        'notes': next((a.get('notes') for a in reversed(g['arts']) if a.get('notes')), None),
        'sources': {
            'en': [f"https://warthunder.com/en/news/{a['aid']}" for a in g['arts'][:4]] or None,
            'zh': [f"https://warthunder.com/zh/news/{a['aid']}" for a in g.get('zh_arts', [])[:2]] or None,
        },
        'confidence': round(min(1.0, 0.35 + 0.2 * bool(end) + 0.2 * bool(discs) + 0.1 * bool(name_zh) + 0.15 * (len(g['arts']) > 1)), 2),
    })
print('新事件:', len(new_events), '空组丢弃:', dropped)

all_events = sorted(list(m1_events.values()) + new_events, key=lambda x: (x.get('start') or x.get('end') or '0000'), reverse=True)
out = {
    'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'build': 'm2',
    'counts': {
        'events': len(all_events),
        'by_type': dict(Counter(e['type'] for e in all_events)),
        'with_vehicles': sum(1 for e in all_events if e.get('vehicles')),
        'with_zh_name': sum(1 for e in all_events if e.get('name_zh')),
        'with_end': sum(1 for e in all_events if e.get('end')),
        'with_discounts': sum(1 for e in all_events if e.get('discounts')),
        'm2_new': len(new_events),
    },
    'events': all_events,
}
json.dump(out, open(f'{SITE}/data/events.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(out, open(f'{DATA}/events_build.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"events.json: {len(all_events)} 条(M1 {len(m1_events)} + M2 新增 {len(new_events)}), {os.path.getsize(f'{SITE}/data/events.json')/1024:.0f} KB")
print(json.dumps(out['counts'], ensure_ascii=False))
