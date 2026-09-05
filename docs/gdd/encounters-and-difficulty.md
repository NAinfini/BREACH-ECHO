---
doc_id: GDD-ENCOUNTERS
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 敌人与难度设计
canon_basis: "SRC-SSOT-2.0 §4A.4–§4A.5、§13、§32、§40"
depends_on: ["world-and-information.md", "narrative-bible.md"]
---

# 敌人、遭遇与难度

## 玩家目的

通过敌人的位置、能力和通信判断应打、绕、先改环境或撤退；高手因读懂局势获胜，不能因为AI看穿输入而受罚。

## 范围与术语

Enemy Role描述迫使玩家做的动作；Director选择合法世界压力，Storyteller是节奏policy，Difficulty是挑战参数，Mutator改变公开规则。四者独立。

## 已确认规则

ENC-001 · CANON · 来源：SRC-SSOT-2.0 §4A.4–§4A.5、§13.1–§13.4、§13.7。

不存在通用Persistent Alarm/Alarm等级，开枪不是犯错。压力来自Ambient/local、Horde/Threat Surge、Objective Pressure和具体系统响应。Horde不是无限刷，结束后必须恢复低压；不用全局红表、倒数或通用地震，用阵营叫声/脚步/机械/环境预兆。AI管线Perception→Belief→Group/Cohort→RoleIntent→Action→Motor，有感知与通信范围，不全知、不input-read。

ENC-002 · CANON · 来源：SRC-SSOT-2.0 §13.3–§13.5。

遭遇语法：Pass-through Threat、Guarded Value、System Holder、Escalation Source、Mobile Pressure、Pursuit/Displacement、Combat Payoff、Forced Breakthrough。每个说明为什么打、能否绕/改造、打了改变什么；无统一潜行加成或击杀配额。Predator可前期不能永久杀，但伤害、部位、控制与引诱都应有用，随后获得真实反制能力；其转移有实际路径。

ENC-003 · CANON · 来源：SRC-SSOT-2.0 §32.1、§40；来源属性：INHERITED。

Relaxed、Standard、Veteran、Nightmare、Cataclysm五难度首次启动全部开放，Standard推荐。提高威胁面、协同、变异、环境、资源/复活压力优先于血量海绵；不锁核心内容。PlayerCount、Difficulty、Storyteller分别配置，不暗改玩家属性。

ENC-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-SSOT-2.0 §13.2、§13.6、§32.2–§32.3。

大规模通过Cohort/LOD/群脑表达，技术压力数见[架构](../technical/architecture-and-performance.md)。Spawner/Constructor是公共能力，靠生态和资源行为差异，不无限做Mom换皮。Storyteller不用实时LLM做不可复现决策；历史Commander/Butcher/Sadist/Madman/Architect/Survivor/CHAOS仅候选。Black Swan独立低概率RNG、可恢复、不进全收集要求。Daily/Challenge可固定seed/rules/content；奖励优先cosmetic/history，无FOMO。

## 玩家流程

ENC-005 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

听到/发现来源→判断Threat Role→选进入路线与首要目标→交火/操纵系统→来源被消除或压力预算结束→确认低压→推进。关卡不靠不断加敌人填空，敌人数量必须有当前场景的具体作用。

## 状态与所有权

ENC-006 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

Authority持有每个来源的可用budget、已生成实体、ingress许可、阵营Belief、communication scope、RNG流和cooldown。一个单位分享的是它知道的有限事实及置信/时间，不共享玩家客户端信息。

| 起点 | 条件 | 结果 |
|---|---|---|
| Ambient | 真实来源触发/目标启动 | Telegraph，暴露可感知预兆 |
| Telegraph | 合法入口可用且budget足 | Surge，按来源生成 |
| Surge | 波预算耗尽/来源失效 | Decay，停止该来源新生成 |
| Decay | 现存威胁被清/离开 | Quiet，不补齐“应有敌人量” |
| Quiet | 新世界事件真实成立 | 新压力过程；无“太安静”事件 |
| SourceSealed | 无合法Breach能力 | 保持封锁，不穿墙生成 |

## 模式配置与内容接口

ENC-007 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

Operation强调高低压与任务状态；Lab/Descent强化持续可读的战斗回报。Role卡声明感知、通信、动作前摇、目标偏好、成本、反制、部位功能、声形提示、禁用生成点。首批角色实例归[战斗原型](../content/combat-prototypes.md)。

## 边界与参数

ENC-008 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

封闭所有合法入口后不刷敌；若目标依赖击杀则验证任务不会因此软锁。玩家断线按剩余有效玩家数改变未来pressure预算，不删除已在场敌人；具体缩放待测。迁移保留Belief、源预算、队列与RNG。召唤物重复请求按source spawn事务去重。五档初值采用测试参数TP-DIFFICULTY-COMBAT；敌人基础HP/伤害/感知不随难度暗变，以有限来源规模、组合、普通补给和环境决策变化难度。所有初值待试玩，不以“最高难”直接推导更多血量。

## 示例

ENC-009 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

正常：Scout发现队伍并成功通信才引来响应，先切传感器可阻断。失败：所有入口被Seal，Director没有合法来源，必须安静，不能生隐形传送兵。跨系统：开启Research Vault释放一个前方可见来源，Finale新增侧翼，因果能被玩家指出。

## 虚空兽与节点供能

ENC-011 · CANON · 来源：SRC-USER-2026-09-05-VOID-ECOLOGY-AND-EXTERNAL-USERS；SRC-USER-2026-09-05-POWER-DOES-NOT-INSTANT-WAKE；SRC-USER-2026-09-05-VOIDBEAST-ACCUMULATED-POPULATION；世界事实见[世界观NAR-027](narrative-bible.md)。

虚空兽将供能中的节点视为食物源和迁徙信标。节点断能时，现有活体逐步进入休眠，不能繁殖或跨越已关闭路线；恢复供能会解除强制休眠条件，并允许其他节点中的活体沿开放路线迁入，但不会让本地个体立即全部醒来。休眠个体保留独立唤醒阈值，只有接近、噪声、接触、伤害、突发功率或持续暴露等局部刺激达到阈值后才进入警觉或活动状态；初版采用接触/伤害立即唤醒、局部声能累积达到阈值唤醒；单纯恢复稳定供电不立即唤醒，数值见测试参数。

因而Power操作同时产生收益和长期威胁：恢复灯光、交通或任务设备，也会先提高既有休眠体苏醒与外部迁入风险，并在更长生态时间尺度上允许繁殖；它本身不等于立即进入战斗。已供电房间仍允许小队观察休眠体、控制动作和噪声、选择潜行或主动清场。单次Operation内的压力来源必须优先是已记录休眠体和合法迁入，不能用“繁殖”解释短时间凭空补怪。

该规则不得成为Director凭空刷怪的借口。关卡状态必须分别记录本地休眠个体和外部合法迁入来源；玩家清除全部本地个体且封闭所有供能入口后，该节点必须永久保持清洁。重新供能前应能通过尸骸、取食痕迹、异常能耗、低代谢生命信号或设施记录获得至少一种风险提示。具体慢速繁殖周期、休眠唤醒时间、能量感知距离与迁入预算仍需原型测试。

ENC-012 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-USER-2026-09-05-LIMITED-NODE-DEFENSE-ASSETS；SRC-USER-2026-09-05-NODE-CLEARANCE-AND-PLANETARY-DESCENT。

限界探索区的自动防御在设施协议恢复前按本地旧权限行动，可以与虚空兽同时形成夹击，但不得默认互相无视：炮塔和机器人必须依各自感知、目标分类和旧命令选择目标。合法协议重写并取得设施控制后，仍受本地系统控制的完整防御在本局切换为玩家阵营，保留当时弹药、损伤和位置，不免费修满或凭空生成。该转换是夺取System Holder后的战术回报，不代表玩家永久取得一个节点。

基础Operation只结算本局MissionInstance，不维护玩家可见的节点清场账。世界观仍允许有限节点被真正清除；该概念只在Descent发布联合行动及其公共历史中进入玩家层。真实行星端点后的虚空兽生态、灼星种领土或借尸者占领区可作为Descent的持续来源；每次Run必须代表新的行动区域或任务，不能把同一个已清房间重新填满再称为正史。

## 验收与尚未实测项

ENC-010 · TEST · 来源：本轮实验建议。

每遭遇至少两种合理解法；20次固定seed重放无未经授权spawn；静默客户端不向AI泄漏输入；关掉声音后仍可通过合法替代提示识别高压。初版只交付一个设施状态驱动Director，不实现七套命名Storyteller。Black Swan与Daily排行榜事件后置；难度、密度和唤醒初值见测试参数，均待试玩。


## 本次定稿：执行边界

首批用Runner/Suppressor，随后Holder/Scout/Flanker；AI只基于合法感知/记忆/通信，Source存量有限。五档难度全部可选，组合、资源与环境约束先变，禁止动态读玩家Build加抗性。无来源spawn、被封Ingress偷刷新、无意义HP海都是否决条件；数量/声距按战斗试制与种子预算实测。

Authority: delegated，SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018。所有未提供实测的参数与验证仍为TEST；未展开的未来功能不在当前实现关键路径。
