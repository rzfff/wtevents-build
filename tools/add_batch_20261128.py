#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-11-28 增量十四轮:2 事件(史海拾遗·十二月 小土星行动 / 潜艇测试)。
来源:官方新闻 en_10343/10344 + zh_2899/2900(标题官方原文;正文 EN 与 zh 全文逐段核实,中文译名取自 zh 官方文)。
背景:11-25 之后哨兵新报的 3 篇里,这 2 篇是库内已有先例的真活动(史海拾遗月度系列 / 测试类活动);
第 3 篇 Steam 大奖提名(10342/2898)库内无同类先例,站长未裁决,本轮不收录。幂等:↻ 按 id 整条替换。"""
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
 'id': 'special_202612', 'type': 'special',
 'name_zh': '史海拾遗·十二月:小土星行动',
 'name_en': 'Pages of History (December): Operation Little Saturn',
 'bp_season': None,
 'start': '2026-12-01', 'end': '2026-12-31', 'end_precision': 'day',
 'end_raw': 'From December 1st until December 31st',
 'dm_event': None,
 'vehicles': [],
 'awards': [
   '每完成 1 项任务得 1 个作战物资箱(8 项任务逐项发放),箱内为下列之一:20-50% 研发加成卡(持续 3-10 场)/20-50% 银狮加成卡(持续 3-10 场)/3-5 份备用载具兑换卡/1 天高级账户/随机地面载具涂装(仅限可用金鹰购买或成就解锁的类型)',
   '完成全部 8 项任务:本期特供个人资料头像(瓦西里·巴达诺夫)',
 ],
 'discounts': [],
 'deadlines': [{'what': '巴达诺夫个人资料头像可用金鹰直接购买(无需完成任务;昵称 → 成就栏 → 史海拾遗)',
                'when': '2027-01-03T11:30:00Z'}],
 'sub_events': [
   {'name': '伯恩哈特防线', 'start': '2026-12-01T11:00:00Z', 'end': '2026-12-05T11:30:00Z',
    'note': '1943-12-01 起,美军(克拉克将军)与英联邦、自由法国部队进攻古斯塔夫防线前方的伯恩哈特防线突出部,耗时一个半月才突破'},
   {'name': '锡奥战役', 'start': '2026-12-05T11:00:00Z', 'end': '2026-12-09T11:30:00Z',
    'note': '1943-12 至 1944-03 初,巴布亚新几内亚北岸锡奥镇:美澳军与巴布亚部队攻坚 1942 年起设防的日军,以较小代价获胜'},
   {'name': '罗盘行动', 'start': '2026-12-09T11:00:00Z', 'end': '2026-12-12T11:30:00Z',
    'note': '1940-12-09 盟军在北非反攻,以劣势兵力大胆突袭,意军大批投降,从埃及马特鲁一路溃退到利比亚班加西'},
   {'name': '冬季风暴行动', 'start': '2026-12-12T11:00:00Z', 'end': '2026-12-16T11:30:00Z',
    'note': '1942-12-12 曼施坦因的顿河集团军群自南面为斯大林格勒被围的第 6 集团军解围,险些突破;第 6 集团军缺燃料未突围,行动失败'},
   {'name': '阿登反击战', 'start': '2026-12-16T11:00:00Z', 'end': '2026-12-19T11:30:00Z',
    'note': '1944-12-16 德军在阿登突袭盟军,意图迫英美单独媾和后抽兵东线;历时一个半月,双方损失惨重,德军未达成目标'},
   {'name': '库尔斯克-奥博扬行动', 'start': '2026-12-19T11:00:00Z', 'end': '2026-12-23T11:30:00Z',
    'note': '1941-42 年冬苏军反攻,试图夺回库尔斯克与奥博扬两城,进展甚微、损失惨重'},
   {'name': '第三次长沙会战', 'start': '2026-12-23T11:00:00Z', 'end': '2026-12-27T11:30:00Z',
    'note': '1941-12-24 起日军第 11 军仓促攻长沙,守军阻击+侧翼反击切断补给线,阿南惟几下令全线退却——日军偷袭珍珠港以来首败'},
   {'name': '巴伦支海海战', 'start': '2026-12-27T11:00:00Z', 'end': '2026-12-31T11:30:00Z',
    'note': '1942-12-31 德军希佩尔海军上将号与吕佐夫号拦截英国 JW 51B 北极船队,英护航舰将其击退、船队无损抵达摩尔曼斯克;雷德尔辞职、邓尼茨接任(官方英文文误作 1941 年)'},
 ],
 'tasks': ('12 月 1-31 日连续开放 8 项历史战役任务:使用与当期史实事件关联的载具参战;每个任务在起始日北京时间 19:00 开始、'
           '截止日北京时间 19:30 到期;除 PVE 守卫模式(Assault)外的任意随机战斗均可完成;各时段任务与进度在 昵称 → 成就 → 史海拾遗 查看。'),
 'notes': ('月度任务活动「史海拾遗/Pages of History」12 月篇,战场从巴布亚新几内亚、北非到长沙与斯大林格勒;'
           '本期头像人物=瓦西里·巴达诺夫(第 24 坦克军军长:1942-12 五天突进 240 公里,12-24 摧毁被围第 6 集团军的补给机场塔钦斯基,'
           '挫败「冬季风暴」解围行动,首枚二级苏沃洛夫勋章获得者)。官方文 11-25 发布,哨兵 11-26 04:53 报新;2026-11-28 增量十四轮补录。'),
 'sources': {'en': ['https://warthunder.com/en/news/10343'], 'zh': ['https://warthunder.com/zh/news/2899']},
}

n2 = {
 'id': 'special_202611_g', 'type': 'special',
 'name_zh': '战争雷霆开启潜艇测试！',
 'name_en': 'Testing Submarines in War Thunder!',
 'bp_season': None,
 'start': '2026-11-26T11:00:00Z', 'end': '2026-11-30T11:00:00Z', 'end_precision': 'hour',
 'end_raw': 'From November 26th (11:00 GMT) until November 30th (11:00 GMT)',
 'dm_event': None,
 'vehicles': [V('us_sub_tang', '刺尾鲷级潜艇', 'Tang-class'), V('germ_sub_type_21', 'XXI 型潜艇', 'Type XXI')],
 'awards': [],
 'discounts': [], 'deadlines': [],
 'sub_events': [
   {'name': '美国阵营:刺尾鲷级潜艇 + 水面与空中支援', 'start': '2026-11-26T11:00:00Z', 'end': '2026-11-30T11:00:00Z',
    'note': '水面:罗利号轻巡洋舰、弗莱彻级驱逐舰、迪利级护卫舰、PT-103 型鱼雷艇;空中:搭载全新深水炸弹的 PBY-5A 卡特琳娜、F6F-5 地狱猫'},
   {'name': '德国阵营:XXI 型潜艇 + 水面与空中支援', 'start': '2026-11-26T11:00:00Z', 'end': '2026-11-30T11:00:00Z',
    'note': '水面:埃姆登号轻巡洋舰、Z 43 号驱逐舰、龙号布雷舰(猎潜艇)、S-38b 级鱼雷艇;空中:携带空投深水炸弹的 He 111 H-16、Bf 109 F-2'},
 ],
 'tasks': ('入口:「军事行动与竞技场」侧边栏 → 潜艇测试;街机与历史模式同步开放,按随机海战规则在 4 张带精细海床地形的地图'
           '(非洲海湾、帕劳群岛、极北海港、日本·横滨港)对抗;全平台玩家均可参加;属初步测试,无奖励,欢迎反馈与报错。'),
 'notes': ('潜艇及配套机制的首次公开测试。①水声探测:水听器(被动,两艘潜艇+埃姆登号+Z 43 号配备)与声呐(主动,美德巡洋舰、驱逐舰+迪利号+龙号配备);'
           '舰船噪音随航速、螺旋桨空泡增大,潜艇周围常显「噪音传播范围」圆环;水听器对准噪音源按住开火键调增益测距,松开后舰员解算鱼雷提前量,'
           '启用鱼雷瞄准解算时目标在射界内即自动修正航向;主动声呐信号易被对方水听器听到。②温跃层在 40 米深度,其下潜艇无法被被动/主动声呐探测、'
           '自己也听不到上方,而鱼雷只能在 20 米以浅发射。两艘测试潜艇=2.61.0.40 入库的活动潜艇(美 us_sub_tang / 德 germ_sub_type_21,III 级 BR 4.7,'
           '中文名取自官方中文文,游戏内中文名截至 11-28 仍为英文 Type Tang / Type XXI)。官方文 11-26 发布,哨兵 11-27 04:53 报新;2026-11-28 增量十四轮补录。'),
 'sources': {'en': ['https://warthunder.com/en/news/10344'], 'zh': ['https://warthunder.com/zh/news/2900']},
}

for n in (n1, n2):
    if n['id'] in exist:
        ev[ev.index(next(e for e in ev if e['id'] == n['id']))] = n; print('↻', n['id'])
    else:
        ev.append(n); print('+', n['id'])

d['generated_at'] = '2026-11-28T06:00:00Z'
d['build'] = 'inc14-20261128'
d['counts'] = {'events': len(ev), 'by_type': dict(Counter(e.get('type') for e in ev)),
               'with_discounts': sum(1 for e in ev if e.get('discounts'))}
json.dump(d, io.open(P, 'w', encoding='utf-8', newline=''), ensure_ascii=False, indent=1)
print('events:', len(ev), '| by_type:', d['counts']['by_type'])
print('SAVED')
