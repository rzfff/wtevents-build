#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-11-23 增量十三轮:3 事件(PCE-842 海岸卫队事件/NF-5A 返场/鹰之暗影百宝箱)。
来源:官方新闻 en_10335/10341/10334 + zh_2893/2897/2892(标题官方原文,正文取 EN 全文核实)。
背景:站长 2026-11-23 质询「活动很久没更新」——彻查坐实 3 条漏更,根因=watch.sh 基线采集 bug(只盯第 2 页,
本批 3 文恰在第 1 页故哨兵从未报);本批同日修 watch.sh。幂等:↻ 按 id 整条替换。"""
import json, io, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

P = 'E:/ah/wtevents-build/site/data/events.json'
d = json.load(io.open(P, encoding='utf-8'))
ev = d['events']
exist = {e['id'] for e in ev}

V = lambda id, zh, en: ({'id': id, 'name_zh': zh, 'name_en': en, 'image': f'/wtapi/assets/images/{id}.png'} if zh
                        else {'id': id, 'name_en': en, 'image': f'/wtapi/assets/images/{id}.png'})

n1 = {
 'id': 'special_202611_f', 'type': 'special',
 'name_zh': '海岸卫队:PCE-842 出击(海军攒分活动)',
 'name_en': 'Get PCE-842 in the Coastal Defender Event!',
 'bp_season': None,
 'start': '2026-11-18T11:00:00Z', 'end': '2026-12-02T11:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From November 18th (11:00 GMT) until December 2nd (11:00 GMT)',
 'dm_event': None,
 'vehicles': [V('us_pce_842_class', 'PCE-842', 'PCE-842-class')],
 'awards': [
   '「港口卫士标志」(Port Guard Sign)贴花',
   '「可部署情报分队臂章」(Deployable Intelligence Element Chevron)贴花',
   '美国海岸警卫队舰旗(船舶挂饰)',
   '奖励箱(5-10 万银狮/银狮与研究点加成器/随机赌注与指令/通用备用载具 1-3 个/已拥有载具的随机涂装/1 天高级账号)',
 ],
 'discounts': [], 'deadlines': [], 'sub_events': [],
 'tasks': ('海军战斗(III 级及以上,街机/全真)攒任务点,每 35,000 分解锁一阶奖励,每阶奖励不同,完成后需手动领取'
           '(游戏内点昵称→Coastal Defender→Get Reward);机制与 special_202610_d 槲寄生 2 活动同款。'),
 'notes': ('PCE-842 级=二战美海军唯一正式定名「巡逻护航舰」(Patrol Craft Escort)的舰级,共造 68 艘,海岸巡逻/反潜/近海护航;'
           '游戏内为美系近岸 rank IV 活动护卫舰(BR 4.0):76mm 艏炮+6×40mm 博福斯+4×20mm 厄利孔,特色是深弹投射器'
           '(艉部滚投之外还可舷侧/舰首抛射),大体量慢速善守点。**注:本车 2026-11-20(2.61.0.33)已同步加入可研发科技树'
           '(银狮 70 万)——活动奖励车开活动期间即转正的先例,与 wtrp 第廿一次换版实测互证(event 95→94)。'),
 'sources': {'en': ['https://warthunder.com/en/news/10335'], 'zh': ['https://warthunder.com/zh/news/2893']},
}

n2 = {
 'id': 'sale_202611_e', 'type': 'sale',
 'name_zh': '纪念 F-5A-21 赢得国际战斗机竞标,NF-5A 重新上架',
 'name_en': "The NF-5A Returns for the Anniversary of the F-5A-21's Victory in the IFA Competition!",
 'bp_season': None,
 'start': '2026-11-20T11:00:00Z', 'end': '2026-11-23T11:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From November 20th (11:00 GMT) until November 23rd (11:00 GMT)',
 'dm_event': None,
 'vehicles': [V('nf_5a_netherlands', 'NF-5A', 'NF-5A')],
 'awards': [], 'deadlines': [], 'sub_events': [], 'tasks': None,
 'discounts': [
   {'target': 'NF-5A(法国 VII 级高级战斗机)', 'item': '限时 30% 折扣:6,489 金鹰(原价 9,270 金鹰);促销结束后以原价常驻上架(首次金鹰直售);商店位:法国>航空>高级载具', 'percent': 30},
 ],
 'notes': ('1970-11-20 北诺 F-5A-21 原型赢得国际战斗机(IFA)竞标,服役定名 F-5E——NF-5A 正是该谱系的荷兰版:'
           '诺斯罗普授权加拿大生产(CF-5A),荷兰批即 NF-5;F-5A-21 的辅进气口/机动襟翼/可伸前起落架等特征源自荷兰版。'
           '游戏内 NF-5A 为「利维坦」大版本引入的法国 VII 级高级机,不快但机动韧性好,20mm 机炮+丰富外挂,'
           '与美系 F-5A 差异=高级身份+独占涂装+可用 AIM-9J/N。2.61.0.37(2026-11-23)起由礼包(pack)转为高级(premium)在架。'),
 'sources': {'en': ['https://warthunder.com/en/news/10341'], 'zh': ['https://warthunder.com/zh/news/2897']},
}

n3 = {
 'id': 'market_202611', 'type': 'market',
 'name_zh': '40 款社区创作涂装随「鹰之暗影」百宝箱加入游戏',
 'name_en': "40 New User-Created Camouflages in the Eagle's Shadow Trophy!",
 'bp_season': None,
 'start': '2026-11-13T14:50:00Z', 'end': None, 'end_precision': 'none',
 'end_raw': '百宝箱长期在役(随下一期替换),无固定截止',
 'dm_event': None,
 'vehicles': [], 'awards': [], 'discounts': [], 'deadlines': [], 'sub_events': [],
 'tasks': None,
 'notes': ('「鹰之暗影」大版本配套百宝箱:17 地面+19 空军+2 海军+2 直升机=40 款社区涂装优惠券,另有稀有载具优惠券与'
           '「鹰之暗影」贴花优惠券。获取:II 级及以上载具、活跃度≥50% 的战斗后概率掉落(突击模式除外);'
           '主机端可在商城金鹰购买;PC 端需 GJN 市场购钥匙开箱,每笔购买按份分成给箱内皮肤作者。'
           '本文 11-13 14:50 发布,比当日 14:00 增量构建晚 50 分钟被卡线漏掉——增量十四轮(11-23)补录。'),
 'sources': {'en': ['https://warthunder.com/en/news/10334'], 'zh': ['https://warthunder.com/zh/news/2892']},
}

for n in (n1, n2, n3):
    if n['id'] in exist:
        ev[ev.index(next(e for e in ev if e['id'] == n['id']))] = n; print('↻', n['id'])
    else:
        ev.append(n); print('+', n['id'])

d['generated_at'] = '2026-11-23T04:30:00Z'
d['build'] = 'inc13-20261123'
d['counts'] = {'events': len(ev), 'by_type': dict(Counter(e.get('type') for e in ev)),
               'with_discounts': sum(1 for e in ev if e.get('discounts'))}
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', d['counts']['by_type'])
print('SAVED')
