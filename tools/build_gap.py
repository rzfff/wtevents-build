# -*- coding: utf-8 -*-
import json

R = []

def ev(aid, typ, title, start, end, prec, raw, discounts, deadlines, rewards, tasks, subs, notes, conf):
    R.append({
        "aid": aid, "lang": "en", "is_event": True, "type": typ,
        "title": title, "name_en": title, "name_zh": None,
        "start": start, "end": end, "end_precision": prec, "end_raw": raw,
        "discounts": discounts, "deadlines": deadlines, "rewards_text": rewards,
        "tasks": tasks, "sub_events": subs, "notes": notes, "confidence": conf,
    })

# 1) 8602 Pages of History (December): The Heroic Nurse
ev(8602, "special", "Pages of History (December): The Heroic Nurse",
   "2023-12-01", "2023-12-31", "day",
   "From December 1st until December 31st, you'll be offered 8 tasks consecutively.",
   [],
   [{"what": "金鹰直购 Ekaterina Mikhailova 头像(免做任务)截止", "when": "2024-01-03T11:30:00Z"}],
   ["Ekaterina Mikhailova profile icon",
    "per-task trophy: 20-50% RP/SL boosters for 3-10 battles",
    "3-5 universal backup vehicles", "1 day premium account",
    "random ground vehicle camouflage"],
   "12/1-12/31连续8个历史战役任务(随机战斗,Assault除外),每完成一个得奖杯,全部完成获Ekaterina Mikhailova专属头像;头像可金鹰直购至2024/1/3 11:30 GMT。",
   [],
   "Pages of History月度系列12月篇;头像人物为苏联英雄医护兵Ekaterina Mikhailova;金鹰直购窗口跨年至2024/1/3;8个任务窗口12/1-4至12/27-31。",
   0.9)

# 2) 8599 Black Friday Bundle
ev(8599, "sale", "Black Friday Bundle!",
   "2023-11-21T11:00:00Z", "2023-11-28T11:00:00Z", "hour",
   "From November 21st 11:00 GMT until November 28th 11:00 GMT",
   [{"target": "商店礼包", "item": "\"Black Friday 2023\" bundle(A43 Black Prince + P-61A-1 Black Widow + 头衔)", "percent": 50, "note": "45.99→23;仅含载具,不含金鹰与高级账户"}],
   [{"what": "头衔任务(11/21-28登录并取3胜,需已购两车)截止,11/29后统一发放", "when": "2023-11-28T11:00:00Z"}],
   ["Unique title \"In the Black\""],
   "黑五礼包5折:含A43 Black Prince与P-61A-1 Black Widow两辆稀有载具及「In the Black」头衔;11/21-28登录并取3胜(需已分别购过两车)可在11/29后领同款头衔。",
   [],
   "礼包最终价按已拥有载具浮动,需登录商店查看个人价;仅限PC/Mac/Linux;头衔获取任务与礼包同窗口(11/21-28)。",
   0.9)

# 3) 8588 Bundeswehr Day
ev(8588, "special", "Bundeswehr Day: A Decal and Two Tanks to Celebrate!",
   "2023-11-10T14:00:00Z", "2023-11-13T07:00:00Z", "hour",
   "From November 10th (14:00 GMT) until November 13th (07:00 GMT)",
   [],
   [],
   ["Bundeswehr Day decal"],
   "11/10-11/13德系载具打3场(III级+,活跃度≥70%,随机战斗)得「Bundeswehr Day」贴花;同窗口Pz.Sfl.Ic与Panzer IV/70(A)金鹰上架(德国>陆军>高级)。",
   [],
   "德国联邦国防军日(1955/11/12首批士兵宣誓);两车为金鹰限时购非折扣;70%为活跃度门槛。",
   0.92)

# 4) 8589 Chinese Air Force Day
ev(8589, "special", "Chinese Air Force Day: A Decal and the Z-19E Is Here to Stay!",
   "2023-11-10T12:00:00Z", "2023-11-13T07:00:00Z", "hour",
   "From November 10th (12:00 GMT) until November 13th (07:00 GMT)",
   [],
   [],
   ["PLA Air Forces Day decal"],
   "11/10-11/13中系飞机打3场(III级+,活跃度≥70%,随机战斗)得「PLA Air Forces Day」贴花;Z-19E自11/10 12:00 GMT金鹰上架且永久常驻(中国>直升机>高级)。",
   [],
   "解放军空军成立日(1949/11/11);Z-19E为here to stay永久上架,主窗口取贴花任务窗口;70%为活跃度门槛。",
   0.92)

# 5) 8587 Polish Independence Day
ev(8587, "special", "Polish Independence Day: A Decal, Camouflage and Lanovski's P-47 to Celebrate!",
   "2023-11-10T10:00:00Z", "2023-11-13T07:00:00Z", "hour",
   "From November 10th (10:00 GMT) until November 13th (07:00 GMT)",
   [],
   [],
   ["Winged Hussars camouflage for Mi-24V", "Polish cockade decal"],
   "11/10-11/13:Lanovski's P-47M-1-RE金鹰上架(美系>空军>高级);驾Mi-24V打3场(活跃度≥70%)得「Winged Hussars」涂装;英系载具打3场(III级+)得「Polish cockade」贴花。",
   [],
   "波兰独立日(1918/11/11);Winged Hussars涂装为2018年后首次回归;70%均为活跃度门槛非折扣。",
   0.92)

# 6) 8580 Birthday Sale in Gaijin.net Store
ev(8580, "sale", "War Thunder's Birthday Sale in the Gaijin.net Store!",
   "2023-11-06T12:00:00Z", "2023-11-13T12:00:00Z", "hour",
   "From 12:00 GMT on 6th of November until 12:00 GMT on 13th of November",
   [{"target": "Gaijin.net商店", "item": "SU-25K Pack", "percent": 50, "note": "59.99→30;含15天高级+2000金鹰"},
    {"target": "Gaijin.net商店", "item": "XM-1 General Motors Pack", "percent": 50, "note": "59.99→30;含15天高级+2000金鹰+沙漠涂装"},
    {"target": "Gaijin.net商店", "item": "Challenger DS Pack", "percent": 50, "note": "64.99→32.50;含15天高级+2000金鹰"},
    {"target": "Gaijin.net商店", "item": "USS Des Moines Pack", "percent": 50, "note": "64.99→32.50;含30天高级+2000金鹰"},
    {"target": "Gaijin.net商店", "item": "40+款载具礼包整体促销", "percent": 50, "note": "购指定礼包另赠WT Mobile版30天高级"}],
   [],
   [],
   "11周年生日促销:Gaijin.net商店40+款载具礼包全线5折;购指定礼包赠WT Mobile 30天高级;促销结束后Aigle、Duguay-Trouin、M728 CEV、USS Des Moines、Rooivalk五款礼包下架。",
   [],
   "文章日期年份2023;标价货币为美元示例;全平台下架名单在文末注明。",
   0.9)

# 7) 8569 Kings of Battle trophy (market)
ev(8569, "market", "40 New User-Created Camouflages in the \"Kings of Battle\" Trophy!",
   None, None, None, None,
   [],
   [],
   ["Coupons for rare vehicles",
    "40 user-created camouflage coupons (19 ground, 19 aircraft, 1 naval, 1 helicopter)",
    "\"Kings of Battle\" decal coupon",
    "Kings of Battle key (Market, GJN)",
    "3 tank + 1 aircraft camouflages returning from previous trophies"],
   "任意战斗(II级+、活跃度≥50%,Assault PvE除外)有概率掉落「Kings of Battle」奖箱;PC需在Market购GJN钥匙开箱,主机在物品商店用金鹰购买;券可自用或上架出售。",
   [],
   "随Kings of Battle大版本上线的Market奖池文;正文无时间窗,start/end置空;部分钥匙收益分给涂装创作者。",
   0.85)

# 8) 8567 Italian National Unity & Armed Forces Day
ev(8567, "special", "Italian National Unity & Armed Forces Day: The P40 and a Decal to celebrate!",
   "2023-11-03T12:00:00Z", "2023-11-06T07:00:00Z", "hour",
   "From November 3rd (12:00 GMT) until November 6th (07:00 GMT)",
   [],
   [],
   ["Bersaglieri cockade decal"],
   "11/3-11/6意系载具打3场(III级+,活跃度≥70%,随机战斗)得「Bersaglieri cockade」贴花;P40「G.C. Leoncello」同窗口金鹰上架(意大利>陆军>高级)。",
   [],
   "意大利国家统一与武装部队日(1918/11/4奥匈投降);70%为活跃度门槛非折扣。",
   0.92)

# 9) 8557 Dreams Come True: TOG II
ev(8557, "marathon", "Dreams Come True: TOG II",
   "2023-11-01T11:00:00Z", "2023-11-13T11:00:00Z", "hour",
   "From November 1st (11:00 GMT) until November 13th (11:00 GMT): Earn points in battles, unlock stages and receive prizes!",
   [],
   [{"what": "未完成阶段可金鹰补票的最后期限(约)", "when": "2023-11-16"}],
   ["TOG II (Premium Rank III Britain, 6 stages grand prize)",
    "\"T.O.G. No. 2\" decal (1 stage)",
    "special decals (2/4 stages)",
    "\"Death Valley\" / \"Colt–Browning M1895\" decorations (3/5 stages)"],
   "11/1-11/13地面战斗(III级+或活动载具I-II级)赚任务点,每35,000分解锁1阶段共6阶段;阶段每2天更换(11/3/5/7/9/11);6阶得TOG II,1阶得贴花,3/5阶得装饰;11/16前可金鹰补票。",
   [],
   "11周年「Dreams Come True」打点马拉松;任务点倍率按模式与载具最高等级计;活动载具判定以载具卡内活动名为准。",
   0.9)

# 10) 8559 War Thunder's 11th Birthday
ev(8559, "anniversary", "War Thunder's 11th Birthday: Let's Celebrate Together!",
   "2023-11-01T11:00:00Z", "2023-11-13T11:00:00Z", "hour",
   "折扣/纪念贴花/Maus窗口: November 1st (11:00 GMT) — November 6th (11:00 GMT); Dreams Come True: TOG II: November 1st — November 13th (11:00 GMT); Gaijin.net促销: November 6th — November 13th",
   [{"target": "全部改装件、护身符、备份", "item": "游戏内折扣", "percent": 50, "note": "Kings of Battle/Sons of Attila新载具与中队载具除外"},
    {"target": "高级账户", "item": "高级账户折扣", "percent": 50, "note": "游戏内90/365天档,Gaijin.net商店180天档"},
    {"target": "全系金鹰/银狮载具购买价", "item": "载具折扣", "percent": 50, "note": "不含上述例外"},
    {"target": "Gaijin.net商店", "item": "生日促销", "percent": 50, "note": "至多5折,11/6-11/13"}],
   [],
   ["\"War Thunder 11 years\" anniversary decal",
    "TOG II via Dreams Come True event",
    "Maus temporarily researchable for Silver Lions",
    "Anniversary tournament series, 300,000+ Golden Eagles prize fund"],
   "11/1 11:00起庆11周年:全场改装/护身符/备份/高级/载具5折(11/1-6);III级+打1场得纪念贴花;Maus限时开放研发;Dreams Come True肝TOG II至11/13;商店11/6-13促销;周年锦标赛奖池30万+金鹰。",
   [{"name": "游戏内全场50%折扣(改装/护身符/备份/高级/载具)", "start": "2023-11-01T11:00:00Z", "end": "2023-11-06T11:00:00Z"},
    {"name": "「War Thunder 11 years」纪念贴花(III级+打1场)", "start": "2023-11-01T11:00:00Z", "end": "2023-11-06T11:00:00Z"},
    {"name": "Maus限时回归开放研发(需德系V级)", "start": "2023-11-01T11:00:00Z", "end": "2023-11-06T11:00:00Z"},
    {"name": "Dreams Come True: TOG II 打点活动", "start": "2023-11-01T11:00:00Z", "end": "2023-11-13T11:00:00Z"},
    {"name": "Gaijin.net商店生日促销(至多50%)", "start": "2023-11-06", "end": "2023-11-13"},
    {"name": "周年系列锦标赛(总奖池300,000+金鹰)", "start": None, "end": None}],
   "11周年总览文(游戏本体2013/11/1开OBT);游戏内折扣不含Kings of Battle与Sons of Attila新载具及中队载具(含其改装/护身符/备份);主窗口取最长子窗口(至11/13)。",
   0.9)

# 11) 8550 Halloween
ev(8550, "festive", "Halloween in War Thunder!",
   "2023-10-27T12:00:00Z", "2023-11-01T07:00:00Z", "hour",
   "From October 27th (12:00 GMT) until November 1st (7:00 GMT)!",
   [],
   [],
   ["Dead Man's Chest trophy decals: \"Angry Black Cat\" / \"The Bat\" / \"Killer Snail\" / \"Fiery Eye\"",
    "Witch's Cauldron trophy (Halloween decals & decorations)",
    "M18 \"Witch tank\" ground event decals (300 rating)",
    "Po-2 \"Night Witch\" air race decals (300 rating)",
    "Po-2 (USSR) for top-1000 rating in \"Witch Hunt\""],
   "10/27-11/1万圣节:商店复刻亡者宝箱与女巫坩埚奖箱(含新贴花Angry Black Cat与The Bat);M18女巫坦克地面活动与Po-2夜女巫竞速各攒300评分得贴花;女巫狩猎评分前1000名获苏系Po-2。",
   [],
   "Po-2奖励于活动结束后48小时内发放;排行榜约15分钟刷新;「killer snail」等旧贴花随奖箱复刻。",
   0.9)

# 12) 8549 Pages of History (November)
ev(8549, "special", "Pages of History (November)",
   "2023-11-01", "2023-11-30", "day",
   "From November 1st until November 30th, you'll be offered 8 tasks consecutively.",
   [],
   [{"what": "金鹰直购 Jock Campbell 头像(免做任务)截止", "when": "2023-12-03T11:30:00Z"}],
   ["John \"Jock\" Campbell profile icon",
    "per-task trophy: 20-50% RP/SL boosters for 3-10 battles",
    "3-5 universal backup vehicles", "1 day premium account",
    "random ground vehicle camouflage"],
   "11/1-11/30连续8个历史战役任务(随机战斗,Assault除外),每完成一个得奖杯,全部完成获Jock Campbell专属头像;头像可金鹰直购至12/3 11:30 GMT。",
   [],
   "Pages of History月度系列11月篇;头像人物为维多利亚十字勋章获得者John Campbell;8个任务窗口11/1-4至11/27-30。",
   0.9)

# 13) 8551 Turkey 100th Anniversary
ev(8551, "special", "Republic of Turkey 100th Anniversary: A Decal and the T129 ATAK is back!",
   "2023-10-27T10:00:00Z", "2023-10-30T07:00:00Z", "hour",
   "From October 27th (10:00 GMT) until October 30th (07:00 GMT)",
   [],
   [],
   ["\"100 years of the Turkish Republic\" decal"],
   "10/27-10/30任意载具打3场(III级+,活跃度≥70%,随机战斗)得「土耳其共和国100周年」贴花;T129 ATAK自10/27 10:00 GMT金鹰上架且永久常驻(意大利>直升机>高级)。",
   [],
   "土耳其共和国成立100周年(1923/10/29);T129 ATAK返场且here to stay;主窗口取贴花任务窗口;70%为活跃度门槛。",
   0.92)

# 14) 8541 Warbonds for Tropical Storm
ev(8541, "battlepass", "\"Tropical Storm\": Warbonds",
   "2023-10-25", "2024-01-24", "day",
   "The Warbond Shop for the \"Tropical Storm\" Battle Pass season will start on October 25th and will finish on January 24th.",
   [],
   [],
   ["MGB-75 (Britain, Coastal, Rank II)",
    "H-81A-2 (China, Rank II)",
    "Pz.III N (Germany, Rank II)",
    "USS Frank Knox (USA destroyer, Rank III, first time)",
    "P-47D-27 (USSR)",
    "Sherman III/IV (Sweden, Rank III, first time)",
    "\"Capricorn Zodiac\" pinup",
    "2018 warbond decals, decorations, camouflage trophies, player icons (Soviet tankers)",
    "boosters, universal backups, wagers, orders, premium test drives, talismans"],
   "Tropical Storm战令战券商店10/25开放至2024/1/24;III级+玩家用战令等级解锁所得战券兑换6辆金币载具(MGB-75/H-81A-2/Pz.III N/USS Frank Knox/P-47D-27苏/Sherman III/IV)、摩羯pinup、涂装贴花及实用道具。",
   [],
   "战令赛季战券商店公告,结束日跨年+1为2024/1/24;USS Frank Knox与Sherman III/IV为首次进入战券商店;正文仅给日期无时刻。",
   0.85)

# 15) 8540 J35A Draken returns
ev(8540, "special", "J35A Draken returns for the anniversary of its maiden flight!",
   "2023-10-25T10:00:00Z", "2023-10-27T07:00:00Z", "hour",
   "From October 25th (10:00 GMT) until October 27th (07:00 GMT)",
   [],
   [],
   [],
   "10/25-10/27 J35A Draken金鹰限时返场(瑞典>空军>高级),纪念1955/10/25首飞,仅购买窗口无附加任务。",
   [],
   "J35为西欧首款入役超音速喷气机;限时金鹰返场非折扣,无折扣与任务。",
   0.92)

# 16) 8525 UH-1C XM-30 returns
ev(8525, "special", "UH-1C XM-30 returns for the anniversary of its maiden flight!",
   "2023-10-20T12:00:00Z", "2023-10-23T07:00:00Z", "hour",
   "From October 20th (12:00 GMT) until October 23rd (07:00 GMT)",
   [],
   [],
   [],
   "10/20-10/23 UH-1C XM-30金鹰限时返场(美国>直升机>高级),纪念UH-1于1956/10/22首飞,仅购买窗口无附加任务。",
   [],
   "UH-1「Huey」系列产量居全史前三;限时金鹰返场非折扣。",
   0.92)

# 17) 8524 Trafalgar Day
ev(8524, "special", "Trafalgar Day: A Decal and HMCS Haida to celebrate!",
   "2023-10-20T10:00:00Z", "2023-10-23T07:00:00Z", "hour",
   "From October 20th (10:00 GMT) until October 23rd (07:00 GMT)",
   [],
   [],
   ["\"Famous Ships: HMS Victory\" decal"],
   "10/20-10/23英系舰船打3场(III级+,活跃度≥70%,随机战斗)得「Famous Ships: HMS Victory」贴花;HMCS Haida同窗口金鹰返场(英国>远洋舰队>高级)。",
   [],
   "特拉法尔加海战日(1805/10/21,英皇家海军主节日);HMCS Haida为金鹰限时返场非折扣;70%为活跃度门槛。",
   0.92)

# ---- task overrides (<=100 chars) ----
new_tasks = {
8602: "12/1-12/31连续8个历史战役任务(随机战斗,Assault除外),每任务得奖杯,全完成获Ekaterina Mikhailova头像;可金鹰直购至2024/1/3 11:30 GMT。",
8599: "黑五礼包5折:A43 Black Prince+P-61A-1 Black Widow+「In the Black」头衔;11/21-28登录并取3胜(需已购两车)可于11/29后领头衔。",
8588: "11/10-11/13德系载具打3场(III级+,活跃≥70%)得「Bundeswehr Day」贴花;Pz.Sfl.Ic与Panzer IV/70(A)金鹰上架(德国>陆军>高级)。",
8589: "11/10-11/13中系飞机打3场(III级+,活跃≥70%)得「PLA Air Forces Day」贴花;Z-19E自11/10 12:00 GMT起金鹰上架且永久常驻。",
8587: "11/10-11/13:P-47M金鹰上架;驾Mi-24V打3场(活跃≥70%)得「Winged Hussars」涂装;英系打3场(III级+)得「Polish cockade」贴花。",
8580: "11周年商店促销:Gaijin.net商店40+礼包全线5折;购指定礼包赠WT Mobile 30天高级;促销结束后Aigle等5款礼包下架。",
8567: "11/3-11/6意系载具打3场(III级+,活跃≥70%)得「Bersaglieri cockade」贴花;P40「G.C. Leoncello」金鹰上架(意大利>陆军>高级)。",
8557: "11/1-11/13地面战斗(III级+或活动载具I-II级)赚任务点,每35,000分解锁1阶段共6阶,6阶得TOG II;阶段每2天更换;11/16前可金鹰补票。",
8559: "11周年庆:全场改装/护身符/备份/高级/载具5折(11/1-6);III级+打1场得纪念贴花;Maus限时研发;TOG II活动至11/13;商店11/6-13促销。",
8550: "10/27-11/1万圣节:亡者宝箱与女巫坩埚奖箱复刻(新贴花黑猫与蝙蝠);M18女巫坦克/Po-2竞速各攒300评分得贴花;竞速前1000名获Po-2。",
8551: "10/27-10/30任意载具打3场(III级+,活跃≥70%)得「土耳其共和国100周年」贴花;T129 ATAK金鹰上架且永久常驻(意大利>直升机>高级)。",
8541: "战令战券商店10/25-2024/1/24开放;III级+用战券兑换6辆金币车(含首次上架Frank Knox与Sherman III/IV)、摩羯pinup、涂装贴花道具等。",
}
for r in R:
    if r["aid"] in new_tasks:
        r["tasks"] = new_tasks[r["aid"]]

# ---- validate tasks length (<=100) ----
bad = 0
for r in R:
    t = r["tasks"]
    if t and len(t) > 100:
        print("WARN len", r["aid"], len(t))
        bad += 1
assert bad == 0, "tasks still over 100"

out = {"results": R}
with open(r"E:\ah\wtevents-build\data\m3\extract_gap.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("wrote", len(R), "records")
from collections import Counter
print(Counter(r["type"] for r in R))
