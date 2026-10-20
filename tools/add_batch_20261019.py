#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-10-19 积压批量入册:8 事件(国庆/新手包/德国统一日/长空奥德赛百宝箱/秃鹰IIN/SEAD/约克公爵预购/战令S25)。
直构模式(不走 apply_gap——本批窗口互相 ≤10 天且标题共享 discounts/decal,启发式折叠必误伤)。
来源:官方新闻 en_10244/10246/10247/10252/10260/10262/10263/10265 + zh 2804/2806/2809/2810/2819/2820/2821/2823(text6/text7)。幂等:按 id 覆盖。"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

V = lambda id, zh, en: ({'id': id, 'name_zh': zh, 'name_en': en, 'image': f'/wtapi/assets/images/{id}.png'} if zh else {'id': id, 'name_en': en, 'image': f'/wtapi/assets/images/{id}.png'})

# 修复项:2026-10-19 首跑误顶掉的旧条目(WTCS Trophy VI),从线上 925 版拉回原样保留
_OLD_MARKET = [e for e in json.load(open('E:/ah/wtevents-build/data/events_live_925.json', encoding='utf-8'))['events'] if e['id'] == 'market_202609']

NEW = [
 dict(id='sale_202610_b', type='sale',
   name_zh='欢度国庆,专属折扣与载具返售活动盛大开启', name_en='Discounts and a Decal for the National Day of the PRC!',
   bp_season=None, start='2026-10-01T09:00:00Z', end='2026-10-08T09:00:00Z', end_precision='hour',
   end_raw='From October 1st (09:00 GMT) until October 8th (09:00 GMT)',
   dm_event=None,
   vehicles=[V('cn_type_69_2a','69-IIA','Type 69-IIa'), V('cn_t_62','␗T-62 (“545”号)','T-62 №545'),
             V('jh_7a','歼轰-7A','JH-7A Prototype'), V('su_30mkk','␗苏-30MKK','Su-30MKK (China)'),
             V('cn_ztz_96a_prot','ZTZ96A 原型车','Type 96A Prototype'), V('j_7d','歼-7D','J-7D'),
             V('cn_ztz_96b','ZTZ96B','ZTZ96B'), V('z_19e','直-19E','Z-19E')],
   awards=['「国庆节」奖杯(任务:中系 III 级及以上载具攒 3000 任务分;内含四款贴花之一:华表/中华人民共和国国徽/国庆 2024/国庆 2025;集齐后改开强化器/备用载具奖箱)'],
   discounts=[
     dict(target='Gaijin 商店·中系礼包自组捆搭', item='七款礼包(Type 96A 原型/J-7D/JH-7A 原型/Su-30MKK/ZTZ96B/Z-19E/69-IIa):购物车加 1 款 75 折、加 2 款及以上 5 折,须一次结算;单品单独购买亦享 75 折;不含金鹰与高级账号', percent=50),
     dict(target='69-IIa(中 V 级)/T-62 545 号(中 VI 级)/JH-7A 原型(中系)', item='游戏内金鹰购:-30%;69-IIa 5866 金鹰、T-62 545 号 6111 金鹰;仅活动期间可购;商店位:中国>陆军/航空>高级载具', percent=30)],
   deadlines=[], sub_events=[],
   tasks='中系 III 级及以上载具战斗攒 3000 任务分开「国庆节」奖箱(随机四款国庆贴花之一,集齐后转强化器/备用);完成后需手动领奖。',
   notes='中华人民共和国国庆纪念日(1949-10-01 成立,天安门广场庆典,黄金周);T-62 545 号=1969 年珍宝岛战斗中被击俘获的苏制 T-62,后经中国工程师研究。', confidence=0.9),

 dict(id='sale_202610_c', type='sale',
   name_zh='Gaijin 商城新手礼包特惠来袭', name_en='Starter Pack Sale!',
   bp_season=None, start='2026-10-01T11:00:00Z', end='2026-10-08T11:00:00Z', end_precision='hour',
   end_raw='From October 1st (11:00 GMT) until October 8th (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[],
   discounts=[dict(target='全系新手礼包(Gaijin 商店)', item='全部国家的新手礼包五折;礼包内含载具+银狮+高级账号时长,适合开新系别提速', percent=50)],
   deadlines=[], sub_events=[], tasks=None,
   notes='与国庆促销同窗的常规新手礼包促销。', confidence=0.9),

 dict(id='sale_202610_d', type='sale',
   name_zh='纪念德国统一日贴花与折扣活动开启', name_en='A Decal, Discounts and Rare Vehicles for German Unity Day!',
   bp_season=None, start='2026-10-02T11:00:00Z', end='2026-10-05T11:00:00Z', end_precision='hour',
   end_raw='From October 2nd (11:00 GMT) until October 5th (11:00 GMT)',
   dm_event=None,
   vehicles=[V('bf-109z','Bf 109 Z','Bf 109 Z-1'), V('germ_destroyer_class1936_z20_karlgalster', None, 'Z20 Karl Galster')],
   awards=['「德国统一日」奖箱(任务:德系 III 级及以上载具攒 3000 任务分;内含四款贴花之一:德国统一日/德国统一/两德统一纪念日/联邦之鹰;集齐后改开强化器/备用;突击模式除外,需手动领奖)'],
   discounts=[
     dict(target='「众力一国」礼包(Gaijin 商店)', item='含侦察兵礼包+Z-20 卡尔·加尔斯特礼包+Bf 109Z 双机身礼包;74.97→37.49 美元', percent=50),
     dict(target='「德国统一日 2026」礼包(Gaijin 商店)', item='含阿尔法喷气 A 礼包+豹 1 礼包;120→59.99 美元', percent=50),
     dict(target='Pz.Sfl.Ic(德 II 级)/Bf 109 Z-1(德 IV 级)/Z20 卡尔·加尔斯特(德系)', item='游戏内金鹰购:-30%;Bf 109 Z-1 2086 金鹰、Pz.Sfl.Ic 700 金鹰;商店位:德国>航空/陆军/远洋舰队>高级载具', percent=30)],
   deadlines=[], sub_events=[],
   tasks='德系 III 级及以上载具战斗攒 3000 任务分开「德国统一日」奖箱(随机四款贴花之一);进度:昵称→成就→节日→German Unity Day。',
   notes='德国统一日(1990-10-03 两德统一);Bf 109 Z-1=双机身试验机(4×30mm MK 108,适合猎轰炸机);Pz.Sfl.Ic=VK 9.01 底盘试验轻歼(50mm Pak 38)。', confidence=0.9),

 dict(id='market_202609_b', type='market',
   name_zh='40 款社区创作涂装随「长空奥德赛」百宝箱加入游戏', name_en='40 New User-Created Camouflages in the Sky Odyssey Trophy!',
   bp_season=None, start='2026-09-30T11:00:00Z', end=None, end_precision='none',
   end_raw='百宝箱长期在役(随下一期替换),无固定截止',
   dm_event=None, vehicles=[],
   awards=['「长空奥德赛」贴花(箱内掉落)','稀有载具兑换券(箱内掉落)'],
   discounts=[],
   deadlines=[], sub_events=[],
   tasks='开箱途径:①II 级及以上载具、活跃度≥50% 的战斗后概率掉落(突击模式除外),PC 玩家需在市场上用 GJN 购「长空奥德赛」钥匙开启(部分销售收入按比例分成给箱内涂装作者);②主机玩家可在游戏内物品商店用金鹰直接购买开启。',
   notes='长空奥德赛大版本主题百宝箱:40 款 WT Live 社区作者涂装(陆 18/空 18/海 2/直升 2)+稀有载具兑换券+专属贴花;希腊载具与新活动载具涂装为主;每售一钥分成给创作者。', confidence=0.9),

 dict(id='sale_202610_e', type='sale',
   name_zh='SO.4050 秃鹰 II 首飞纪念日,游戏内 IIN 型开启限时折扣', name_en="Vautour IIN Available with a Discount for the Anniversary of the Vautour II's First Flight!",
   bp_season=None, start='2026-10-16T09:00:00Z', end='2026-10-19T09:00:00Z', end_precision='hour',
   end_raw='From October 16th (09:00 GMT) until October 19th (09:00 GMT)',
   dm_event=None,
   vehicles=[V('so_4050_vautour_2n','秃鹰 IIN(C)','Vautour IIN')],
   awards=[],
   discounts=[dict(target='秃鹰 IIN(法国战机)', item='5992 金鹰;-30%;商店位:法国>航空>高级载具', percent=30)],
   deadlines=[], sub_events=[], tasks=None,
   notes='SO.4050 秃鹰 II 首飞纪念(1952-10-16,法国战后早期喷气机,1958-1979 服役近 150 架);IIN=双座全天候截击型,曾随以色列空军参战;轰炸取向:载弹高达 4400kg(250-400kg 炸弹/SNEB 23/AS-30 火箭),自卫 4×30mm DEFA 551+AA-20 空空导弹。', confidence=0.9),

 dict(id='special_202610_b', type='special',
   name_zh='非对称对抗:防空压制活动回归', name_en='SEAD: Asymmetrical Battle Returns!',
   bp_season=None, start='2026-10-16T11:00:00Z', end='2026-10-19T11:00:00Z', end_precision='hour',
   end_raw='From October 16th (11:00 GMT) until October 19th (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[],
   discounts=[],
   deadlines=[], sub_events=[],
   tasks='机库→活动与锦标赛→Suppression of Enemy Air Defenses;拥有 V 级及以上战机即可参加,载具系统分配无需购买(出击耗银狮,任务结束未被击毁或从安全退出区离场则按机体状态退还);每玩家 3 次重生;无标记模式(仅敌机悬停于己方出生点上空时可见);参与可赚研发点与银狮。',
   notes='非对称对抗(纪念 1965-10-17 越战「铁手行动」——战争史上首次压制敌方防空作战,系列持续至 1973):进攻方(F-4E 鬼怪 II[火箭/炸弹+空空导弹]/AH-1F[ATGM+火箭])摧毁全部 S-75 阵地;防守方(米格-21bis)协同 AI S-75 与 ZSU-23-4 石勒喀防守;反辐射导弹经内部测试过强不开放(核战冲突模式仍可用)。', confidence=0.9),

 dict(id='sale_202610_f', type='sale',
   name_zh='约克公爵号战列舰开放预购', name_en='Pre-order: HMS Duke of York',
   bp_season=None, start='2026-10-19T11:00:00Z', end=None, end_precision='none',
   end_raw='预购开放至下个大版本上线(时间未公布)',
   dm_event=None, vehicles=[],
   awards=['预购专属:「国王的演讲」称号、「白玫瑰」贴花、约克旗(大版本上线后发放)'],
   discounts=[dict(target='约克公爵号礼包(Gaijin 商店,预购)', item='含约克公爵号(英 VI 级战列舰)+30 天高级+3000 金鹰+三项预购专属;79.99 美元(无折扣,预购价)', percent=None)],
   deadlines=[], sub_events=[], tasks=None,
   notes='英系第二艘高级顶级战列舰(乔治五世级,1943 年状态:30 门 20mm 机炮);定位生存防御型:381mm 主装甲带/152mm 装甲甲板/10 门 356mm 主炮+133mm 副炮可发射 HE-VT 近炸弹(远程防空利器),机动平庸;史实:1943-12 北角海战重创沙恩霍斯特号(命中至少 10 发主炮弹)。随下个大版本实装。', confidence=0.85),

 dict(id='battlepass_202610', type='battlepass',
   name_zh='战斗通行证第 25 季「钢铁狂怒」', name_en='Battle Pass Season 25: Steel Fury and Its Warbond Shop!',
   bp_season=25, start='2026-10-21T12:00:00Z', end='2027-01-20T12:00:00Z', end_precision='hour',
   end_raw='Beginning on: October 21st (12:00 GMT); Ending on: January 20th (12:00 GMT)',
   dm_event=None, vehicles=[],
   awards=['S-706(德 III 级鱼雷艇,高级)','猎豹 G2 坦克歼击车(德 IV 级,高级)','「克蕾曼汀/格特鲁德/艾莉卡/布伦希尔德」德系女名涂写贴花×4','猎豹 G2 资料背景','弹药箱/PWK 42 LP/Puppchen 挂件','105/125 级升级券×2(两张可换下一季通行证,或使新车可交易)'],
   discounts=[],
   deadlines=[dict(what='开季 28 天后可用金鹰购买进度点', when='2026-11-18T12:00:00Z')],
   sub_events=[],
   tasks='通行证 2000 金鹰(进阶版 2500 金鹰含 150 进度点);升级=攒进度点(每级 10 点):登录 1-5 点/每日任务 2-5 点/挑战任务 30 点(每周解锁,另 3 个随等级解锁);奖券商店可用战令奖券兑换 Z4 措尔纳号驱逐舰(防空特化)/FR-1 火球(美混动战机)/涂装箱/德坦克兵头像奖箱/「1944 年 10 月小姐」贴花;战斗奖箱可开出往季载具(ORP 加兰/底特律号/刺猬马蒂尔达/Ro.57 四臂)。',
   notes='第 25 季主题=德国;S-706=德国 Schnellboote 末代鱼雷艇(近 80km/h,4 具鱼雷管,有望成游戏最佳雷艇之一);猎豹 G2=猎豹歼击车第二生产型(88mm 同虎王炮+Em 0.9m R 测距仪,1944 年巴拉顿湖与阿登役实装史实)。', confidence=0.9),
]

for p in ['E:/ah/wtevents-build/site/data/events.json', 'E:/ah/wtevents-build/data/events_build.json']:
    d = json.load(open(p, encoding='utf-8'))
    _drop = {x['id'] for x in NEW} | {'market_202609'}  # 同时清掉首跑误写的 Sky Odyssey 顶替版
    d['events'] = [e for e in d['events'] if e['id'] not in _drop] + NEW + _OLD_MARKET
    d['events'].sort(key=lambda x: (x.get('start') or x.get('end') or '0000'), reverse=True)
    from collections import Counter
    d['counts'] = {'events': len(d['events']), 'by_type': dict(Counter(e['type'] for e in d['events'])),
                   'with_discounts': sum(1 for e in d['events'] if e.get('discounts'))}
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if 'site' in p else None)
    print(p.split('/')[-3], 'total', d['counts']['events'], d['counts']['by_type'].get('sale'), d['counts']['by_type'].get('battlepass'))
print('BATCH_DONE')
