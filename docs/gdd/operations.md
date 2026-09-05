---
doc_id: GDD-OPERATIONS
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: Operation模式设计
canon_basis: "SRC-SSOT-2.0 §4A；最新用户Operation与武器改装意图"
depends_on: ["vision.md", "world-and-information.md"]
---

# Systemic Tactical Operation

## 玩家目的与范围

进入失控设施，带着事先选好的装备面对资源、路线和团队执行问题。本文仅拥有模式旅程与配置差异，共享战斗、经济、世界、生命规则分别归其系统文件。

OPS-001 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

Run是一个连续Operation/Facility/Mission，无玩家可见Layers；资源、门、Cart、Knowledge、Support和Optional后果连续保留。Mission比改装更核心；采用有限Field Modification，不启用自动Fusion或无限Relic池。移除改装后的同任务对照仍应有趣。

OPS-002 · CANON · 来源：SRC-SSOT-2.0 §4A.8、§4A.16。

完成目标后以可观察的世界恶化推动离开，无“60秒到点处决”式硬撤离计时；留下不提供稳定farm收益。真正不可恢复Wipe意味着失败，无gameplay checkpoint。恢复见[生命](survival-and-recovery.md)，持久收益见[进度](progression-and-bastion.md)。

## 最新 REVIEW RECOMMENDATION

OPS-003 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

唯一首发Operation；入场锁装备身份，局内以WeaponModule/ToolModule/TeamProtocol改变解法。标准长局初值每玩家2保证+1可选机会；安装预览后3s在合法维护点提交，同挂点替换、旧件留世界。原自动Fusion仅Lab/FUTURE，不能吞掉Operation配件。数量和挂点归[测试参数](../production/test-profile.md)，统一数学归[修改与效果](modifications-and-effects.md)。

## 玩家旅程与状态

OPS-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮模式扩写。

| 阶段 | 玩家主要问题 | 使用的共享系统 | 结束证据 |
|---|---|---|---|
| Briefing/Loadout | 带什么、任务与风险是什么 | [玩家](player-and-input.md)、[战斗](combat-and-arsenal.md) | 真人Ready，公开ruleset固定 |
| Insertion | 武器能否完成当前对手问题 | 战斗/敌人 | 首个可读战斗与任务上下文 |
| Recon | 缺什么信息，走哪条路 | [世界](world-and-information.md) | 取得合法位置/设施状态 |
| Commit | 花资源改变什么 | [经济](economy-and-support.md) | Cart/Support事务及世界后果 |
| Execution | 如何兑现先前选择 | [任务](missions-and-spaces.md) | 前向故障被解决/降级 |
| Exit | 值得再贪吗、怎么带队走 | 世界恶化/生命 | 退出或最终失败 |
| Debrief | 哪项决定造成结果 | [战报与回放](debrief-and-replay.md)、进度/因果记录 | 结算、可回看行动与下一局动机 |

Authority拥有run phase和唯一结果；模式不自行复制伤害、物资、合成或存档实现。离队/重连保留当前角色Seat与配装状态，新进者可接管空Seat并读取简短当前目标/资源/已提交决策，不重做briefing才能游玩。

OPS-009 · CANON · 来源：SRC-USER-2026-09-05-LEGACY-ID-LOW-CLEARANCE；权限语义归[设施规则WRD-015](world-and-information.md)。

Operation小队使用旧制人类身份进入断网设施。凭证通常足以通过基础识别，却只能取得低级、局部或过期权限；壁垒无法在远端直接接管设施。Recon与Execution阶段因此包含现场确认旧身份映射、恢复设施内权限链或在权限不足时选择替代路线。每项任务必须明确起始权限、可恢复权限及越权后果，不能把“权限不足”当作任意锁门借口。

OPS-010 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-USER-2026-09-05-CARRIER-REBOOT-PHYSICAL-RECOVERY；SRC-USER-2026-09-05-LIMITED-NODE-DEFENSE-ASSETS；SRC-USER-2026-09-05-REGION-RISK-REWARD-PROFILES；SRC-USER-2026-09-05-OPTIONAL-GLYPH-REROUTES。

设施网络恢复是Operation任务族之一，不代表玩家正在永久收复一个界桥节点。执行该任务时，小队进入失联设施建立Terminal Uplink、读取载波、重写本地人类协议并恢复设施控制。成功必须改变本局可观察状态，包括通信恢复、地图/任务信息更新，以及符合权限的炮塔、机器人、门和资源库转为己方；失败或中断不得伪装成设施已经恢复。界桥节点及其长期清场只属于世界观，基础游戏不显示或累计节点进度。

区域配置保持不同风险回报。无限探索区补给少、虚空兽和路线危险更多，回收废料、材料、外观信用点、字形知识与筑路者资料更丰富；限界探索区弹药、医疗、炮塔、机器人和封闭储备更多，前期仍有虚空兽及失控防御，但完成重写后更容易建立安全据点，长期探索奖励相对少。可选字形改线连接预先存在的秘密支路，以额外敌人、功率、时间或退路风险换取资源、信用点、成就、外观或知识；它不是免费奖励室。

OPS-011 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-PROCEDURAL-OPERATION-HUB-BOARD；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY；SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE；生成责任见[任务MIS-016](missions-and-spaces.md)。

Operation是从壁垒中央Hub任务板选择的可复玩合同。每份任务Offer在出发前公开区域和设施主题、随机主任务、零到一个常规支线、已知局势/环境警告、主要奖励、预计任务长度和可选难度；极少数手制特殊任务可以另有第二支线，但不能成为生成器默认。队伍选定任务与难度并Ready后锁定MissionSeed和规则版本，加载随机地图；失败、退出或读档不得重掷同一已锁定实例来窥探地图与奖励。

所有Operation都应让门、电力、路线、防御、敌人或资源在本局内真实响应玩家行动，但基础游戏不保存玩家可见的节点版图、清场状态或账号剧情阶段。程序合同负责侦察、维修、回收、运输、压制、样本、救援或防御；特殊合同可以提供手制事件或公共世界事件内容，但不构成必须按顺序完成的个人主线。可选故事发现进入玩家Archive，节点统计仅在OPS-013定义的Descent发布联合行动期间启用。

五档难度沿用ENC-003，选择发生在锁定任务后、进入任务前；难度不得改变任务事实或封锁核心故事收藏。它只调整公开的敌人组合与协同、资源/复活压力、环境约束和可选变异，并可提供透明的结算倍率或挑战资格；具体初始外观奖励倍率见测试参数，核心知识和任务事实不受倍率改变。重要故事收藏不得因任务板刷新、随机Seed或现实时间活动永久错过；任务板采用6个Offer，回Hub/完成合同刷新，出发前可免费手动整批刷新；锁定Run后不可重掷，初值见测试参数。

OPS-012 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-OPERATION-MISSION-PORTFOLIO-PCG；详细生成见[任务MIS-016–MIS-017](missions-and-spaces.md)。

正式Operation不使用GTFO式完整固定关卡。每局从区域、设施主题、主任务、兼容支线、空间图、系统状态、资源分布、敌人来源和公开Mutator生成新的MissionInstance；关键剧情地标可以是必经手制Cluster，但抵达路线、相邻空间、目标位置和局势仍由Seed组合。设计目标是玩家反复遇见熟悉规则，却不能依靠背诵整张地图和固定刷怪点完成任务。

首批任务组合至少覆盖以下不同工作，不得把它们全部换皮成“启动终端后守圈”：

| 任务族 | 核心动作与压力 | 主要产出 |
|---|---|---|
| 废料回收 | 搜索、评估价值、携带或拆解，并决定何时停止贪取 | 废料、外观信用点价值物 |
| 资源取得 | 定位、恢复采集/仓储、分配供能并把有限资源安全运出 | 人造太阳材料、弹药/医疗供应、战略资源 |
| 技术回收 | 突破权限或物理封锁，保护原型、部件或制造设备完整撤离 | 武器/工具横向解锁、维修能力 |
| 研究数据 | 恢复研究设施、确认数据真实性，并在快速残缺上传与高风险完整提取间选择 | Archive、字形与筑路者知识 |
| 设施网络恢复 | 重建本地载波译码与身份映射，夺回设施控制 | 友军防御、设施情报、当前合同资源 |
| 威胁处理 | 追踪、诱导、封锁、捕获或击杀明确威胁 | 路线安全、样本、危险区域准入 |

同一任务族必须能因地图拓扑、支线、设施系统、敌对来源和资源分布要求不同计划，而不仅是目标物换名字。某个任务族若无论Seed如何都产生同一路线和同一防守终局，应删减或重做生成槽，不能把“随机门的位置不同”冒充新体验。

OPS-013 · DIRECTION · 来源：SRC-USER-2026-09-05-NODES-LORE-ONLY-DESCENT-COMMUNITY-EVENT；世界边界见[世界观NAR-030](narrative-bible.md)。

基础游戏的任务板不显示节点地图、节点所有权或节点恢复计数。准备发布Descent DLC时，才开启一次全服务器联合行动：指定的程序Operation根据公开条件贡献`NodeRecoveryProgress`，全体玩家共同修复通向第一个真实敌对行星端点的路线。进度属于服务器级活动账，不是某个玩家私人世界，也不把每张随机地图宣称成独立永久节点。

联合行动完成后，端点在唯一正史中永久开放，并成为Descent入口。活动可以提供参与纪念外观、日志和阶段性Hub变化，但不能把已购买DLC永久扣在社区阈值后面；必须预设确定的完成/开放方案，使晚入坑、离线或活动结束后购买的玩家仍能访问内容。本作是合作PVE，活动只做结果去重和数据完整性，不建设竞技反作弊。阈值、贡献算法、区域服务器合并方式、活动时长和是否允许失败仍OPEN，发布方案确定前不得把它写成首发依赖。

## 模式配置与参数唯一表

| 项目 | 当前合同 | 唯一责任 |
|---|---|---|
| 标准长局 / Demo / 首个灰盒 | 40–50 / 15–25 / 10–15分钟体验目标，TEST | [首发范围](../production/release-scope.md) |
| 现场改装机会与挂点 | 2保证+1可选初值；明确安装替换 | [测试参数](../production/test-profile.md) |
| 自动Fusion / 无限Relic | Operation禁用；Lab/FUTURE隔离 | [修改与效果](modifications-and-effects.md) |
| 入场槽位 | 2枪 / 1工具 / 1自由战术模块 | [玩家合同](player-and-input.md) |
| 任务板与难度倍率 | 六Offer与免费局前刷新；倍率仅允许外观收益 | [测试参数](../production/test-profile.md) |

## 内容接口与边界

OPS-005 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮模式扩写。

首个模板采用[BLACKSTART](../content/blackstart.md)，主角是Terminal信息与Power Cart，Door/Support作支撑；不额外塞Boss、Predator或谜题大全。所有主线能无Bot单人顺序完成。已完成目标后只关闭该目标可重复奖励来源，不能偷删未取得且设计承诺的资源；世界恶化必须有实际路径与反馈。若能稳定farm，先修奖励来源/可见世界行为，不加隐藏处决表。

## 正常、失败与跨系统示例

OPS-006 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮模式扩写。

正常：队伍选择稳枪配件牺牲ADS速度，然后用通风换得较远视线；装备与路线共同产生计划。失败：最后医疗被早耗，终局仍有合法近战/封门解法但团队执行失败；结算保留已上传知识，不回档。跨系统：一人选下挂结构工具，能更有效破坏普通可破结构，但不能绕过需要任务Cell的关键门。

## 验收与尚未实测项

OPS-007 · TEST · 来源：本轮模式验证建议。

以相同枪感/敌人/时长比较“纯战斗任务”“设施选择Operation”“设施选择+少量改装”；记录自发复玩、后果复述、等待、资源争执，而非问玩家喜欢多少系统。M2微BLACKSTART验收后若任务层未明显提高复玩，停止扩建设施，回到分叉决策。准确Gate归[制作计划](../production/roadmap-and-validation.md)。
## Team Ordnance 的模式位置

OPS-008 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-USER-2026-09-04-ORDNANCE-MISSIONS。
临时团队重武器是任务中的强力世界资产，能推动Breach、短时火力优势与Predator Reversal，但不改变常规loadout identity。玩家带入的枪继续是主角，特殊资产通过双手与空间成本制造需要队友的机会。详细机制归战斗，首个可搭建分支在BLACKSTART。
