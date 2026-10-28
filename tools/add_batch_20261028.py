#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-10-28 增量:9 新事件(国庆/新手包/统一日/Vautour/A-20/约克公爵预购/核升级测试/Mistel 2/万圣节竞速/总决赛掉宝)
+ 3 条 sources 增补(SEAD 回归/长空奥德赛涂装百宝箱/战令 S25 奖券商店 zh 孪生)"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

V = lambda id, zh, en: ({'id': id, 'name_zh': zh, 'name_en': en, 'image': f'/wtapi/assets/images/{id}.png'} if zh else {'id': id, 'name_en': en, 'image': f'/wtapi/assets/images/{id}.png'})
S = lambda en, zh: {'en': [f'https://warthunder.com/en/news/{en}'], 'zh': [f'https://warthunder.com/zh/news/{zh}']}

NEW = [
 dict(id='sale_202610_l', type='sale',
   name_zh='欢度国庆:中国系专属折扣与限时返场活动开启', name_en='Discounts and a Decal for the National Day of the PRC!',
   bp_season=None, start='2026-10-01T09:00:00Z', end='2026-10-08T09:00:00Z', end_precision='hour',
   end_raw='Store: From October 1st (09:00 GMT) until October 8th (09:00 GMT); Golden Eagles: From October 1st (11:00 GMT) until October 8th (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=['国庆专属贴花'],
   discounts=[
     dict(target='中国系礼包×7(Gaijin 商店:96A 原型车/J-7D/JH-7A 原型机/Su-30MKK(中)/ZTZ96B/Z-19E/69-IIa 式)', item='购物车加 1 件 30% 折扣、加 2 件及以上 50% 折扣(需一次结算)', percent=50),
     dict(target='69-IIa 式(中 V 级坦克)', item='5866 金鹰;-30%;仅活动期间可购;商店位:中国>陆军>高级载具', percent=30),
     dict(target='T-62 №545 / JH-7A 原型机', item='限时返场;-30% 金鹰折扣;中国>陆军/航空>高级载具', percent=30)],
   deadlines=[], sub_events=[], tasks=None,
   notes='中华人民共和国国庆(1949-10-01 开国,天安门广场庆典,黄金周);金币返场窗口 10/1-10/8 11:00 GMT 与商店捆绑窗错开 2 小时。', confidence=0.9),

 dict(id='sale_202610_m', type='sale',
   name_zh='全国家新手礼包五折促销', name_en='Starter Pack Sale!',
   bp_season=None, start='2026-10-01T11:00:00Z', end='2026-10-08T11:00:00Z', end_precision='hour',
   end_raw='From October 1st (11:00 GMT) until October 8th (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[],
   discounts=[dict(target='全国家新手礼包(Gaijin 商店)', item='含载具+银狮+高级账号时长;-50%;适合开新国家线', percent=50)],
   deadlines=[], sub_events=[], tasks=None,
   notes='与国庆促销同窗的例行新手礼包促销。', confidence=0.9),

 dict(id='sale_202610_n', type='sale',
   name_zh='德国统一日:贴花、折扣与稀有载具限时返场', name_en='A Decal, Discounts and Rare Vehicles for German Unity Day!',
   bp_season=None, start='2026-10-02T11:00:00Z', end='2026-10-05T11:00:00Z', end_precision='hour',
   end_raw='From October 2nd (11:00 GMT) until October 5th (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=['德国统一日专属贴花'],
   discounts=[
     dict(target='「众力一国」捆绑包(侦察兵礼包+Z-20 卡尔·加尔斯特礼包+Bf 109Z 双子座礼包)', item='74.97→37.49 美元;-50%', percent=50),
     dict(target='「德国统一日 2026」捆绑包(阿尔法喷气 A 礼包+豹式礼包)', item='120→59.99 美元;-50%', percent=50),
     dict(target='Pz.Sfl.Ic(德 II 级)/Bf 109 Z-1(德 IV 级)/Z20 卡尔·加尔斯特(德 III 级)', item='700/2086/3416 金鹰;-30%;仅活动期间可购;德国>航空/陆军/远洋舰队>高级载具', percent=30)],
   deadlines=[], sub_events=[], tasks=None,
   notes='德国统一日(1990-10-03 两德统一);商店捆绑与金币返场同窗。', confidence=0.9),

 dict(id='sale_202610_o', type='sale',
   name_zh='秃鹰 IIN 首飞纪念日限时折扣', name_en="Vautour IIN Available with a Discount for the Anniversary of the Vautour II's First Flight!",
   bp_season=None, start='2026-10-16T09:00:00Z', end='2026-10-19T09:00:00Z', end_precision='hour',
   end_raw='From October 16th (09:00 GMT) until October 19th (09:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[],
   discounts=[dict(target='秃鹰 IIN(法 VI 级战机)', item='5992 金鹰;-30%;仅本次促销期间可购;商店位:法国>航空>高级载具', percent=30)],
   deadlines=[], sub_events=[], tasks=None,
   notes='SO.4050 秃鹰 II 首飞纪念(1952-10-16,战后早期法国喷气机,法军 1958-1979 服役,总产近 150 架);IIN 为双座全天候截击型,曾随以色列空军参战;载弹量达 4400kg。', confidence=0.9),

 dict(id='sale_202610_p', type='sale',
   name_zh='A-20 浩劫首飞纪念日:英国版限时返售', name_en="The British A-20 is Available with a Discount To celebrate the A-20's First Flight!",
   bp_season=None, start='2026-10-26T09:00:00Z', end='2026-10-29T09:00:00Z', end_precision='hour',
   end_raw='From October 26th (09:00 GMT) until October 29th (09:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[],
   discounts=[dict(target='浩劫 Mk I(英 II 级攻击机)', item='490 金鹰;-30%;仅本次促销期间可购;商店位:英国>航空>高级载具', percent=30)],
   deadlines=[], sub_events=[], tasks=None,
   notes='道格拉斯 A-20 原型机首飞纪念(1938-10-26);曾服役法/英/美/苏空军,苏联经租借法案大量接收;英国版 Mk I 挂 4×500 磅炸弹。', confidence=0.9),

 dict(id='sale_202610_q', type='sale',
   name_zh='约克公爵号战列舰礼包开启预售', name_en='Pre-order: HMS Duke of York',
   bp_season=None, start='2026-10-19T11:00:00Z', end=None, end_precision='none',
   end_raw='预购开放至下个大版本上线(时间未公布)',
   dm_event=None, vehicles=[V('gb_duke_of_york', '约克公爵号', 'HMS Duke of York')] if False else [],
   awards=['预购专属:「国王的演讲」称号、「约克的白玫瑰」贴花、约克旗(大版本上线后发放)'],
   discounts=[dict(target='约克公爵号礼包(Gaijin 商店,预购)', item='含约克公爵号(英 VI 级高级战列舰)+30 天高级+3000 金鹰;79.99 美元(预购价)', percent=None)],
   deadlines=[], sub_events=[], tasks=None,
   notes='「沙恩霍斯特杀手」、本土舰队未来旗舰;1943 年形态:10 门 356mm 主炮/30 门 20mm 自动炮/133mm 副炮配 HE-VT 近炸弹;防护优秀、机动平平;舰上吉祥物猫「威士忌」。', confidence=0.85),

 dict(id='special_202610_c', type='special',
   name_zh='核战冲突模式拓展至全真:测试活动开启', name_en='Testing Nuclear Escalation in Simulator Battles!',
   bp_season=None, start='2026-10-27T13:00:00Z', end='2026-10-29T13:00:00Z', end_precision='hour',
   end_raw='From October 27th (13:00 GMT) until October 29th (13:00 GMT)',
   dm_event=None, vehicles=[],
   awards=[],
   discounts=[],
   deadlines=[], sub_events=[], tasks=None,
   notes='全真难度版核战冲突测试:热带海岸/东南城市图,载具按 BR 时代分组(8.7-9.7/10.0-11.0/11.3-13.0/13.3+),收益按持久对峙口径结算;入口=活动与锦标赛>核战冲突。10 月上旬曾测过新版东南渔湾地图(special_202610)。', confidence=0.9),

 dict(id='special_202610_d', type='special',
   name_zh='梦想成真:槲寄生 2(Mistel 2)复合机活动', name_en='Dreams Come True: Mistel 2',
   bp_season=None, start='2026-10-28T11:00:00Z', end='2026-11-11T11:00:00Z', end_precision='hour',
   end_raw='From October 28th (11:00 GMT) until November 11th (11:00 GMT)',
   dm_event=None,
   vehicles=[V('fw_190a_8_mistel', '槲寄生 2', 'Mistel 2'), V('ju_88g_1_mistel', '槲寄生 2', 'Mistel 2')],
   awards=['「父子」贴花', '「抱着炸弹的孩子」贴花', '「槲寄生」头像框', '奖励箱(5-10 万银狮/加成器/赌注与指令/备用载具 1-3 个/随机涂装/1 天高级)'],
   discounts=[],
   deadlines=[], sub_events=[],
   tasks='空战(街机/历史/全真,III 级及以上)攒任务点,每 35000 分解锁一阶奖励,需手动领取;I/II 级活动载具也可参与积分(有倍率,详见任务说明)。',
   notes='槲寄生(Mistel)=Fw 190 A-8(拆武备减重)背负 Ju 88 G-1(机头改锥形装药巨型炸弹)的复合体,绰号「父子」;飞行员驾驶战斗机导向目标后释放,轰炸机由自动驾驶直飞目标。德 III 级高级轰炸机;两台组成载具(上下件)随 2.59.0.90 加入 wtapi 数据(3387→3389)。', confidence=0.9),

 dict(id='special_202610_e', type='special',
   name_zh='观看 2026 总决赛赢取三色烟等掉宝好礼', name_en='Watch the 2026 Grand Finals and Earn Tricolor Smoke & More Twitch Drops!',
   bp_season=None, start='2026-10-24T13:50:00Z', end='2026-11-11T23:59:00Z', end_precision='day',
   end_raw='掉宝窗口:10/24-25、10/31-11/1、11/2-4、11/6、11/7-8、11/9-11(各日不同起始时刻;周一至周三英文频道有重播)',
   dm_event=None, vehicles=[],
   awards=['三色烟等 Twitch 掉宝(含两款载具特殊涂装)'],
   discounts=[],
   deadlines=[], sub_events=[], tasks=None,
   notes='WTCS 2026 总决赛(奖金池 15000 美元,八强:DODEC/Voyager/AVReS/Jinx/FIVESTICKS/INVICTUS/MRCLS/LEET);英德法俄波五语 Twitch 直播+YouTube 回放;观看官方频道累计时长领掉宝。', confidence=0.85),

 dict(id='festive_202610_b', type='festive',
   name_zh='骇人万圣节:亡命竞速赛回归', name_en='Spooky Races Return for Halloween!',
   bp_season=None, start='2026-10-28T11:00:00Z', end='2026-11-01T11:00:00Z', end_precision='hour',
   end_raw='Races: From October 28th (11:00 GMT) until November 1st (11:00 GMT) — 注意:竞速开赛较原计划推迟 24 小时;Dead Man\'s Chest / Witch\'s Cauldron: From October 27th (11:00 GMT) until November 1st (11:00 GMT)',
   dm_event=None, vehicles=[],
   awards=['「阴森之地」头像框(地面赛 750 评分)', '「绿幽灵」中队徽章贴花(空赛 750 评分)', '「Boo!」贴花(任意 III 级以上载具 3000 任务点,活跃度≥70%)'],
   discounts=[],
   deadlines=[dict(what='亡者宝箱(往季万圣节贴花)与女巫大锅(往季万圣节挂件)奖箱返场上架游戏内商店', when='2026-10-27T11:00:00Z')],
   sub_events=[], tasks=None,
   notes='万圣节主题竞速:地面赛「穿越黑暗森林」(500 评分得女巫大锅奖箱挂件)与空赛「女巫狩猎」(300 评分得亡者宝箱贴花);重复物品折抵为奖箱(2-10 万银狮等)。', confidence=0.9),
]

# —— sources 增补(已录事件补挂新闻源,清理哨兵积压)——
ENRICH = {
 'special_202610_b': ('10263', '2820'),
 'market_202609_b': ('10244', '2804'),
 'battlepass_202610': (None, '2823'),
}

# —— NEW 记录挂新闻源(短 id 形式,与既有记录一致)——
SRC = {
 'sale_202610_l': ('10246', '2806'),
 'sale_202610_m': ('10247', '2809'),
 'sale_202610_n': ('10252', '2810'),
 'sale_202610_o': ('10262', '2819'),
 'sale_202610_p': ('10281', '2840'),
 'sale_202610_q': ('10260', '2821'),
 'special_202610_c': ('10283', '2845'),
 'special_202610_d': ('10282', '2841'),
 'special_202610_e': ('10275', '2835'),
 'festive_202610_b': ('10286', '2843'),
}
for ev in NEW:
    en, zh = SRC[ev['id']]
    ev['sources'] = {'en': [f'https://warthunder.com/en/news/{en}'], 'zh': [f'https://warthunder.com/zh/news/{zh}']}

for p in ['E:/ah/wtevents-build/site/data/events.json', 'E:/ah/wtevents-build/data/events_build.json']:
    d = json.load(open(p, encoding='utf-8'))
    existing_ids = {e['id'] for e in d['events']}
    for ev in NEW:
        if ev['id'] in existing_ids:
            print(f'WARNING: {ev["id"]} already exists, will overwrite')
    d['events'] = [e for e in d['events'] if e['id'] not in {x['id'] for x in NEW}] + NEW
    # sources 增补
    for eid, (en_slug, zh_slug) in ENRICH.items():
        for e in d['events']:
            if e['id'] == eid:
                src = e.setdefault('sources', {'en': [], 'zh': []})
                if en_slug and f'warthunder.com/en/news/{en_slug.split("-")[0]}' not in str(src.get('en')):
                    src.setdefault('en', []).append(f'https://warthunder.com/en/news/{en_slug}')
                if zh_slug and not any(zh_slug.split('-')[0] in str(u) for u in src.get('zh', [])):
                    src.setdefault('zh', []).append(f'https://warthunder.com/zh/news/{zh_slug}')
                print(f'ENRICH {eid}: en={len(src.get("en",[]))} zh={len(src.get("zh",[]))}')
    d['events'].sort(key=lambda x: (x.get('start') or x.get('end') or '0000'), reverse=True)
    from collections import Counter
    d['counts'] = {'events': len(d['events']), 'by_type': dict(Counter(e['type'] for e in d['events'])),
                   'with_discounts': sum(1 for e in d['events'] if e.get('discounts'))}
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if 'site' in p else None)
    print(p, 'total', d['counts']['events'], dict(sorted(d['counts']['by_type'].items())))
print('BATCH_DONE')
