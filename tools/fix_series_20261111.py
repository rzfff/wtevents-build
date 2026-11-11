#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-11-11 史海拾遗系列+英国武装部队纪念日·结构修复批(M4 收尾加餐,站长令「遗留的都做了」)。
病根:M2 合并期把「月度史海+下月预告/邻事件」粘成合成体。本批:
  改 4:special_202502(名偷三月→二月归位)/marathon_202505(名偷英国+吞六月→五月归位)/
       marathon_202512(无名无zh→十二月补全,1月篇外移)/sale_202512_c(名偷十二月史海→冬促归位)
  建 5:special_202503 三月(整月缺失)/marathon_202506 六月(被吞)/special_202506_c 英国2025/
       special_202606_c 英国2026(整年缺)/special_202601 一月2026(篇从十二月外移)
素材:en_9349/9388/9481/9517/9814/9874/9586/10114 + zh_1942/1977/2070/2106/2175/2393/2440/2447/2677 全文(deeparts*.txt)
"""
import json, io, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
P = r'E:\ah\wtevents-build\site\data\events.json'
d = json.load(io.open(P, encoding='utf-8'))
ev = d['events']
by = {e['id']: e for e in ev}
exist = set(by)

TROPHY = ['20-50% 研发加成卡(3-10 场)', '20-50% 银狮加成卡(3-10 场)', '3-5 份备用载具兑换卡', '1 天高级账户', '随机地面载具涂装']

# ---------- A. special_202502:二月归位 ----------
e = by['special_202502']
e['name_zh'] = '史海拾遗·二月:五星大帅'
e['awards'] = TROPHY[:4] + ['专属玩家头像:道格拉斯·麦克阿瑟(五星大帅,完成全部 8 任务;金鹰直购截止 2025-03-03 11:30 GMT)']
e['tasks'] = ('2 月 1 日至 28 日连续开放 8 个任务(每 3-4 天一个,北京时间 19:00 开 19:30 关);随机战斗完成'
              '(突击模式除外);每任务给作战物资箱,全部完成得专属头像')
e['notes'] = ('月度历史任务活动;2 月战役含马尼拉战役(1945)/阿德敏箱战役(1942)/蓝山 719 行动(1971)/'
              '地狱犬行动(沙恩霍斯特号海峡冲刺,1942)等;头像=麦克阿瑟(EN 名 The Big Chief)。'
              '⚠ 2026-11-11 修复:原名被三月预告文偷占,本条已归位;三月内容拆出为 special_202503')
e['sources']['en'] = ['https://warthunder.com/en/news/9349']
e['sources']['zh'] = ['https://warthunder.com/zh/news/1942']

# ---------- B. special_202503:三月(新建) ----------
n3 = {
 'id': 'special_202503', 'type': 'special',
 'name_zh': '史海拾遗·三月:皇家王牌', 'name_en': 'Pages of History (March): The Royal Ace',
 'start': '2025-03-01', 'end': '2025-03-31', 'end_precision': 'day',
 'end_raw': 'From March 1st until March 31st',
 'dm_event': None, 'vehicles': [],
 'awards': TROPHY[:4] + ['专属玩家头像:詹姆斯·埃德加·约翰逊(皇家空军王牌,完成全部 8 任务;金鹰直购截止 2025-04-03 11:30 GMT)'],
 'discounts': [], 'deadlines': [],
 'tasks': '3 月 1 日至 31 日连续开放 8 个任务(每 3-4 天一个);随机战斗完成(突击模式除外);全部完成得专属头像',
 'notes': ('月度历史任务活动;3 月战役:勒热夫-维亚济马攻势(1943)/喷火战斗机首飞(1936)/普斯科夫攻势(1944)/'
           '萨尔-普法尔茨攻势(1945)/维也纳攻势(1945)/第二次锡尔特湾海战(1942)/纳杰夫战役(2003)/'
           '马塔潘角海战(1941);头像=约翰逊(喷火王牌,EN 名 The Royal Ace)。2026-11-11 补建:原被 M2 合并吞进二月条目'),
 'sources': {'en': ['https://warthunder.com/en/news/9388'], 'zh': ['https://warthunder.com/zh/news/1977']},
}

# ---------- C. marathon_202505:五月归位 ----------
e = by['marathon_202505']
e['name_zh'] = '史海拾遗·五月:胜利之路'
e['awards'] = TROPHY[:4] + ['专属玩家头像:斯捷潘·涅乌斯特罗耶夫(国会大厦突击营长,完成全部 8 任务;金鹰直购截止 2025-06-03 11:30 GMT)']
e['tasks'] = ('5 月 1 日至 31 日连续开放 8 个任务(每 3-4 天一个,北京时间 19:00 开 19:30 关);随机战斗完成'
              '(PVE 以外任意匹配模式);每任务给作战物资箱,全部完成得专属头像')
e['notes'] = ('月度历史任务活动;5 月战役:婆罗洲行动·塔拉坎战役(1945)/马达加斯加战役(1942)/欧洲胜利日(80 周年)/'
              '权杖行动(1944)/突尼斯战役收官(1943)/克里特岛战役(1941)/森格尔防线(1944)/F-4 鬼怪首飞(1958);'
              '头像=涅乌斯特罗耶夫(EN 名 Road to the Reichstag,胜利之路)。'
              '⚠ 2026-11-11 修复:原被灌英国武装部队纪念日标题+吞并六月内容,均已拆出')
e['deadlines'] = [{'what': '金鹰直购本期头像(免做任务)截止', 'when': '2025-06-03T11:30:00Z'}]
e['sources']['en'] = ['https://warthunder.com/en/news/9481']
e['sources']['zh'] = ['https://warthunder.com/zh/news/2070']

# ---------- D. marathon_202506:六月(新建,自五月拆出) ----------
n6 = {
 'id': 'marathon_202506', 'type': 'memorial',
 'name_zh': '史海拾遗·六月:荒原骑兵', 'name_en': 'Pages of History (June): Rough Rider',
 'start': '2025-06-01', 'end': '2025-06-30', 'end_precision': 'day',
 'end_raw': 'From June 1st until June 30th',
 'dm_event': None, 'vehicles': [],
 'awards': TROPHY[:4] + ['专属玩家头像:西奥多·罗斯福三世(诺曼底登陆最年长者,完成全部 8 任务;金鹰直购截止 2025-07-03 11:30 GMT)'],
 'discounts': [], 'deadlines': [],
 'tasks': '6 月 1 日至 30 日连续开放 8 个任务(每 3-4 天一个);随机战斗完成(突击模式除外);全部完成得专属头像',
 'notes': ('月度历史任务活动;6 月战役:中途岛战役(1942)/诺曼底登陆 D-Day(1944)/维堡-彼得罗扎沃茨克攻势(1944)/'
           '波卡基村之战(1944)/战斧行动(1941)/菲律宾海海战(1944)/拉塞尼艾之战(1941)/蓝色行动(1942);'
           '头像=老罗斯福之子罗斯福三世(EN 名 Rough Rider,荒原骑兵)。2026-11-11 补建:原被 M2 合并吞进五月条目'),
 'sources': {'en': ['https://warthunder.com/en/news/9517'], 'zh': ['https://warthunder.com/zh/news/2106']},
}

# ---------- E. marathon_202512:十二月补全 ----------
e = by['marathon_202512']
e['name_zh'] = '史海拾遗·十二月:阿登英雄'
e['awards'] = TROPHY[:4] + ['专属玩家头像:弗朗西斯·卡罗伊(阿登战役老兵勋章获得者,完成全部 8 任务;金鹰直购截止 2026-01-03 11:30 GMT)']
e['tasks'] = '12 月 1 日至 31 日连续开放 8 个任务(每 3-4 天一个);随机战斗完成(突击模式除外);全部完成得专属头像'
e['notes'] = ('月度历史任务活动;12 月战役:伯恩哈特防线(1943)/西奥之战(1943)/罗盘行动(1940)/冬季风暴行动(1942)/'
             '阿登反攻(1944)/库尔斯克-奥博扬攻势(1943)/长沙之战(1941)等;头像=卡罗伊(EN 名 The Hero of the Ardennes)。'
             '⚠ 2026-11-11 修复:原名空缺且中文预告文被冬促条目偷占,均已归位;一月篇(9874)外移至 special_202601')
e['deadlines'] = [{'what': '金鹰直购本期头像(免做任务)截止', 'when': '2026-01-03T11:30:00Z'}]
e['sources']['en'] = ['https://warthunder.com/en/news/9814']
e['sources']['zh'] = ['https://warthunder.com/zh/news/2393']

# ---------- F. sale_202512_c:冬促归位 ----------
e = by['sale_202512_c']
e['name_zh'] = '战争雷霆冬季特卖正式上线!'
e['awards'] = []
e['tasks'] = ''
e['notes'] = ('⚠ 2026-11-11 修复:本条原被灌「史海拾遗·十二月」标题与预告文(EN 名实为冬季特卖);'
              '十二月史海内容已归还 marathon_202512;本条 zh 双源=游戏内冬促(2440)+Gaijin 商城冬促(2447)。'
              '游戏内冬季特卖+商城冬促(12-24 上线,延至 1 月)。')
e['sources']['zh'] = ['https://warthunder.com/zh/news/2440', 'https://warthunder.com/zh/news/2447']

# ---------- G. special_202601:一月2026(新建,篇从十二月外移) ----------
n16 = {
 'id': 'special_202601', 'type': 'special',
 'name_zh': '史海拾遗·一月:列宁格勒的天空', 'name_en': 'Pages of History (January): In the Skies of Leningrad',
 'start': '2026-01-01', 'end': '2026-01-31', 'end_precision': 'day',
 'end_raw': 'From January 1st until January 31st',
 'dm_event': None, 'vehicles': [],
 'awards': TROPHY[:4] + ['专属玩家头像(完成全部 8 任务;金鹰直购截止 2026-02-03 11:30 GMT)'],
 'discounts': [], 'deadlines': [],
 'tasks': '1 月 1 日至 31 日连续开放 8 个任务(每 3-4 天一个);随机战斗完成(突击模式除外);全部完成得专属头像',
 'notes': ('月度历史任务活动,主题=列宁格勒的天空;2026-11-11 补建:预告文(2025-12-30)原被 M2 合并挂在十二月条目下。'
           '⚠ zh 孪生未检出(title_map 无此条),待后续增量补挂'),
 'sources': {'en': ['https://warthunder.com/en/news/9874'], 'zh': []},
}

# ---------- H. special_202506_c:英国武装部队纪念日 2025(新建) ----------
nu25 = {
 'id': 'special_202506_c', 'type': 'special',
 'name_zh': '英国武装部队纪念日:「2025 英国武装力量纪念日」贴花', 'name_en': 'A Themed Decal for British Armed Forces Day!',
 'start': '2025-06-27T12:00:00Z', 'end': '2025-06-30T12:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From June 27th (12:00 GMT) until June 30th (12:00 GMT);北京时间 6 月 27 日 20:00 至 6 月 30 日 20:00',
 'dm_event': None, 'vehicles': [],
 'awards': ['「2025 英国武装力量纪念日」贴花'],
 'discounts': [], 'deadlines': [],
 'tasks': ('使用英国 III 级及以上载具完成 3 场战斗(活跃度≥70%;排除无间断对抗/守卫模式/直升机 PVE)'
           '→「2025 英国武装力量纪念日」贴花;进度在 昵称→成就→节假日→英国武装部队成立纪念日;贴花在自定义「纪念日与节假日」分类'),
 'notes': ('英国武装部队纪念日=每年 6 月最后一个星期六(2025 年为 6 月 28 日),预备役人员提前 3 天庆祝;'
           '全英 170 场庆典;宗旨为向现役与退伍军人传达公众支持。2026-11-11 补建:zh 文原被错挂到 marathon_202505'
           '(合成体病根之一),EN 孪生 9586 同日。'),
 'sources': {'en': ['https://warthunder.com/en/news/9586'], 'zh': ['https://warthunder.com/zh/news/2175']},
}

# ---------- I. special_202606_d:英国武装部队纪念日 2026(新建) ----------
nu26 = {
 'id': 'special_202606_d', 'type': 'special',
 'name_zh': '英国武装部队纪念日:贴花物资箱', 'name_en': 'A Decal Trophy for British Armed Forces Day!',
 'start': '2026-06-26T11:00:00Z', 'end': '2026-06-29T11:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From June 26th (11:00 GMT) until June 29th (11:00 GMT);北京时间 6 月 26 日 19:00 至 6 月 29 日 19:00',
 'dm_event': None, 'vehicles': [],
 'awards': ['「英国武装部队纪念日」贴花物资箱(三选一往期贴花:英国武装部队纪念日/英国国防部纹章/2025 英国武装力量纪念日;集齐三枚改得:20-50% 研发或银狮加成卡/3-5 通用备用载具/1 天高级账号)'],
 'discounts': [], 'deadlines': [],
 'tasks': ('使用英国科技树 III 级及以上载具累计 3000 任务分(随机战斗,排除守卫模式)→贴花物资箱;'
           '完成后需手动领取(昵称→成就→节假日→英国武装部队纪念日);纪念日贴花在「纪念日与节假日」分类,'
           '国防部纹章与 2025 贴花在「英国→陆军」分类'),
 'notes': ('首批维多利亚十字勋章 1857-06-26 授予克里米亚战争将士;2009 年起 6 月最后一个星期六为英国武装部队纪念日。'
           '英国军队二战史:法国投降后独抗德国一年,租借法案下瓦伦丁/玛蒂尔达随红军作战;战后以联军行动为主,'
           '福克兰战争展示千里投送能力。2026-11-11 补建:整年事件此前缺失。'),
 'sources': {'en': ['https://warthunder.com/en/news/10114'], 'zh': ['https://warthunder.com/zh/news/2677']},
}

for n in (n3, n6, n16, nu25, nu26):
    if n['id'] in exist:
        ev[ev.index(by[n['id']])] = n; print('↻', n['id'])
    else:
        ev.append(n); print('+', n['id'])

d['generated_at'] = '2026-11-11T16:00:00Z'
d['counts'] = {'events': len(ev), 'by_type': dict(Counter(e.get('type') for e in ev)),
               'with_discounts': sum(1 for e in ev if e.get('discounts'))}
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', d['counts']['by_type'])
print('SAVED')
