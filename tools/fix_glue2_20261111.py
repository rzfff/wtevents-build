#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-11-11 连环合成体终修(M4 收尾二段)。
病根深化:UK/法国武装部队日与涂装箱也被 M2 粘成三位一体——
  special_202506_b = UK2025+法2025+利维坦涂装箱三名一体
  festive_202606  = UK2026+法2026 双名一体(顶着「法国空军」假名)
  special_202606_d = 被 fix_series 误覆盖(核战冲突回归),本批复活
处置:UK2025/UK2026 归位、法2025/法2026/利维坦涂装箱三事件补建、删重复 _c、复活核战。
素材:en_9593/10121 全文(frarts.txt)+此前 deeparts 系。
"""
import json, io, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
P = r'E:\ah\wtevents-build\site\data\events.json'
d = json.load(io.open(P, encoding='utf-8'))
ev = d['events']
by = {e['id']: e for e in ev}

# ---------- 1. special_202506_b → UK 武装部队纪念日 2025(归位) ----------
e = by['special_202506_b']
e.update({
 'name_zh': '英国武装部队纪念日:「2025 英国武装力量纪念日」贴花',
 'awards': ['「2025 英国武装力量纪念日」贴花'],
 'tasks': ('使用英国 III 级及以上载具完成 3 场战斗(活跃度≥70%;排除无间断对抗/守卫模式/直升机 PVE)'
           '→「2025 英国武装力量纪念日」贴花;进度在 昵称→成就→节假日;贴花在自定义「纪念日与节假日」分类'),
 'notes': ('英国武装部队纪念日=每年 6 月最后一个星期六(2025 年为 6 月 28 日),预备役提前 3 天;全英 170 场庆典。'
           '⚠ 2026-11-11 修复:本条原为 UK2025+法国空军节2025+利维坦涂装箱三名一体(EN 名与任务实为 UK,'
           '中文名偷自涂装箱文),后两者已拆出为 special_202507_d 与 market_202506'),
 'sources': {'en': ['https://warthunder.com/en/news/9586'], 'zh': ['https://warthunder.com/zh/news/2175']},
})

# ---------- 2. 删我建的重复 special_202506_c ----------
ev[:] = [x for x in ev if x['id'] != 'special_202506_c']

# ---------- 3. market_202506:利维坦涂装箱(新建) ----------
n_cam = {
 'id': 'market_202506', 'type': 'market',
 'name_zh': '40 款玩家自制涂装随「利维坦」百宝箱加入游戏!',
 'name_en': '40 New User-Created Camouflages in the Leviathan Trophy!',
 'start': '2025-06-27', 'end': None, 'end_precision': 'none',
 'end_raw': '2025-06-27 上架(随利维坦版本),持续至下批涂装箱接档',
 'dm_event': None, 'vehicles': [],
 'awards': ['「利维坦」百宝箱(40 款玩家自制涂装池)'], 'discounts': [], 'deadlines': [], 'tasks': '',
 'notes': ('玩家自制涂装月更系列(同黄蜂之蜷/火线交锋百宝箱);⚠ 2026-11-11 修复时从 special_202506_b 三名一体中拆出;'
           'EN 孪生未随合并带入,暂 zh 单源,待增量补挂'),
 'sources': {'en': [], 'zh': ['https://warthunder.com/zh/news/2174']},
}

# ---------- 4. special_202507_d:法国空军节 2025(新建) ----------
n_fr25 = {
 'id': 'special_202507_d', 'type': 'special',
 'name_zh': '法国空军节:「法国空军节 2025」贴花', 'name_en': 'A New Decal for French Air Force Day!',
 'start': '2025-07-03T11:00:00Z', 'end': '2025-07-07T11:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From July 3rd (11:00 GMT) until July 7th (11:00 GMT)',
 'dm_event': None, 'vehicles': [],
 'awards': ['「法国空军节 2025」贴花'], 'discounts': [], 'deadlines': [],
 'tasks': ('使用法国 III 级及以上飞机完成 3 场战斗(活跃度≥70%;排除无间断对抗/守卫模式)'
           '→「法国空军节 2025」贴花;贴花在自定义「法国→空军」分类'),
 'notes': ('法国空军 1934-07-02 自陆军独立(一战起大规模用兵,间战期机队欧洲最大);现役 4 万余人,'
           '200 架幻影 2000 与阵风。⚠ 2026-11-11 修复时从 special_202506_b 三名一体中拆出;'
           'EN 孪生未随合并带入,暂 zh 待补(zh_2174 系涂装箱文不属此)。'),
 'sources': {'en': ['https://warthunder.com/en/news/9593'], 'zh': []},
}

# ---------- 5. festive_202606 → UK 武装部队纪念日 2026(归位) ----------
e = by['festive_202606']
e.update({
 'name_zh': '英国武装部队纪念日:贴花物资箱',
 'awards': ['「英国武装部队纪念日」贴花物资箱(三选一往期贴花:英国武装部队纪念日/英国国防部纹章/2025 英国武装力量纪念日;集齐改得:20-50% 研发或银狮加成卡/3-5 通用备用载具/1 天高级账号)'],
 'tasks': ('使用英国科技树 III 级及以上载具累计 3000 任务分(随机战斗,排除守卫模式)→贴花物资箱;'
           '完成后手动领取(昵称→成就→节假日→英国武装部队纪念日);纪念日贴花在「纪念日与节假日」分类,'
           '国防部纹章与 2025 贴花在「英国→陆军」分类'),
 'notes': ('首批维多利亚十字勋章 1857-06-26 授予;2009 年起 6 月最后一个星期六为纪念日。英军二战史/租借法案/'
           '福克兰投送。⚠ 2026-11-11 修复:本条原为 UK2026+法国空军节2026 双名一体(顶着法国空军假名,'
           'EN 名与任务实为 UK),法国侧已拆出为 special_202607_f'),
 'sources': {'en': ['https://warthunder.com/en/news/10114'], 'zh': ['https://warthunder.com/zh/news/2677']},
})

# ---------- 6. special_202607_f:法国空军节 2026(新建) ----------
n_fr26 = {
 'id': 'special_202607_f', 'type': 'special',
 'name_zh': '法国空军节:贴花战利品箱', 'name_en': 'Celebrating French Air Force Day with a Decal Trophy!',
 'start': '2026-07-02T11:00:00Z', 'end': '2026-07-05T11:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From July 2nd (11:00 GMT) until July 5th (11:00 GMT)',
 'dm_event': None, 'vehicles': [],
 'awards': ['「法国空军节」战利品箱(往期贴花四选一:法国空军节/法国空军司令部纹章/法国空军节 2025;集齐改得加成卡/备用载具/1 天高级账号)'],
 'discounts': [], 'deadlines': [],
 'tasks': ('使用法国 III 级及以上飞机累计 3000 任务分(随机战斗,排除守卫模式)→战利品箱;完成后手动领取'
           '(昵称→成就→节假日→法国空军节);司令部纹章与 2025 贴花在「法国→空军」分类,其余在「节假日」分类'),
 'notes': ('法国空军 1934-07-02 独立成军;二战中法籍飞行员在皇家空军与苏联空军(诺曼底-涅曼团)服役;'
           '战后幻影/阵风自研谱系。⚠ 2026-11-11 修复时从 festive_202606 双名一体中拆出。'),
 'sources': {'en': ['https://warthunder.com/en/news/10121'], 'zh': ['https://warthunder.com/zh/news/2684']},
}

# ---------- 7. special_202606_d:复活核战冲突回归(被误覆盖) ----------
n_nuke = {
 'id': 'special_202606_d', 'type': 'special',
 'name_zh': '核战冲突模式限时回归!', 'name_en': 'Nuclear Escalation Returns!',
 'start': '2026-06-26T12:00:00Z', 'end': '2026-07-06T11:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From June 26th (12:00 GMT) until July 6th (11:00 GMT)',
 'dm_event': None, 'vehicles': [], 'awards': [], 'discounts': [], 'deadlines': [],
 'tasks': '全国家可参加的大规模核冲突活动,BR 13.0-14.7,5/30千吨级核弹由战术机携带,以摧毁目标总分定胜负,无即时胜利',
 'notes': '四月活动改进版:可驾驶任意国家自机、新增AI舰队、前线扩大、重生机制与防空火控改动。⚠ 2026-11-11 曾被系列修复脚本误覆盖,当批复活(内容=git 原版)',
 'sources': {'en': ['https://warthunder.com/en/news/10115'],
             'zh': ['https://warthunder.com/zh/news/2678', 'https://warthunder.com/zh/news/2686']},
}

for n in (n_cam, n_fr25, n_fr26, n_nuke):
    if n['id'] in by:
        ev[ev.index(by[n['id']])] = n; print('↻', n['id'])
    else:
        ev.append(n); print('+', n['id'])

d['generated_at'] = '2026-11-11T17:00:00Z'
d['counts'] = {'events': len(ev), 'by_type': dict(Counter(e.get('type') for e in ev)),
               'with_discounts': sum(1 for e in ev if e.get('discounts'))}
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', d['counts']['by_type'])
print('SAVED')
