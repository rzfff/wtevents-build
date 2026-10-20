#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-10-16 薄事件补数据:11 条 score 7-8 事件回源文章(en_9492 等 11 篇,text5/)重补
tasks/awards/discounts/notes/精确时间。来源:官方新闻原文逐篇人工核对。可重复运行(幂等覆盖)。"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

E = {
 'memorial_202505': dict(
   end='2025-05-12T13:00:00Z', end_precision='hour', end_raw='From May 7th (13:00 GMT) until May 12th (13:00 GMT)',
   tasks='III 级及以上载具完成三任务:「我们赢了!」贴花=70% 活跃度打 3 场;「DS-39」挂件=陆战累计 20000 任务分;「胜利日」资料背景=70% 活跃度赢 5 场;进度:昵称→成就→Victory Day。',
   awards=['「我们赢了!」贴花','「DS-39」陆战挂件','「胜利日」个人资料背景','往届胜利日奖励奖杯(游戏内物品商店:纪念碑主题贴花「后方-前线」「祖国」「解放者战士」与勃伦/ROKS-3/M1 加兰德/马克沁-托卡列夫等挂件)'],
   deadlines=[{'what':'Gaijin 商店二战参战载具礼包折扣截止','when':'2025-05-14T11:00:00Z'}],
   discounts=[{'target':'Gaijin 商店·二战参战载具礼包系列','item':'多款礼包/捆绑包限时折扣(05-07 11:00 起,详情见商店)', 'percent':None}],
   notes='欧洲胜利日 80 周年(1945-05-08 二战欧洲战事结束);同期联动「胜利传奇:T-34-85 游击队」活动(05-08~05-20,另立条目)。'),
 'sale_202410_d': dict(
   end='2024-10-28T09:00:00Z', end_precision='hour', end_raw='From today until October 28th (09:00 GMT)',
   discounts=[{'target':'J35A 龙式(瑞典战机)','item':'4545 金鹰;限时返场;商店位:瑞典>航空>高级载具','percent':50}],
   notes='SAAB 35 龙首飞纪念(1955-10-25):西欧首型超音速战机/双三角翼/首次完成眼镜蛇机动/平飞首破 2 马赫;机上无对抗措施,需机动规避导弹,固定武装 30mm Akan 航炮。'),
 'memorial_202408_c': dict(
   end='2024-08-19T09:00:00Z', end_precision='hour', end_raw='From today until August 19th (09:00 GMT)',
   tasks='美系 III 级及以上飞机打 3 场解锁「伞兵」贴花(活跃度≥70%,无尽对抗/突击模式除外);进度:昵称→成就→节日→US Airborne Forces Day。',
   awards=['「伞兵」贴花'],
   discounts=[{'target':'UH-1C XM-30(美直升机)','item':'8910 金鹰;限时上架;商店位:美国>直升机>高级载具','percent':None}],
   notes='美国空降兵日(1940-08-16 美军首次伞降;1943 起参加意大利/诺曼底/阿登战役);UH-1C XM-30 可挂 M75 榴弹发射器(40mm,230 发/分)/M134 机枪/FFAR 火箭/BGM-71C 导弹/双 30mm XM140。'),
 'memorial_202408_b': dict(
   end='2024-08-19T09:00:00Z', end_precision='hour', end_raw='From today until August 19th (09:00 GMT)',
   tasks='美或英系 III 级及以上载具打 3 场解锁「波兰陆军徽章」贴花(活跃度≥70%);贴花位置:中立国→坦克。',
   awards=['「波兰陆军徽章」贴花'],
   discounts=[{'target':'拉诺夫斯基的 P-47M-1-RE(美系战机)','item':'6090 金鹰;限时返场;波兰飞行员 Witold Lanovski 座机涂装;商店位:美国>航空>高级载具','percent':None}],
   notes='波兰建军节(08-15,华沙阅兵日);P-47M 为高空性能王者,8×12.7mm 勃朗宁,可挂 2×1000 磅炸弹与 HVAR 火箭。'),
 'sale_202408_d': dict(
   end='2024-08-19T07:00:00Z', end_precision='hour', end_raw='From now until August 19th (07:00 GMT)',
   tasks='使用任意狂风家族战机(IDS 1995/IDS MFG/IDS ASSTA1/IDS WTD61/GR.1/F.3/F.3 Late/ADV)打 3 场解锁 50 周年纪念贴花(III 级及以上,活跃度≥70%)。',
   awards=['「狂风首飞 50 周年」纪念贴花'],
   discounts=[{'target':'狂风 IDS WTD 61 礼包(Gaijin 商店)','item':'五折','percent':50}],
   notes='帕那维亚狂风首飞 50 周年(1974-08-14);英国皇家空军 2019 退役其狂风,德国/意大利/沙特仍在役。'),
 'memorial_202405': dict(
   end='2024-05-31T11:00:00Z', end_precision='hour', end_raw='From May 29th until May 31st (11:00 GMT)',
   tasks='瑞典 III 级及以上载具打 3 场解锁「乌普兰团徽章」贴花(活跃度≥70%);追加任务:05-29~06-12 用 SAV 20.12.48 打 3 场得「Wiki approved: SAV 20.12.48」贴花。',
   awards=['「乌普兰团徽章」贴花','「Wiki approved: SAV 20.12.48」贴花(06-12 截止)'],
   discounts=[{'target':'SAV 20.12.48(瑞典坦歼)','item':'1300 金鹰;限时上架;商店位:瑞典>陆军>高级载具','percent':None}],
   notes='瑞典国防军日(1940-05-29 议会批准组建,现员额约 2.2 万、约占陆军半数);SAV 20.12.48 特点为极高射速与穿甲弹,装甲薄弱依赖机动。'),
 'sale_202405_b': dict(
   end='2024-06-03T13:00:00Z', end_precision='hour', end_raw='From May 29th (13:00 GMT) until June 3rd (13:00 GMT)',
   discounts=[{'target':'米兰(法国战机)','item':'9090 金鹰;限时返场;商店位:法国>航空>高级载具','percent':None}],
   notes='米兰(Milan)首飞纪念(1969-05-29,幻影 III 的瑞士订单衍生型,次年定版换装 Atar 9K-50 发动机);机动性出色、极速高,带弹与弹道计算机亦可对地。'),
 'memorial_202405_b': dict(
   end_precision='none', end_raw='From May 24th (11:00 GMT) — 常驻上架,无截止(新闻原文"is here to stay")',
   discounts=[{'target':'百夫长 Mk.5 AVRE(英重坦)','item':'8200 金鹰;自 2024-05-24 11:00 GMT 起常驻上架;商店位:英国>陆军>高级载具','percent':None}],
   notes='皇家工兵团成立纪念日(1716-05-26 乔治一世敕令设立,1855 年定现名,1832 年获座右铭「Ubique/无处不在」);AVRE=装甲工兵车,特色为 165mm 爆破炮+HESH、推土铲、车体/turret 周围 ROMOR-A 爆反与侧裙,5 乘员。'),
 'memorial_202307': dict(
   end='2023-07-10T13:00:00Z', end_precision='hour', end_raw='From July 7th (13:00 GMT) until July 10th (13:00 GMT)',
   tasks='美或英系 III 级及以上载具(活跃度≥70%)打 3 场得「胜利载具:谢尔曼 II」贴花;再用地面载具赢 5 场得「维克斯机枪」3D 挂件;无尽对抗/突击模式除外;进度:昵称→成就→节日→Operation Husky。',
   awards=['「胜利载具:谢尔曼 II」贴花','「维克斯机枪」3D 挂件'],
   notes='哈士基行动 80 周年(1943-07-09 盟军登陆西西里;一个半月后控制全岛、打通地中海航线,墨索里尼随即倒台)。'),
 'special_202206_b': dict(
   end='2022-06-13T14:00:00Z', end_precision='hour', end_raw='From 14:00 GMT on 10th of June until 14:00 GMT on the 13th of June',
   discounts=[{'target':'RN Geniere(意大利 III 级驱逐舰)','item':'金鹰限时返场(2020 年末下架后首次回归);机动优秀、火力与防空强','percent':None}],
   notes='意大利海军日(1918-06-10 意海军击沉奥匈无畏舰「圣伊斯特万」号);官方老新闻格式(2022 前)。'),
 '2013_winter_magic': dict(
   end='2014-01-12', end_precision='day', end_raw='Starting from December 25th 8am GMT to January 12th',
   tasks='每日发布若干自选任务:全完成可得两架绝版高级机 TB-3 与 XF5F(也可只选其一做对应任务);「明日热门」机制:当天最热门战机次日获 24h 研发点乘子;每日折扣由官方论坛玩家投票决定;01-01~01-10 全勤另送 7 天高级账号。',
   awards=['TB-3(绝版高级重型轰炸机)','XF5F(绝版高级战机)','7 天高级账号(01-01~01-10 全任务勤)'],
   discounts=[{'target':'全部 III 级战机(平安夜当日)','item':'-30%;12-24 15:00~12-25 15:00 GMT;德系 La-5FN 与美系 XP-55 除外','percent':30}],
   notes='2013 圣诞「冬日魔法」:玩家自选任务/论坛投票折扣的互动型节日活动;本站活动档案中 2011 年后最早期的记录之一。'),
}

for p in ['E:/ah/wtevents-build/site/data/events.json', 'E:/ah/wtevents-build/data/events_build.json']:
    d = json.load(open(p, encoding='utf-8'))
    hit = 0
    for e in d['events']:
        if e['id'] in E:
            e.update(E[e['id']])
            e['confidence'] = max(e.get('confidence') or 0.5, 0.85)
            hit += 1
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if 'site' in p else None)
    print(p.split('/')[-3], 'enriched', hit)
print('ENRICH_DONE')
