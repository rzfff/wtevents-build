#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wtevents M1 机械层:timelapse 骨架 + datamine 载具 + 官方中文名 + sitemap 日期对齐 + 抓取队列
产物全部落 data/,stdout 打印汇总。只读源,不写源。"""
import json, re, os, sys, html
from datetime import date, datetime

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
os.makedirs(DATA, exist_ok=True)

TL = 'E:/ah/tmp-wt/gapcheck/tl.json'
ZHC = 'E:/ah/wt-tools-research/r2/zhcover/final_id_coverage.json'
VFULL = 'E:/ah/wtapi-build/dist/api/vehicles-full.json'
SM_EN = 'E:/ah/tmp-wt/sm-en-full.xml'
SM_ZH = 'E:/ah/tmp-wt/sm-zh-full.xml'

def load(p):
    return json.load(open(p, encoding='utf-8'))

def dump(name, obj):
    p = os.path.join(DATA, name)
    json.dump(obj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return p

ROMAN = {'i':1,'ii':2,'iii':3,'iv':4,'v':5,'vi':6,'vii':7,'viii':8,'ix':9,'x':10,'xi':11,'xii':12,
         'xiii':13,'xiv':14,'xv':15,'xvi':16,'xvii':17,'xviii':18,'xix':19,'xx':20,'xxi':21,'xxii':22,
         'xxiii':23,'xxiv':24,'xxv':25}

# ---------- 1. timelapse 骨架 ----------
tl = load(TL)
acts = [it for it in tl['items'] if it['section'] != 'updates']
print('timelapse 活动条数:', len(acts), '分节:', {s: sum(1 for a in acts if a['section']==s) for s in set(a['section'] for a in acts)})

bp_counter = 0
skeleton = []
for it in acts:
    title = (it.get('title') or '').strip()
    start = it.get('start_date')
    feats = it.get('features') or []
    awards, other = [], []
    for f in feats:
        ft = (f.get('title') or '')
        fis = f.get('items') or []
        if 'award' in ft.lower():
            awards += fis
        elif 'release' not in ft.lower():
            other.append(ft.rstrip(': ') + ': ' + ' | '.join(fis))
    bp_season = None
    if it['section'] == 'battlepass':
        bp_counter += 1
        bp_season = bp_counter  # 按 start 排序已是时间序(tl 自带顺序)
        m = re.search(r'Season\s+([IVXL]+)\b', title, re.I)
        if m and ROMAN.get(m.group(1).lower()) != bp_season:
            print('  [warn] BP 序号不一致:', title, '序号', bp_season, 'vs 罗马', m.group(1))
    eid = re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')[:64]
    news = it.get('linkNews') or ''
    m = re.search(r'/news/(\d+)', news)
    news_id = int(m.group(1)) if m else None
    skeleton.append({
        'key': f"{(start or 'xxxx')[:4]}_{eid}" if start else eid,
        'section': it['section'],
        'bp_season': bp_season,
        'title': title,
        'start': start,
        'news_id': news_id,
        'news_url': news or None,
        'wiki_vehicles': it.get('linkVehicles'),
        'img': (it.get('img') or {}).get('preview'),
        'awards': awards,
        'feats_other': other,
    })
seen = {}
for s in skeleton:
    seen[s['key']] = seen.get(s['key'], 0) + 1
    if seen[s['key']] > 1:
        s['key'] += f"_{seen[s['key']]}"
no_news = [s['key'] for s in skeleton if not s['news_url']]
print('骨架:', len(skeleton), '条;无 linkNews:', len(no_news), no_news)
dump('skeleton.json', skeleton)

# ---------- 2. datamine 载具(vehicles-full 自带 event 字段 + locales EN 名) ----------
vf = load(VFULL)
EN_VEH = load('E:/ah/wtapi-build/dist/locales/en.json').get('vehicles', {})

def clean_disp(s):
    s = (s or '').replace('\u200b', '').strip()
    return re.sub(r'^[^\x20-\x7e\u4e00-\u9fff]+', '', s)  # 剥前缀缴获/国籍标记符

def v_name(vid):
    return clean_disp(EN_VEH.get(vid + '_short') or EN_VEH.get(vid + '_extended') or vid)

event_vehicles = {}   # dm_event_id -> [ {id,name_en,name_zh?,release,image} ]
for v in vf:
    e = v.get('event')
    vid = v['identifier']
    if not e:
        continue
    event_vehicles.setdefault(e, []).append({
        'id': vid, 'name_en': v_name(vid), 'release_date': v.get('release_date'),
        'image': f"/wtapi/assets/images/{vid}.png",
    })
print('datamine 活动→载具:', len(event_vehicles), '个活动 ID,合计', sum(len(x) for x in event_vehicles.values()), '台')
dump('event_vehicles.json', event_vehicles)

# ---------- 3. 官方中文名(menu.csv 结论复用) ----------
zhoff = {}
z = load(ZHC)
for lvl in ('strong', 'weak'):
    for row in z.get(lvl, []):
        # [event_id, menu_key, zh_name, family]
        if isinstance(row, (list, tuple)) and len(row) >= 3 and row[2]:
            zhoff.setdefault(row[0], {'name_zh': row[2], 'grade': lvl})
print('官方中文名活动数:', len(zhoff))
dump('zh_official.json', zhoff)

# ---------- 4. 载具中文名(names-zh 家族前缀匹配) ----------
nz = load('E:/ah/wtapi-build/dist/api/names-zh.json')
fams = ['tracked_vehicles', 'aircraft', 'helicopters', 'ships', 'boats']
nz_exact = {}
for k, val in nz.items():
    if '/' in k:
        nz_exact[k.split('/', 1)[1]] = val  # 后段 id 直查(同名冲突取后写,概率低)
def v_zh(vid):
    if vid in nz:
        return nz[vid]
    for f in fams:
        if f + '/' + vid in nz:
            return nz[f + '/' + vid]
    return nz_exact.get(vid)
for eid, lst in event_vehicles.items():
    for vv in lst:
        vv['name_zh'] = v_zh(vv['id'])

# ---------- 5. timelapse ↔ datamine 活动对齐 ----------
def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())
dm_names = []  # (norm_name, event_id)
dm_exact = {}
for eid, lst in event_vehicles.items():
    for vv in lst:
        dm_names.append((norm(vv['name_en']), eid))
        dm_exact.setdefault(norm(vv['name_en']), eid)

def ymatch(e, y):
    if not y:
        return True
    my = re.search(r'(19|20)\d\d', e)
    return (not my) or my.group(0) == y

dm_match = {}
for s in skeleton:
    y = (s['start'] or '')[:4]
    hit = None
    if s['bp_season']:
        cand = f"battlepass_season{s['bp_season']}"
        if cand in event_vehicles:
            hit = cand
    if not hit:
        # 标题词直配:Summer/Winter + 年份
        tl = s['title'].lower()
        for word, pre in (('summer', 'summer_'), ('winter', 'winter_')):
            if word in tl and y and (pre + y) in event_vehicles:
                cand = pre + y
                # 校验:奖励车至少 1 台与该 datamine 活动重合,防跨年错配
                vv = {norm(x['name_en']) for x in event_vehicles[cand]}
                if not s['awards'] or any(any(n and (n in a or a in n) for n in vv) for a in map(norm, s['awards'])):
                    hit = cand
                    break
    if not hit and s['awards']:
        votes = {}
        for a in s['awards']:
            an = norm(re.sub(r'\(.*?\)', '', a))
            ex = dm_exact.get(an)
            if ex:
                votes[ex] = votes.get(ex, 0) + 2
            for n, e in dm_names:
                if len(n) >= 4 and len(an) >= 4 and (n in an or an in n):
                    votes[e] = votes.get(e, 0) + 1
        for e, c in sorted(votes.items(), key=lambda x: -x[1]):
            if not e.startswith('battlepass') and ymatch(e, y) and c >= 2:
                hit = e
                break
    dm_match[s['key']] = hit
matched = sum(1 for v in dm_match.values() if v)
print('datamine 对齐:', matched, '/', len(skeleton))
dump('dm_match.json', dm_match)

# ---------- 6. sitemap lastmod 对齐 + 抓取队列 ----------
def sm_dates(p):
    txt = open(p, encoding='utf-8', errors='ignore').read()
    out = {}
    for m in re.finditer(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', txt):
        out[m.group(1).strip()] = m.group(2)[:10]
    return out

en_d = sm_dates(SM_EN)
zh_d = sm_dates(SM_ZH)
print('sitemap lastmod: en', len(en_d), 'zh', len(zh_d))

from datetime import timedelta
def d2(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except Exception:
        return None

ZH_PREFIX_GOOD = ('shi-jian', 'shang-dian', 'te-shu', 'shi-chang', 'ren-wu-jiang-quan')
queue = []
zh_total = 0
for s in skeleton:
    en_url, en_id = s['news_url'], s['news_id']
    en_date = en_d.get(en_url) if en_url else None
    q = {'key': s['key'], 'en_id': en_id, 'en_url': en_url, 'en_date': en_date, 'zh': []}
    if en_url and en_id and not re.search(r'/news/\d+-', en_url):
        q['en_old_format'] = True
    cands = []
    if en_date:
        ed = d2(en_date)
        if ed:
            for u, dd in zh_d.items():
                zd = d2(dd)
                if not zd:
                    continue
                delta = abs((zd - ed).days)
                if delta <= 3:
                    slug_ok = u.endswith('-zh') or '/news/' in u
                    pref = any(('/' + p + '-') in u for p in ZH_PREFIX_GOOD)
                    cands.append((delta, 0 if pref else 1, u))
            cands.sort()
            q['zh'] = [u for _, _, u in cands[:3]]
            zh_total += len(q['zh'])
    queue.append(q)
print('抓取队列: EN', sum(1 for q in queue if q['en_url']), 'zh 候选', zh_total)
dump('fetch_queue.json', queue)

en_list = '\n'.join(f"{q['en_id'] or 'x'}\t{q['en_url']}" for q in queue if q['en_url'])
zh_list = '\n'.join(u for q in queue for u in q['zh'])
open(os.path.join(DATA, 'fetch_en.tsv'), 'w', encoding='utf-8').write(en_list)
open(os.path.join(DATA, 'fetch_zh.txt'), 'w', encoding='utf-8').write(zh_list + '\n')
print('DONE data/ 下产物就绪')
