---
doc_id: TECH-ARCH
doc_type: technical
stage: DRAFT
updated: 2026-09-05
owner_role: 架构负责人
canon_basis: "SRC-SSOT-2.0 §1.5、§22–§23、§29；SRC-USER-2026-09-05-UNITY-ENGINE-LOCK；SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST；SRC-USER-2026-09-05-TICK-ARCHITECTURE"
depends_on: ["modding-and-toolchain.md", "../governance/decisions/DDD-0008-engine-unity6.md", "../governance/decisions/DDD-0011-tick-architecture.md"]
---

# 模拟架构与性能合同

## 目的与边界

为当前Operation提供可测量、可恢复、可扩展的模拟。**引擎已锁定Unity 6，正式渲染管线锁定URP，Gameplay默认采用GameObject/MonoBehaviour。** 本文仍是TDD契约草案，尚未实现完整系统、跑完整benchmark或证明跨平台确定性。

ARC-001 · CANON · 来源：SRC-SSOT-2.0 §1.5、§22.1、§22.6、§23.1–§23.4。

Cardinality/Topology/Capability是数据：官方槽位不渗透Save/Network/UI/Entity。Simulation performance优先；可降VFX/audio voices/远处表示/动画细节，不能暗删合法伤害、承诺敌人数、投射物/Proc/Summon结果。实体由components/profiles/tags组合；AnatomyGraph支持0..N部位、稳定ID、拓扑、命中体、完整度/装甲与增删/再生/转换，能力从图编译供热路径读取。

ARC-002 · DIRECTION · 来源：SRC-SSOT-2.0 §22.2–§22.5。

候选ECS/archetype/chunk/SoA、hot/cold split、index+generation handle、稳态热路径近零general heap分配；TaskGraph/DAG、worker-local buffer、deterministic commit；Command/Event/Transaction分离；脏依赖增量编译；批量Projectile/query、游戏物理与表现物理分离、层级空间/导航/flow/cohort；AOI/delta/dirty mask、共享语义schema、snapshot+journal、semantic RNG。以上只是高负载系统可采用的技术方向，不构成默认DOTS要求。

## 通用接缝与真实消费者

ARC-003 · PROPOSED · 来源：SRC-USER-2026-09-04-MODULAR-REFINEMENT；本轮架构评审。

Kernel拥有Action/Entity/Damage/Effect/Tag/Stat/Reaction与提交序；不引用Operation专属Terminal类型、BLACKSTART目标或Descent层数。Ruleset提供Run lifecycle、合法内容池、ResourcePolicy、RewardSource/cadence、MapGrammar、failure policy。Operation是首个实际消费者，内部10分钟Combat Lab是第二个低成本契约测试，不提供Roguelike专用接口或发布功能。

ContentPackage通过能力接口声明内容；核心服务有清楚边界，但不承诺任意替换物理/网络authority/序列化即可继续运行。禁止每个小对象做插件、全局event bus隐藏依赖或散落if(operation)分支。模式差异通过已显式调用的policy表达；未被两个实际消费者或当前内容需要的扩展点不添加。

## 数据所有权与提交流程

ARC-004 · PROPOSED · 来源：本轮技术扩写。

输入Command→权限/前置校验→候选状态与成本→确定顺序Commit→事实Event→后续规则处理→Snapshot/Journal→网络/表现投影。每个事务持有输入revision、幂等ID和结果；事件说明已发生事实，不能作为未经校验的万能写入口。批处理保留原语义与贡献，不只保留总DPS。

| 阶段 | 输入/输出 | 失败处理 |
|---|---|---|
| ContentLoad | pin后的包→验证过registry | 不支持schema/能力冲突则停止进入 |
| Compile | graph→可执行规则 | 零推进环/歧义配方报定位错误 |
| Simulate | command+state→candidate | 资源/权限不足明确拒绝 |
| Commit | candidate→新revision+journal | 原子，不发布半个Fusion/Cart |
| Replicate | 已提交状态→客户端视图 | 可重发，不重新执行语义 |
| Present | 已知事实→画面声音 | 可降级密度，canonical不变 |

## 参数、引擎与性能计划

ARC-005 · TEST · 来源：SRC-SSOT-2.0 §22.7、§29.2、§40。

源压力目标保留：1k/2.5k/5k AI、10k projectiles、50k projectile torture、动态anatomy/多tentacles、4人高utility/proc/God Build、未来大Mod压力、Deck thermal soak、战斗中host migration。它们是TEST benchmark，不是已证明规模或市场承诺。真实可见/高精度AI数量应由灰盒实际玩法定义，不能把5000当必须生产5000只怪。

ARC-006 · CANON · 来源：SRC-USER-2026-09-05-UNITY-ENGINE-LOCK；决策见[DDD-0008](../governance/decisions/DDD-0008-engine-unity6.md)。

**BREACH: ECHO正式锁定Unity 6。** 后续架构、工具、资产、网络和构建流程可针对Unity优化，不再承担Unreal兼容责任。改引擎属于新的高返工成本SUPERSEDING决策。

ARC-007 · LEGACY/SUPERSEDED · 来源：SRC-SSOT-2.0 §29.2；SUPERSEDED BY ARC-006。

旧基线要求用同一Prototype对Unity与Unreal作同级比较后再锁引擎。该比较原则已完成产品决策使命，不再要求生产两套引擎原型。仍保留其测量思想：任何Unity技术选择都必须通过代表性场景、硬件、构建配置和可重复日志验证，而不是靠营销结论。

ARC-008 · PROPOSED · 来源：本轮技术评审；按Unity锁定调整。

先固定玩家场景与日志，再比较Unity内部具体实现：网络方案、导航/空间查询、Projectile表示、序列化、Job/Burst热路径等。记录hardware、build配置、包hash、帧时间分位、sim时间、分配、网络带宽、温度与可视密度。超过预算必须调整公开范围或算法并复测，不偷偷减少真实结果。

ARC-010 · CANON · 来源：SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST。

**GameObject/MonoBehaviour是默认实现。** 新系统首先使用常规Unity结构实现，以开发速度、Agent可理解性、调试和资产兼容为优先。只有Profiler/Profile证明某具体系统在真实目标负载下成为显著CPU/内存瓶颈，并且DOTS/Entities/Burst/Jobs有清楚收益时，才迁移该系统或热路径。迁移应保持对上层Gameplay合同稳定，不允许把“未来可能需要高性能”当成提前ECS化整个项目的理由。

典型的DOTS候选可能包括高数量Enemy simulation、Projectile、Status/Reaction、Proc/Effect热路径、空间查询或Horde bookkeeping；这些只是候选，不是预分配所有权。Player、Viewmodel、Camera、UI、菜单、Hero交互、普通Door/Terminal/任务对象同样不因类别而永远禁止迁移，最终以Profile证据为准。

ARC-011 · CANON · 来源：SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST。

**正式Render Pipeline为Unity 6 URP。** HDRP不建立并行资产或兼容管线。正式材质、Shader、VFX、Lighting、Fog、Decal、LOD和资产采购以URP为唯一生产基线。URP仍需在Stylized Industrial Realism真实场景中接受GPU frame time、memory、shader variant/build成本、战斗可读性和Steam Deck thermal soak测试；测试用于优化URP实现，不再把HDRP当默认备份方案。

ARC-012 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE；详见[DDD-0011](../governance/decisions/DDD-0011-tick-architecture.md)。

**Simulation采用固定60 Hz authority timebase，但整体架构必须multi-rate。** Render FPS、Network Replication、AI Brain和Dormant/background对象不与60 Hz强绑。AI高层思考默认约5–10 Hz并stagger/time-slice，当前Intent的移动/碰撞/攻击时序继续由60 Hz Authority执行；关键玩家/Boss状态约30 Hz复制方向，其余AI按重要性降频并可Dormant/Event-driven。Gameplay Physics默认与60 Hz Authority对齐，但不要求每个Physics Actor 60 Hz发送Transform。

Fixed-step loop必须限制catch-up工作量，不能无限追赶导致spiral-of-death。过载时允许先推迟低优先AI Think、background simulation、low-priority replication与cosmetic工作，禁止通过“优化”丢弃已经合法发生的Damage、Proc、Gameplay Physics、资源或任务结果。60 Hz tickrate是Gameplay/Protocol基线，不是普通Server配置项；Mod Gameplay时间基于SimulationTime/seconds/events而非Render FPS。

该条不是性能已通过的声明。60 Hz Authority必须在目标Host硬件、4人网络、高utility/proc、Projectile压力与代表性敌人数下通过Profiler/thermal soak；若失败，应优化热路径、调度、数据布局或公开规模，而不是偷偷改变Gameplay结果。

## 内容接口、边界与验证

ARC-009 · PROPOSED · 来源：本轮技术扩写。

每能力声明读写集合、成本/时序、可重放状态、权限和故障归属；Mod耗时可归因，安全故障停止该受影响会话并给诊断，不继续伪成功。跨平台bitwise determinism目前未证明；服务器权威与可重放有序语义不自动等于物理跨CPU完全一致。

验证 Operation和Lab各消费同一Damage/Effect/Package/Save schema；替换mode package不用改Kernel源码；两个不同部位拓扑敌人支持相同命中协议；表征优化前后结果账一致。Unity首个技术Spike至少覆盖玩家+一把枪、100/500/1000轻量敌人、Projectile压力、基础Reaction/Effect、4人网络、Host loss恢复、一个Facility模块和一次购入资产导入。Tick架构Spike需记录60 Hz sim frame budget、catch-up次数、AI cohort耗时、replication bytes/sec、packet rate、Dormant savings、Projectile网络成本和不同Render FPS下Gameplay一致性。所有性能检查尚未运行。
