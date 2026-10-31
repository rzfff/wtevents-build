#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""增量八轮(2026-11-01):949→951。
+2 新事件:special_202611 史海拾遗·十一月「幸运王牌」/ sale_202611 强-5D 与 F/A-18D 预购
+11 处 sources 补挂(10-26 六直构事件的双语源 + 10-28 五事件的 EN 源)
+anniversary_202610 重写为 14 周年大伞(游戏内折扣/商店大促/贴花任务/鼠式回归/周边,五个子窗全细)
+sale_202610_k 补 J35XS 折扣行(文章实提两机同折)
站长令(2026-11-01):活动内容写细一点——本批起 discounts/tasks/awards/deadlines/notes 全字段充实。
"""
import json, io, sys
sys.stdout.reconfigure(encoding='utf-8')
P = r'E:\ah\wtevents-build\site\data\events.json'
d = json.load(io.open(P, encoding='utf-8'))
ev = d['events']
by = {e['id']: e for e in ev}

def src(e, en=None, zh=None):
    s = e.setdefault('sources', {'en': [], 'zh': []})
    if s is None: s = e['sources'] = {'en': [], 'zh': []}
    for k, ids in (('en', en), ('zh', zh)):
        for i in (ids or []):
            u = f'https://warthunder.com/{k}/news/{i}'
            if u not in s.setdefault(k, []):
                s[k].append(u)

# ---------- A. 补挂源(11) ----------
src(by['sale_202610_g'], '10269', '2828')   # 特拉法尔加
src(by['sale_202610_h'], '10270', '2830')   # 加拿大涅厄泊日
src(by['sale_202610_i'], '10273', '2832')   # UH-1C XM-30
src(by['sale_202610_j'], '10274', '2833')   # 黄貂鱼 II 预购
by['sale_202610_j']['notes'] = (by['sale_202610_j'].get('notes') or '') + ' 预购车随 2.60「鹰之影」大版本实装。'
src(by['sale_202610_k'], '10278', '2837')   # J35A 龙式
if not any('J35XS' in (r.get('target') or '') for r in by['sale_202610_k']['discounts']):
    by['sale_202610_k']['discounts'].append({
        'target': 'Saab J35XS(瑞典 VI 级战机,出口型)', 'item': '与 J35A 同享 -50%;文章明言两机同折',
        'percent': 50})
src(by['special_202610_d'], '10282')        # 槲寄生 2
src(by['festive_202610_b'], '10286')        # 万圣节竞速
src(by['special_202610_c'], '10283')        # 核冲突全真测试
src(by['sale_202610_p'], '10281')           # A-20 浩劫
src(by['special_202610_e'], '10275')        # Twitch 掉宝

# ---------- B. anniversary_202610 重写为 14 周年大伞 ----------
a = by['anniversary_202610']
a['name_zh'] = '战争雷霆 14 周年庆(游戏内折扣+商店大促+贴花任务+鼠式回归)'
a['name_en'] = "War Thunder's 14th Birthday Celebration"
a['start'] = '2026-10-23T11:00:00Z'
a['end'] = '2026-11-11T11:00:00Z'
a['end_precision'] = 'hour'
a['deadlines'] = [
    {'what': '游戏内折扣(预庆)', 'start': '2026-10-23T11:00:00Z', 'end': '2026-10-28T11:00:00Z',
     'detail': '全国家载具银狮/金鹰购买 5 折;不含 Sky Odyssey 与 Heavy Cavalry 两代大版本新增车'},
    {'what': 'Gaijin 商店周年大促', 'start': '2026-10-28T11:00:00Z', 'end': '2026-11-02T11:00:00Z',
     'detail': '大批捆绑包至多 -50%:ZTZ96B 包($69.99→$35)/A-10A 雷电早期包($59.99→$30)/BMPT-72 包($69.99→$35)/Alpha Jet A 包($59.99→$30)等;促销结束後 Vickers GBT155、AH-64DJP、Northrop NF-5A 三包全平台下架'},
    {'what': '14 周年纪念贴花任务', 'start': '2026-10-30T11:00:00Z', 'end': '2026-11-05T11:00:00Z',
     'detail': '任意 III 级或以上载具,任意模式打 1 场即得「战争雷霆 14 周年」纪念贴花'},
    {'what': '鼠式(Maus)年度回归研发', 'start': '2026-10-30T11:00:00Z', 'end': '2026-11-05T11:00:00Z',
     'detail': '德系陆战 V 级解锁即可开研鼠式;窗口内投入任意研发点(哪怕 1 点)活动结束後不清空,可随时续研'},
    {'what': '蜗牛玩偶(Makeship 周边)', 'start': None, 'end': '2026-11-07T16:00:00Z',
     'detail': 'Gaijin 首次 Makeship 联名限量实体周边,售完即绝版;2027-03-12 起发货'},
]
a['awards'] = ['「战争雷霆 14 周年」纪念贴花(完成 1 场战斗任务即得)']
a['tasks'] = ['任意 III 级+载具完成 1 场战斗(任意模式)→ 14 周年纪念贴花']
a['notes'] = ('游戏开放测试始于 2012-11-01,本轮为 14 周年;庆典主窗 2026-10-28 11:00→11-11 11:00 GMT,'
              '与「梦想成真:槲寄生 2」活动同窗收官(Mistel 2=Ju 88 G-1 机身改巨型聚能战斗部的 FW 190 A-8 复合机,绰号「父子」);'
              '游戏内 5 折预庆(10-23~10-28)早于庆典主窗一周开启。')
src(a, ['10277', '10299', '10288'], ['2836', '2858', '2848'])

# ---------- C. 新事件(2) ----------
new = [
    {
        'id': 'special_202611', 'type': 'special',
        'name_zh': '史海拾遗·十一月:幸运王牌', 'name_en': 'Pages of History (November): Incredible Luck',
        'start': '2026-11-01', 'end': '2026-11-30', 'end_precision': 'day',
        'end_raw': 'From November 1st until November 30th',
        'dm_event': None, 'vehicles': [],
        'awards': ['每任务战利品箱×8(逐任务发放)', '全部完成:独特个人资料图标'],
        'discounts': [],
        'tasks': ['11 月内连续完成 8 个任务:使用与当期史实事件关联的载具参战;每完成 1 个任务得 1 个战利品箱,8 个全完成额外得独特个人资料图标'],
        'notes': ('月度任务活动「史海拾遗/Pages of History」11 月篇:主题覆盖意大利、苏联、埃及、伊朗等多战场的历史事件,'
                  '驾驶与史实挂钩的载具参战取奖;本期主角人物=英国王牌飞行员 Robert Tuck。'),
        'sources': {'en': ['https://warthunder.com/en/news/10291'],
                    'zh': ['https://warthunder.com/zh/news/2851']},
    },
    {
        'id': 'sale_202611', 'type': 'sale',
        'name_zh': '强-5D 与 F/A-18D 礼包开启预售(2.60「鹰之影」)', 'name_en': 'Pre-orders: F/A-18D and Q-5D',
        'start': '2026-10-29', 'end': None, 'end_precision': 'none',
        'end_raw': '预售自 10-29 起,随 2.60 大版本实装截止(未公布固定结束时间)',
        'dm_event': None, 'vehicles': [],
        'awards': ['预购赠品:「恶魔之刺」称号(F/A-18D 包)', '「VMFA-232 红魔」臂章贴花(F/A-18D 包)'],
        'discounts': [
            {'target': 'F/A-18D Pack(美 VIII 级高级双座大黄蜂)',
             'item': '$79.99:含 F/A-18D+30 天高级账号+3000 金鹰+预购称号与贴花', 'percent': None},
            {'target': 'Q-5D Pack(中 VI 级高级强击机)',
             'item': '含 Q-5D+高级账号+金鹰(价格见商店页)', 'percent': None},
        ],
        'tasks': [],
        'notes': ('2.60「鹰之影」(Eagle\'s Shadow)大版本双预购:F/A-18D——美系双座高级大黄蜂,最多 6 枚 AIM-120B 主动雷达弹,'
                  '激光/卫星制导武器齐备;Q-5D——中超音速强击机,64 组干扰弹+全向雷达告警(可探测地空导弹发射),'
                  '无空空弹、依赖双 23mm 翼根航炮,定位在 Q-5/Q-5A 与 Q-5L/A-5C 之间,BR 约 9.0-9.3,利好高级队列研发。'
                  '⚠ 官方声明:实装前性能可能调整。'),
        'sources': {'en': ['https://warthunder.com/en/news/10293'],
                    'zh': ['https://warthunder.com/zh/news/2853']},
    },
]
exist = {e['id'] for e in ev}
for n in new:
    if n['id'] not in exist:
        ev.append(n)
        print('+', n['id'])

# ---------- D. meta ----------
d['generated_at'] = '2026-11-01T00:00:00Z'
d['counts'] = {
    'events': len(ev),
    'by_type': d['counts']['by_type'],
    'with_discounts': sum(1 for e in ev if e.get('discounts')),
}
from collections import Counter
c = Counter(e.get('type') for e in ev)
d['counts']['by_type'] = dict(c)
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', dict(c))
print('SAVED')
