#!/usr/bin/env python3
"""One-time review corrections after the explicit baseline migration."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'docs'
MARKER=D/'governance/finalization-baseline.json'

def replace(path: str, old: str, new: str) -> None:
 p=D/path; text=p.read_text(encoding='utf-8')
 if old not in text: raise RuntimeError(f'Review anchor not found: {path}: {old[:70]}')
 p.write_text(text.replace(old,new),encoding='utf-8')

def section(path: str, start: str, end: str, body: str) -> None:
 p=D/path; text=p.read_text(encoding='utf-8'); a=text.index(start); b=text.index(end,a+len(start))
 p.write_text(text[:a]+body.rstrip()+'\n\n'+text[b:],encoding='utf-8')

def append(path: str, body: str) -> None:
 p=D/path; p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n'+body.strip()+'\n',encoding='utf-8')

def main() -> None:
 data=json.loads(MARKER.read_text(encoding='utf-8'))
 for rel,digest in data['protected_source_sha256'].items():
  if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest: raise RuntimeError('Protected source changed: '+rel)
 if data.get('review_corrections_applied'):
  print('Review corrections already applied.'); return
 hist='governance/history/decision-register-before-finalization-2026-09-05.md'
 replace(hist,'depends_on: ["authoring-guide.md", "../gdd/vision.md"]','depends_on: ["../authoring-guide.md", "../../gdd/vision.md"]')
 replace(hist,'# 决策、冲突与未决问题总览','# 定稿前决策与未决问题（历史，2026-09-05）')
 replace('gdd/survival-and-recovery.md','当前合法HealthCap的20–25% · TEST','当前合法HealthCap的20% · TEST；数值归测试参数')
 replace('gdd/survival-and-recovery.md','HealthCap的35–50% · TEST','当前合法HealthCap的40% · TEST；数值归测试参数')
 replace('gdd/economy-and-support.md','当前Energy firearm候选使用可掉落、可补给的有限Energy Block；Heat若保留只是额外承诺，不生成弹块，也不能靠等待恢复有限资源。该方向与ECO-001继承的广义Energy续航表述需在枪械范围冻结时正式裁决；现在不删除Staff或Arcane基线。','Operation Energy枪已选择可掉落、可补给的有限Energy Block；Heat只限制节奏，不生成弹块。DDD-0014已经覆盖旧广义Energy续航的Operation解释；Staff/Arcane只保留Lab/FUTURE，不加载到当前奖励池或配装。具体三枪数值见战斗试制参数。')
 replace('gdd/economy-and-support.md','Pod内容公共所有：Ammo/Med/Tactical/Power可拿、放、再分；Weapon/Relic用Shared Draft，首轮每人最多claim一件或Pass，余物之后自由。Relic吸收后不能drop；Prototype是可转交团队资产。Host/Leader无特权。可从reserve拆出按ammo family/capacity拾取的实体bundle，并放回合法locker/storage。','Pod内容公共所有：Ammo/Med/Tactical/允许的Power可拿、放、再分，关键任务Cell不能被随机补给生成。Operation高价值Modification用Shared Draft，首轮每Seat最多claim一件或Pass，余物之后自由。固定入场枪身份不由Pod随机替换；模块按挂点安装，拆出实例可留世界，Prototype是可转交重资产。Host/Leader无特权。reserve可拆为按弹族/容量拾取的实体bundle并放回合法locker；Lab吸收型Relic不进入此Operation流程。')
 replace('gdd/economy-and-support.md','正常：队伍缺Ammo但想要Relic','正常：队伍缺Ammo但想要枪械模块')
 replace('gdd/economy-and-support.md','跨系统：Relic把团队标记窗口转成节省装填时间','跨系统：合法模块把团队标记窗口转成节省装填时间')
 replace('gdd/economy-and-support.md','永远选Energy/Relic Pod','永远选Energy/Modification Pod')
 replace('gdd/economy-and-support.md','推荐Operation奖励以WeaponModule/ToolModule/TeamProtocol为主，数量和原Relic目标冲突归[模式参数](operations.md)。','Operation奖励确定为WeaponModule/ToolModule/TeamProtocol，数量由[测试参数](../production/test-profile.md)拥有，原Relic目标只属Lab。')
 replace('gdd/economy-and-support.md','传统Relic自动Fusion只留Lab/未来规则集候选，现行源基线与新方案由决策记录区分。','传统Relic/自动Fusion仅留Lab/FUTURE；当前Operation选择由DDD-0014记录，不存在两套并行官方经济。')
 replace('gdd/player-and-input.md','Operation推荐入场锁定装备身份，局内少量Weapon/Tool Modification；具体次数由[模式参数](operations.md)拥有。','Operation入场锁定装备身份，局内有限Weapon/Tool Modification；具体次数由[测试参数](../production/test-profile.md)拥有。')
 replace('gdd/progression-and-bastion.md','失败保留已上传/Banked Knowledge/Data的100%、Cosmetic/Fusion Discovery；Run Weapon/Relic/Spell/Utility/Prototype不永久继承，Mission Completion Bonus失败无。代币失败比例是测试而非保证。成功与失败结果都须有可追踪凭据。','失败保留已上传/Banked Knowledge/Data的100%和已合法入账的外观/收藏；Run枪械实例、Modification、工具资源与Prototype不永久继承，失败无Mission Completion Bonus，未撤离废料收益0%。不因一次任务失败撤销此前合法账号解锁。Lab的Fusion发现是隔离测试数据，不写官方Operation解锁。成功/失败均有可追踪幂等凭据。')
 replace('gdd/missions-and-spaces.md','纯合法近战/Staff loadout或明确局前限制','全部首发合法两枪/一工具/一战术模块配装；Staff/主近战不在Operation合法集合')
 replace('gdd/missions-and-spaces.md','推荐管线为：','选定管线为：')
 replace('gdd/coop-and-social.md','已领Relic记录','已领Modification记录')
 replace('content/blackstart.md','增加Knowledge/Relic/Support','增加Knowledge/Modification/Support')
 replace('gdd/world-and-information.md','跨系统：Spear玩家在普通Door将被砸开前拉开距离','跨系统：Shotgun玩家在普通Door将被砸开前拉开距离')
 replace('gdd/world-and-information.md','| 安全确认延迟/门耐受/Query耗时 | OPEN | 原文未给定 |','| 安全确认/普通门/终端响应初值 | 3s保持确认 / 120结构HP / 本地响应目标≤0.2s · TEST | 见测试参数；玩家理解查询步骤与系统响应时间分别测量 |')
 replace('gdd/encounters-and-difficulty.md','Difficulty表中的伤害/血量/感知距离/压力窗口均OPEN，不从“最高难”直接推导更多血量。','五档初值采用测试参数TP-DIFFICULTY-COMBAT；敌人基础HP/伤害/感知不随难度暗变，以有限来源规模、组合、普通补给和环境决策变化难度。所有初值待试玩，不以“最高难”直接推导更多血量。')
 replace('gdd/encounters-and-difficulty.md','最终采用哪些刺激仍需原型确认','初版采用接触/伤害立即唤醒、局部声能累积达到阈值唤醒；单纯恢复稳定供电不立即唤醒，数值见测试参数')
 replace('gdd/encounters-and-difficulty.md','Storyteller扩展、具体Horde密度、难度曲线全部待试玩。','初版只交付一个设施状态驱动Director，不实现七套命名Storyteller。Black Swan与Daily排行榜事件后置；难度、密度和唤醒初值见测试参数，均待试玩。')
 replace('gdd/ux-and-accessibility.md','推荐Operation改装以可见挂点和tradeoff表达','Operation改装以可见挂点和tradeoff表达')
 replace('gdd/audio-and-haptics.md','精确voice预算、duck量、haptic强度OPEN，不能把torture规模当实际音轨数。','音频初值采用测试参数TP-AUDIO，实际听辨和设备预算尚未测量，不能把torture规模当实际音轨数。')
 replace('gdd/vision.md','推荐首先验证','已选择，先验证')
 replace('gdd/vision.md','推荐边界与双倍资源反例','当前边界与双倍资源反例')
 replace('gdd/vision.md','推荐profile因此进一步收敛到','当前profile因此确定为')
 replace('content/modification-catalog.md','# 修改、Relic 与 Fusion 内容候选','# Operation修改目录与Lab实验')
 replace('content/modification-catalog.md','Operation候选优先WeaponModule/ToolModule/TeamProtocol','Operation采用WeaponModule/ToolModule/TeamProtocol')
 replace('content/modification-catalog.md','## Operation Weapon/Tool Modification 候选','## Operation Weapon/Tool Modification 初版测试卡')
 replace('content/characters.md','最终代号、人格、经历、关系、收藏事实与台词数量均待用户裁决和原型测试；所有美术与身体设定按CHAR-008明确延后。','最终代号、人格、经历、关系与收藏事实由OWNER-01审阅；原型台词数量是开发者可调整的TEST，不要求所有者逐个裁决。所有美术与身体设定按CHAR-008明确延后。')
 replace('gdd/story-overview.md','她/他关注的核心问题（代词不指定性别）','核心问题')
 replace('production/platform-and-release.md','## 最新发行建议','## 选定发行路径')
 replace('production/risk-register.md','30天实际吞吐','至少两个已完成里程碑的实际吞吐')
 replace('technical/architecture-and-performance.md','Unity首个技术Spike至少覆盖玩家+一把枪、100/500/1000轻量敌人、Projectile压力、基础Reaction/Effect、4人网络、Host loss恢复、一个Facility模块和一次购入资产导入。','这些Spike分阶段执行而非阻塞第一个构建：M0仅玩家+一把枪和本地命令/构建；M1加入100/500/1000轻量敌人和Projectile/Effect压力测试；M2加入Facility；M3验证4人网络与Host loss。购入资产导入只在OWNER-02批准实际采购后进行，此前用原创灰盒验证同一管线。')
 replace('technical/modding-and-toolchain.md','扩展层级Data→Graph→Sandbox Script，native明确unsandboxed；','长期扩展层级Data→Graph→Sandbox Script，native明确unsandboxed；首版范围由DDD-0017限定为Data/有界Graph，Script/Native与完整TC不在首发；')
 # Specify launch/test/future status on individual rows, not just a distant appendix.
 p=D/'content/combat-prototypes.md'; text=p.read_text()
 for ident in ['W-AR','W-SHOTGUN','W-EM','W-EB-SINGLE','W-EB-AUTO','W-EB-CHARGE','U-SCAN','U-FOAM','E-RUNNER','E-SUPPRESSOR','E-HOLDER','E-SCOUT','E-FLANKER','O-HMG','O-CANNON','O-CUTTER']:
  text=text.replace(f'| {ident} · PROPOSED |',f'| {ident} · DECIDED / 数值TEST |')
 for ident in ['W-HAMMER','W-KNIFE','W-SPEAR','W-SWORD']:
  text=text.replace(f'| {ident} · TEST |',f'| {ident} · Lab/FUTURE TEST |')
 for ident in ['W-STAFF','S-BOLT','S-FIELD','S-WARD','O-GL','O-SONIC']:
  text=text.replace(f'| {ident} · PROPOSED |',f'| {ident} · Lab/FUTURE候选 |')
 text=text.replace('对合法Attack/Spell/Utility延迟Echo','Operation仅对合法已付费枪械攻击延迟Echo')
 text=text.replace('回声额外成本等为PROPOSED','回声额外成本等采用战斗试制参数的TEST初值')
 text=text.replace('其余数值射速、距离、热量、弹仓通过裸武器试测确定，不列伪精确最终DPS。','首发射速、距离、热量、弹仓采用战斗试制参数，后续裸武器实测调整，不称为最终DPS。')
 text=text.replace('## Weapon 与 Spell 卡','## 武器卡（首发与Lab逐行标注）')
 text=text.replace('## Team Ordnance 候选卡','## Team Ordnance（首发三件与未来候选）')
 p.write_text(text,encoding='utf-8')
 section('gdd/central-story-spine.md','## 仍需决定','## 验证与最终审查','''## 本轮叙事问题处置

| 原问题 | 当前决定 / 责任 |
|---|---|
| STORY-Q01/02：四人代号、立场和六组关系 | OWNER-01审阅完整候选；技术配装已解绑，不阻塞灰盒 |
| STORY-Q03：调度机构/Handler | 先用“壁垒外勤调度”功能性称呼及一个任务广播渠道，提供合同风险/目的，不扩写新主要人物；最终机构专名/演员随OWNER-01/03 |
| STORY-Q04：未部署队员 | 未部署者留Hub/轮休，不强迫少人局生成多余跟随NPC；他们不是本局幽灵声音，远程发言须标明合法通信来源 |
| STORY-Q05：公共历史 | 以故事总览的一至五节的大轮廓为已有公共知识；个体决定、证据细节、设施事故由Archive补充，禁止主任务依赖私藏秘密 |
| STORY-Q06：另外两外部种族 | 基础普通简报不宣称四人已遇到灼星种/借尸者；保留既有作者事实和未核实远端信息，正式出场属于未来扩展内容审批 |
| STORY-Q07：公共更新时间线 | 只用版本级PublicHistoryRevision统一切换对白和内容；不是账号剧情Stage；基础1.0不实现实时全球活动后端 |
| STORY-Q08：初批收藏 | 四人物主题+两个设施事件集合，每组3–5片为TEST排产初值；事实/陈述/推断三类显示，具体人物事实随OWNER-01，数量由开发者试测调整 |
| STORY-Q09：Signature绑定 | 已关闭：任意角色可选任意合法个人战术模块，DDD-0014；CharacterID与TacticalModuleID分离 |

以上普通交付选择为delegated决定，既有明确人物/历史事实不被覆盖。最终故事与人物审阅只有OWNER-01这一入口。''')
 # Explicit initial numbers close ordinary implementation questions without pretending they were tested.
 append('production/test-profile.md','''## TP-DIFFICULTY-COMBAT：五档遭遇初值

全部TEST。敌人HP、单次攻击伤害、感知上限均维持内容卡基准，不按难度暗涨。来源预算单位初值：Runner=1、Suppressor=2、Holder=4、Scout=2、Flanker=2；一个标准小型来源预算12点，实际房间只加载语义允许的Role。

| 难度 | 有限来源总预算倍率 | 每批最多并行角色种类 | 普通非关键补给倍率 | 基本原则 |
|---|---:|---:|---:|---|
| Relaxed | 0.7 | 2 | 1.25 | 清楚单方向预兆，保留完整机制与知识 |
| Standard | 1.0 | 3 | 1.0 | 基础侧路/设施选择 |
| Veteran | 1.2 | 4 | 0.9 | 更常见支持+侧翼配合，不提高AI全知能力 |
| Nightmare | 1.4 | 5 | 0.8 | 更多公开环境约束与多源协同 |
| Cataclysm | 1.6 | 5 | 0.75 | 更少资源余量，仍可推理与顺序单人完成 |

真人/Bot有效参战Seat数量1/2/3/4的未来来源预算倍率为1/1.5/2/2.5，不修改在场敌人或关键Cell费用。人数变化只在下一未开始遭遇边界应用；已花掉的Source预算永不重置或因重连再获配额。局部预兆初值至少2s，来源完成后除新真实事件外不因安静而再开波；潜在后续阶段要在任务卡预告，避免无限Source换皮。普通Supply可以随人数做预算但包内守恒不变；关键解题资源必须先通过可解性验证，倍率不能把其乘没。五档都不是只改这个表便宣称完成内容。

## TP-WORLD与TP-WAKE：设施/休眠初值

Cart/重大配置保持确认3s，取消不提交；普通可破门120结构HP、明确SecuritySeal无普通伤害Breach能力就不可破，破门不是付HP绕开任务权限。合法本地终端查询响应目标≤0.2s是系统延迟指标；玩家完成一项常规信息查询中位≤15s是UX指标，二者分别记录。

休眠个体累积WakeExposure：本地接触或实际受伤立即唤醒；可听见的独立大冲击+60、同AttackRoot枪声+25，阈值100，缺少刺激时每秒衰减10。初始普通声源最大传播20m，再按门/材质/实际距离衰减，不能每pellet重复加一次完整声能。供电只解除休眠约束，不直接加满Exposure；靠近而未触碰只在2m内每秒+10。全部是世界范围内局部输入，不读玩家相机/按键，不凭空创建活体；没有供电的伤害反应遵守该生物的具体合法状态而非自动激活全网。

## TP-AUDIO与TP-CAMERA：表现初值

真实3D音频声部初值48：关键危险/团队事实保留8、玩家枪/命中12、敌人/环境20、音乐/低优先8；按距离/优先级虚拟化，不减少Gameplay听觉或伤害事件。队友讲话只对音乐/低优先环境duck −6dB，attack50ms、release300ms，不能duck关键威胁；主音量/音乐/效果/语音/人物对白独立。Haptics初值35%并可0–100%调节，无支持设备仍有视听替代。

FPS默认垂直FOV70度，55–85可调；TPS垂直FOV60度、臂长2.5m、肩偏0.45m、可换肩，碰撞将Camera推至不穿墙处。瞄准镜可声明倍率但不能改变Authority武器散布事实；Camera peek不能获取秘密标记或穿过枪口遮挡。镜头摇晃/运动模糊可关，ADS灵敏度独立，控制器Aim Assist初版只在可见合法目标附近降低转向增益，不自动吸附穿墙、不替玩家按扳机。全部待实际键鼠/控制器与Deck可读性验证。''')
 append('gdd/player-and-input.md','''## PLY-015 · 默认实体输入映射（TEST）

下表是M0的明确可执行初值，不是要求所有者选择键位；玩家可重绑，所有冲突均在设置中提示。提示图标按当前输入设备更新。战斗中的菜单不暂停在线模拟；只有真正离线Solo暂停菜单暂停SimulationTime。

| 动作 | 键鼠默认 | 标准Xbox布局控制器默认 |
|---|---|---|
| 移动/瞄准 | WASD / Mouse | 左/右摇杆 |
| ADS / 开火 | 右键 / 左键 | LT / RT |
| 跑、跳、蹲/跑中滑铲 | Shift、Space、Ctrl | L3、A、B |
| 1/2号枪 | 1 / 2；滚轮切换 | Y切换；持重资产时Y先放下并切枪 |
| 单一工具 | 3选择工具，再Fire提交 | 持LB预备工具，RT提交；松LB取消预备；不能同时发主枪 |
| 个人战术模块 | 4 | RB；动作持续/取消依模块定义 |
| 交互/换弹 | E / R | X点按有合法近距交互时优先交互，否则换弹；持X明确换弹，点按与长按不能双触发 |
| Quick Melee | V | R3 |
| Ping/语义轮盘 | Q点按/长按 | D-pad右点按/长按 |
| 手电 | F | D-pad上 |
| 支援请求 | 持C打开，方向键输入，松C保留/关闭预览不扣费 | 持D-pad下打开支援选择，确认后方向输入；首个打开按键不计入代码 |
| 地图/物资 | M / Tab | View打开地图和物资分页 |
| 视角/换肩 | Z / Alt（TPS） | D-pad左点按切FPS/TPS、长按换肩；可拆分重绑 |
| 暂停/设置/社交 | Escape | Menu |

高风险支援代码完成后仍需合法投掷/放置信标；不会按完方向就远程扣费。控制器的交互/换弹双用途必须在首轮测试检查误操作，并提供将二者拆到任意可用按键/组合的选项；不能强迫残障玩家执行长按或高速代码，可开启等价顺序菜单/切换式输入，但仍付相同模拟时间与资源承诺。宏与设备高帧率不能改变提交时点。''')
 # Make test headings say what they actually contain; do not erase real future/owner OPEN items.
 for p in D.rglob('*.md'):
  text=p.read_text(encoding='utf-8')
  if re.search(r'(?m)^stage: BASELINE$',text) and p.parent.name not in {'decisions','sources'}:
   text=text.replace('## 验证与 OPEN','## 验收与尚未实测项').replace('## 指标与OPEN','## 指标与商业审批')
   p.write_text(text,encoding='utf-8')
 append('governance/finalization-review.md','''## 结构检查后发现并修正

归档搬移后的两个frontmatter依赖路径错误；生命恢复原范围与新初值并列；旧Energy/Relic经济段落仍写等待裁决；叙事Q09仍重复询问已经解绑的模块；单人可解性引用已退出Operation的Staff；世界/音频/难度仍缺执行初值。全部在责任文档直接修正，不只增加概要覆盖。

七项validator自测在本地实际通过；最终远端结构检查结果以对应commit的Actions日志与artifact为准。输入、摄像机、音频、门/休眠和五难度初值仍为TEST，本次没有假装做过游戏或人体工学验证。''')
 data['review_corrections_applied']=True
 data['review_corrections']=['archive dependencies','finite-energy and draft rules','recovery tuning ownership','narrative question disposition','launch versus Lab rows','initial difficulty/world/audio/camera/input profiles']
 MARKER.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Applied responsibility-document review corrections; game validation remains NOT RUN.')

if __name__=='__main__': main()
