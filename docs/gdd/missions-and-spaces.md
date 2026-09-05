---
doc_id: GDD-MISSIONS
doc_type: gdd
stage: DRAFT
updated: 2026-09-05
owner_role: 任务与空间设计
canon_basis: "SRC-SSOT-2.0 §4A.7、§13.5、§15、§17"
depends_on: ["world-and-information.md"]
---

# 任务语法、空间生成与可解性

## 玩家目的

每局面对熟悉问题与不同局势，靠路线、设施和资源选择改变任务结果。固定谜题一旦背熟就失去谜底；本项目需要持续的不确定局势和执行压力。

## 范围与术语

Template定义任务问题；Cluster是手制空间；port描述安全/维护/交通/通风/Fold/货运/电力/Optional/ThreatIngress连接；Situation定义当前威胁与世界状态。生成器不替设计师发明核心乐趣。

## 已确认规则

MIS-001 · CANON · 来源：SRC-SSOT-2.0 §15.1–§15.3。

主要任务至少有一个变化的世界状态及一个真改变后续玩法的选择。语法有Restart/Reconfigure、Predator Reversal、Capability Acquisition、Infrastructure Reclamation、Condition-sensitive Transport、Network/Uplink、Containment Allocation、Ecological/System State Collapse。常规只用一个Primary加零到一个Secondary，极少第三个；禁止全塞。

MIS-002 · CANON · 来源：SRC-SSOT-2.0 §4A.7、§15.3、§17.1–§17.3。

Operation使用手制Cluster和程序图/状态，Forward-Branch-Rejoin，Optional尽量有前方第二出口，主线不强迫回五到十分钟前Terminal，新Power Cell在下游Relay配置，撤离尽量新路线。目标/终端/Cell可变位置但合法可达，需Resource Safety Budget；技术合法但无聊或不公的图仍不合格，不能空走廊凑时长。

MIS-003 · CANON · 来源：SRC-SSOT-2.0 §15.5、§13.5。

子目标失败优先Degraded Success：丢功能、改局勢或增加有意义步骤。不可逆失败应少且提前可读，生成器可验证。Predator序列为Threat→Manipulation/Trap→Capability Acquisition→Reversal，前向取得能力，敌人经真实空间到前方。

MIS-004 · DIRECTION · 来源：SRC-SSOT-2.0 §15.4、§17.2。

BLACKSTART=Restart+Containment；HUNTING GROUND=Predator+Capability；COLD STORAGE=运输条件+设施回收；DEAD NETWORK=网络+状态坍塌。Descent使用Isaac-like宏观图和手制真3D空间，Treasure/Shop/Gamble/Sacrifice/Elite/Event/Secret/Boss分类仍待原型审定。

## 玩家流程

MIS-005 · PROPOSED · 来源：本轮系统扩写。

Briefing给目标与一项主要未知→探索确认事实→选分支→执行条件明确的动作→读世界变化→处理前向故障→达成或降级完成→撤离。谜题信息应位于问题附近或前向必经路径，不能把Wiki知识设为正常成功门槛。

## 状态与数据所有权

MIS-006 · PROPOSED · 来源：本轮系统扩写。

Authority拥有ObjectiveState、critical item凭据、world dependencies、route graph、completion reason。每次目标动作提交携带前置世界版本与幂等ID，网络Client只请求。Designer拥有模板约束，Generator只填可替换Situation槽。

| 起点 | 事件 | 结果 |
|---|---|---|
| Briefed | 插入完成 | Active，主目标可读 |
| Active | 子动作完成且依赖满足 | WorldChange+下一步原子推进 |
| Active | 可降级子目标失败 | Degraded，说明丢失价值/新路径 |
| Active/Degraded | Primary条件成立 | Resolved，开启合法撤离 |
| Active | 不可恢复条件成立且已预告 | Failed，发唯一结果 |
| 任意 | 旧动作重放 | 返回原结果，不重复发奖/开门 |

## 生成资源可解性

MIS-007 · PROPOSED · 来源：本轮系统扩写。

先检查图可达、必需资源可达与能力可满足，再检查消费约束，最后人工判断有趣。把任务必要消耗与可选择战斗分开：对每条批准主路径，计算初始可用量+保证可达供给−必要动作消耗−代表性战斗保守消耗；至少一条路线满足所有资源族非负及HealthCap合法。医疗不能简单算“敌人必然造成伤害”，应按可执行反制与试测分位值估计。

独特任务Cell做离散库存与依赖检查：拿到它不能依赖先花同一个Cell。Power选择枚举所有合法配置，保证成功/已预告降级/明确失败三者之一，不出现无提示死锁。还需检查无Bot单人、任意一至四个不同角色Seat、纯合法近战/Staff loadout或明确局前限制。数学通过仅代表存在解，不代表新手知道解；可观察线索和实际路径必须试玩验证。

## 模式配置与内容接口

MIS-008 · PROPOSED · 来源：本轮系统扩写。

Operation Template引用世界/经济规则与特定content profile；Lab没有任务图但仍消费相同run lifecycle/奖励协议。内容卡声明目标、状态依赖、动作、资源、port、降级、失败、退出和验收。固定[BLACKSTART](../content/blackstart.md)先证明空间，未过关前不随机化。

## 边界与参数

MIS-009 · PROPOSED · 来源：本轮系统扩写。

任务物不允许丢到不可达处软锁；确实毁坏时必须走设计过的失败/降级，不隐形再生。两人同完成目标只有一次推进。断线不能留“必须该玩家才可开”的控制锁。主线必须支持单人顺序执行，不靠强制Bot同时按开关。层图大小、步行速度、必要资源预算属模板TEST，暂无统一全球数值。

## 示例

MIS-010 · PROPOSED · 来源：本轮系统扩写。

正常：Maintenance是低弹耗长路线，Security是短且高爆发成本；两路前方重接。失败：生成出的Coupler在需Coupler开启的门后，验证拒绝seed。跨系统：选Vault并未直接提高敌人血量，而是释放具体Ingress和增加资源，风险/回报同一次选择可见。

## 验证与 OPEN

MIS-011 · TEST · 来源：本轮实验建议。

固定图所有目标从开局走到结束；枚举Cart与关键任务状态组合，保存失败seed与原因；20个随后生成seed做人工无聊/公平排名。地图随机性、玩家技术分布和资源保守估计不能仅用图算法宣布通过。
## Predator Reversal、Breach 与 Forward Rejoin 细化

MIS-012 · DIRECTION · 来源：SRC-USER-2026-09-04-ORDNANCE-MISSIONS；继承语法SRC-SSOT-2.0 §13.5、§15.2。
用户希望前期只能躲/诱导/打断/破部位的Threat，经Terminal/环境理解规则、trap/seal/power/vent临时控制，再前向获取改变capability的武器/装置，通过新通道/运输/敌人突破快速重接，从猎物变猎人。终点可kill/dismember/permanent contain，不是取枪后十分钟原路返程。

MIS-013 · PROPOSED · 来源：本轮任务扩写。
Predator状态：Hunting→Identified→ContainedTemporarily→CounterCapabilityAcquired→Rejoined→Reversed。每态声明真实能力、可用反制、出口与失败后果；前期“不能永久杀”不等于打它完全无效。临时控制失败让它沿已知可行路径推进，不能凭空teleport或免疫先前全部攻击。反制装置使部分装甲/再生/移动机制可处理，而非隐藏CanKillBoss=true。

Breach/Tool Hunt流程：看见阻碍与后方可达目标→选择维护区取反结构炮/恢复切割机/冒险通风→各路线在障碍后前向汇合。重武器快速且消耗团队资产，旁路更慢/更险但保持主线可行。若武器可以被提前用尽，验证必须在零Ammo状态也存在成功路线；禁把跑腿和数学无解伪装成严厉难度。当前BLACKSTART只试一个小Breach分支，不顺便制作完整Predator模板。

## 设施网络恢复与字形改线任务

MIS-014 · DIRECTION · 来源：SRC-USER-2026-09-05-CARRIER-REBOOT-PHYSICAL-RECOVERY；SRC-USER-2026-09-05-LIMITED-NODE-DEFENSE-ASSETS。

设施网络恢复模板采用`Route Evidence→Glyph Route→Insertion→Terminal Uplink→Carrier Read→Protocol Rewrite→Identity Verify→Facility Control→World Payoff`。步骤可以被关卡前向交错，不能退化成连续八次读条。至少一个中段结果必须改变本局实际局势：恢复门控、显示合法路线、开放资源库，或使仍受设施控制的炮塔和机器人从隔离/敌对转为友军。该合同结算设施情报与资源，不向基础游戏提交节点进度；节点长期恢复仅在Descent发布联合行动中统计。

限界探索区模板偏向“先夺控制权，后用设施打赢”：弹药、医疗、备用电源、炮塔和机器人较多，但入网前自动防御可能是额外威胁。无限探索区模板偏向“少补给穿过高风险路线，带回更多长期价值”：虚空兽密度与合法迁入源更多，固定防御较少，废料、材料、字形知识和筑路者资料更丰富。二者不是简单难度倍率；同等难度下必须通过不同资源和世界动词区分。

MIS-015 · DIRECTION · 来源：SRC-USER-2026-09-05-OPTIONAL-GLYPH-REROUTES；SRC-USER-2026-09-05-REGION-RISK-REWARD-PROFILES。

可选字形改线只连接模板预先声明的隐藏仓库、维修空间或支路。玩家先通过合法证据取得备用序列，再决定是否占用路线、投入Power/时间或打开额外ThreatIngress。奖励可为当局物资、可撤离废料、外观信用点资格、成就条件、外观物品、字形知识或筑路者资料；重要奖励须与新增敌人或其他可读代价同一事务提交。秘密内容不得成为主线唯一解，也不得要求玩家盲猜、查Wiki或穷举无反馈序列。

## 程序Operation与任务板合同

MIS-016 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-PROCEDURAL-OPERATION-HUB-BOARD；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY；模式入口见[Operation OPS-011](operations.md)。

基础游戏的程序内容只使用三层：`RegionProfile`定义无限区、限界区等历史与资源倾向；`MissionSite`定义本局设施主题和环境条件；`MissionInstance`由固定Seed生成并在结算后销毁。界桥节点只存在于作者层世界观，不进入基础任务生成参数、玩家地图或永久进度。基础游戏不维护账号剧情阶段，普通合同也不需要为每局编造一个永久世界坐标。

生成采用手制模块与程序组合，而不是让算法凭空发明房间。推荐管线为：

`RegionProfile → FacilityTheme → PrimaryTemplate → compatible Secondary → Situation/Modifiers → handcrafted Cluster Graph → objective/resource placement → enemy ingress → solvability validation → MissionSeed lock`。

任务板上的随机性是玩家决策前已经揭示的输入随机：玩家先看到主任务、支线、区域、已知危险和奖励，再决定装备与难度。地图内部结构、未侦察敌人和部分资源位置可以保持未知。主任务与支线必须通过兼容矩阵组合；任何组合都要通过可达性、必要资源、单人顺序可解、入口合法、敌人来源和撤离路径验证。随机不等于可以把取任务物放在需要该任务物才能打开的门后，也不允许用纯粹路程延长40–50分钟。

程序池首个目标不是“数量无限”，而是让有限模块产生不同决策。玩家正式游玩的Operation默认都使用程序空间图；特殊事件或故事收藏只允许嵌入语义兼容的手制地标与事件Cluster，不允许因为出现故事房就把整张路线固定成GTFO式背板关卡。灰盒Gate至少需要三个主任务模板、三个可兼容支线、两个区域Profile和足够多的手制Cluster，使测试玩家不能只靠记住模块顺序完成任务；确切房间数量在生产测速后决定，不先承诺大型内容池。失败Seed必须保存完整生成输入以便复现，不得静默重掷成看似成功的地图。

MIS-017 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-OPERATION-MISSION-PORTFOLIO-PCG。

首批生成器使用六个任务族：废料回收、资源取得、技术回收、研究数据、设施网络恢复和威胁处理；每个Offer选一个Primary，并从兼容池选零到一个常规Secondary。Secondary必须改变路线、携带预算、时间暴露、资源选择或撤离条件，不得只是顺路点击若干同类物件。详细任务内容与奖励所有权见[Operation OPS-012](operations.md)和[经济](economy-and-support.md)。

各任务族用不同动词形成可辨识结构：废料回收要求搜索与贪取取舍；资源取得要求供能、装载与运输；技术回收要求保持设备完整并解决权限/物理封锁；研究数据要求恢复、验证并选择上传完整度；设施网络恢复要求译码、身份和本地控制恢复；威胁处理要求追踪、操纵空间并封锁、捕获或击杀。若三个以上任务族最终都收束成同一处静止防守读条，任务池判定失败。

“每局是新体验”按决策差异验证，不按Seed不同自我宣布。对同一Primary连续生成多组地图，测试队伍应因关键路线、设施系统、支线、资源位置或敌人来源改变计划；只改变房间朝向、走廊长度、装饰和敌人数量不计新体验。生成器保留近期MissionFingerprint并抑制区域、Primary、Secondary、Situation和关键图结构的近似连抽；窗口长度与相似度阈值在内容量测试后确定。

MIS-018 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE；叙事规则见[中央故事STORY-011](central-story-spine.md)。

故事收藏必须绑定语义兼容的手制Cluster：研究人员记录只出现在其工作、居住或撤离路径，武器来源只出现在相关军械/试验场景，事故痕迹必须与设施状态和尸体位置互相解释。生成器可以改变该Cluster在合法图中的位置、进入成本、敌情和支路，但不能把关键线索随机撒进无关房间。一个收藏组的必要片段必须在长期正常游玩中可重复获得；不得被单个Seed、失败即绝版或限时活动永久锁死。多人队伍中，一名玩家确认收藏后，为当局所有符合资格且在场的玩家登记发现，不制造抢日志的拾取竞争。
