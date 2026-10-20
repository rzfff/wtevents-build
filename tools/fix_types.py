#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""标签修正引擎:anniversary 语义三分(游戏周年庆|历史纪念日|纪念返售促销)+ 新类型 memorial"""
import json, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

GAME_ANN = re.compile(
    r'(war.?thunder|战争雷霆|战雷|gaijin)[^\n]{0,28}(anniversar|birthday|\d+\s*years?|周年|生日)'
    r'|anniversary[^\n]{0,12}war.?thunder|reaches its \d+(st|nd|rd|th)?\s*ye?a?r?|周年庆|周年庆典|生日庆典'
    r'|birthday,? war thunder'
    r'|war.?thunder.?[\u2019\']?s \d{1,2}(st|nd|rd|th)? (anniversar|birthday)'
    r'|\d{1,2}(st|nd|rd|th) anniversary together', re.I)
BATTLE_NATION = re.compile(
    r'battle of|d-?day|v-?day|victory|胜利|liberation|解放|independence|独立'
    r'|normandy|诺曼底|stalingrad|斯大林|kursk|库尔斯克|midway|中途岛|britain|不列颠'
    r'|leningrad|列宁格勒|guadalcanal|瓜岛|moscow|莫斯科|berlin|柏林'
    r'|air force|空军|navy|海军|army|陆军|坦克手|armed forces|武装部队|军队'
    r'|national day|国庆|建军|抗战|二战结束|world war|载人航天|space flight|poland regains|波兰', re.I)
MEM_SEM = re.compile(r'anniversar|周年|纪念日|纪念|birthday|生日|诞辰|first flight|首飞|day!|jubilee', re.I)
EQUIP_SUBJ = re.compile(r'first flight|首飞|designer|bureau|construct|诞生', re.I)
DISCOUNT_ACT = re.compile(
    r'discount|折扣|返售|返场|限时|returns?\b|back (?:with|for)|temporarily'
    r'|available (?:at|for)|上架|re-?introduc|on sale|sale', re.I)
PERSON_SUBJ = re.compile(
    r'(?:birthday|诞辰|anniversary)[^\n]{0,30}\b(?:of\b)?[A-Z][a-z]+|[\u4e00-\u9fff]{2,4}(?:诞辰|生日)')

PREORDER = re.compile(r'预售|预购|pre-?order', re.I)
HOLIDAY = re.compile(r'妇女节|women.?s day|christmas|圣诞|新年|new year|halloween|万圣|valentine|情人节|st.?patrick|母亲节|father.?s day|感恩节|thanksgiving', re.I)
SPORTS = re.compile(r'足球|football|联赛|league|锦标赛|tournament|e-?sports|世界杯|world cup', re.I)
CHEST = re.compile(r'百宝箱|chest|战利品|涂装|camouflage|loot|皮肤|skin', re.I)

CROSSOVER = re.compile(r'atomic heart|come to war thunder|联动|collab', re.I)

def classify(e):
    name = (e.get('name_en') or '') + ' ' + (e.get('name_zh') or '')
    t = e['type']
    if re.search(r'足球|football', name):
        return None, None  # 坦克足球等体育模式永不改类
    if e.get('bp_season'):
        return None, None  # 战令季永不改类(第 1 季「胜利 75 周年」教训)
    if CROSSOVER.search(name) and t in ('special', 'anniversary', 'festive'):
        return 'market', 'IP 联动'
    if GAME_ANN.search(name):
        m = GAME_ANN.search(name)
        if re.search(r'周年庆|周年庆典|生日庆典', m.group(0)) and not re.search(r'战雷|雷霆|gaijin|thunder', name, re.I):
            pass
        else:
            return 'anniversary', '游戏本体周年/生日'
    if PREORDER.search(name):
        return ('sale' if t != 'sale' else None), '预购/预售属促销'
    if HOLIDAY.search(name) and t in ('festive', 'special', 'memorial', 'sale'):
        return 'festive', '传统节日'
    if MEM_SEM.search(name):
        if BATTLE_NATION.search(name):
            return 'memorial', '历史/国别/军种纪念'
    if SPORTS.search(name) or CHEST.search(name):
        return None, None
    if MEM_SEM.search(name):
        if (EQUIP_SUBJ.search(name) or PERSON_SUBJ.search(name)) and (DISCOUNT_ACT.search(name) or e.get('discounts')):
            return 'sale', '纪念由头的返售/折扣'
        if t in ('special', 'festive', 'sale', 'anniversary'):
            return 'memorial', '人物/机构/装备纪念'
    if t == 'anniversary':
        if DISCOUNT_ACT.search(name) or e.get('discounts'):
            return 'sale', 'anniversary 误挂→实为促销'
        return 'special', 'anniversary 误挂→归特别'
    return None, None

for p in ['E:/ah/wtevents-build/site/data/events.json', 'E:/ah/wtevents-build/data/events_build.json']:
    d = json.load(open(p, encoding='utf-8'))
    changes = []
    for e in d['events']:
        nt, why = classify(e)
        if nt and nt != e['type']:
            changes.append((e['id'], e['type'], nt, why, (e.get('name_zh') or e.get('name_en') or '')[:36]))
            e['type'] = nt
        # 周年庆事件的 zh 名不含周年语义=误挂的子帖标题 → 退回英文
        if e['type'] == 'anniversary' and e.get('name_zh') and not re.search(r'周年|生日|庆典|anniversar|birthday', e['name_zh'], re.I):
            e['name_zh'] = None
    d['counts']['by_type'] = dict(Counter(e['type'] for e in d['events']))
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if 'site' in p else None)
    print(f"== {'site' if 'site' in p else 'build'}: 改 {len(changes)} 条 ==")
    if 'site' in p:
        for c in changes:
            print(f"  {c[0]:26s} {c[1]:>10s} -> {c[2]:<9s} [{c[3]}] {c[4]}")
