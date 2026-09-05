---
doc_id: GDD-BUILD
doc_type: gdd
stage: DRAFT
updated: 2026-09-04
owner_role: 构筑系统设计
canon_basis: "SRC-SSOT-2.0 §9、§10、§37、§40"
depends_on: ["combat-and-arsenal.md"]
---

# Relic、Proc、数值与自动 Fusion

## 玩家目的

看懂一次变化为什么发生，主动组合出新的行为；复杂度应让玩家获得控制感，不让队友只能观看无法解释的爆炸。

## 范围与术语

Provider 是提供属性/事件处理器的有效实例；Relic 是通用被动物品域；Synergy 保留原件，Fusion 消费原件并生成新实例，Loop 是因果闭环。事件协议由技术契约落地，本文件负责玩法语义。

## 已确认规则

BLD-001 · CANON · 来源：SRC-SSOT-2.0 §9.1–§9.4。

Relic 局内无限累计，无固定六槽，结束不永久带出。数值加成合法，但必须标 Tag、Zone、SourceScope 和实际受益效果。重要 Proc 输出是一等事件，默认可以继续触发；每个 Trigger 明确接受 Direct/Triggered/Utility/Reaction/Summon/Team/World 等来源，不设置全局禁止 Proc-from-proc。

BLD-002 · CANON · 来源：SRC-SSOT-2.0 §9.4、§10.4。

有时间、弹道飞行、资源/冷却、目标状态或动作节奏推进的循环合法；同一 commit 内零时间、零资源、零状态变化的 A→B→A 非终止循环非法，编译阶段应检测并拒绝或显式重写为周期过程。不设隐藏 Proc depth cap、Boss全局伤害cap或anti-build scaling；高密度优化表示，不删除合法结果。

BLD-003 · CANON · 来源：SRC-SSOT-2.0 §9.5、§37。

Fusion 是自动、确定的 consuming synthesis：条件满足后 A+B→C，A/B独立实例消失，C是真新实例并可继续 C+D→E。最后材料拾取前，未知配方只隐藏结果，必须提示强互动与消耗成本；发现后显示 Known Fusion。继承处理包括 Preserve、Merge、Convert、RebindScope、Promote、明确 Discard，重大损失提前可读。没有Forge、手动合成确认或随机失败率。

BLD-004 · CANON · 来源：SRC-SSOT-2.0 §10.1–§10.3。

Stat pipeline：Base→Weapon/Utility/Ability→Character/Core→Relic→Team/Conditional→Crit→Target DamageTaken→Element/Reaction→Defense。同区加算、跨区乘算；统一Stat Engine编译。暴击率超过100%进入Crit Tiers；Utility/Ability直接伤害默认可Crit，除非该效果明确禁止。Reaction用Tag/Registry定义，世界Medium/Material/Network可参与，跨玩家来源有效。

## 玩家流程

BLD-005 · PROPOSED · 来源：本轮系统扩写。

取得Anchor→看见可连接Tag与受益对象→在拾取最后材料前看将被消费的实例及损失→拾取提交→自动Fusion→简短变化摘要→战后查看根事件/投入转换。玩家选择发生在取得材料前；已合法取得后不再弹出“是否融合”制造第二确认。

## 状态与所有权

BLD-006 · PROPOSED · 来源：本轮系统扩写。

Authority 拥有 BuildRevision、ProviderID、RecipeRegistryRevision、discoveryClaims、event queue及RNG流。每个事件带 eventID、rootID、parentID、ownerPlayer、sourceInstance、sourceScope、tags、target、simulationTime、authorityEpoch。仅同一玩家合法可消费的拥有物进入默认配方；跨玩家融合须配方显式支持并形成独立 SharedDecision，首批内容不采用。

| 当前 | 前置/事件 | 结果 |
|---|---|---|
| Stable | 合法取得新Provider | CandidateGraph，生成收益与消耗预览依据 |
| CandidateGraph | 多配方同时满足 | 进入确定仲裁，不能依赖线程/文件加载顺序 |
| CandidateGraph | 非法零推进循环 | 整笔取得/融合事务拒绝并解释，不吞材料 |
| CandidateGraph | 校验与仲裁成功 | AtomicCommit消费输入、生成输出、更新发现与版本 |
| Stable新版本 | 新输出可继续Fusion | 同事务候选序列继续，逐步校验、记录谱系 |
| Commit已完成 | 重复网络请求 | 返回同一结果，不再次消耗/生C |

## 自动 Fusion 多配方仲裁

BLD-007 · PROPOSED · 来源：本轮系统扩写。

加载内容时拒绝完全相同材料/条件但没有明确优先级的配方冲突。运行时候选按显式 recipe priority→消耗材料种类数降序→namespaced recipeID排序；材料按稳定实例创建序选择。发现状态不参与顺序，避免老玩家账户知识偷偷改战斗结果。

最后材料预览展示当前胜出配方会消费的实例；若并发拾取改变BuildRevision，重新生成预览并让尚未提交的拾取重新确认获取，不能按过期预览吞物。已提交的多个拾取按权威排序逐个融合。循环合成 A→B→A 同样需编译检查；同事务连锁必须有严格减少材料或明确定义的终止秩，否则内容验证失败。

每件输出保存输入谱系与继承映射。规则判定中先创建候选快照，所有改动一起提交；中途异常保持旧Build且物品仍留世界。这是事务原子性，不是游戏失败回滚。

## 模式配置与内容接口

BLD-008 · PROPOSED · 来源：本轮 Operation-first评审。

两模式共用事件、融合与数学语义；奖励密度和可授予能力由公开ruleset/profile控制。Operation候选池的经济边界见[经济](economy-and-support.md)，无限累积是容量规则，不代表每种模式必须无限供给。极端循环先在内部[Combat Lab](../technical/modding-and-toolchain.md)验证，不承诺发布Descent。

内容卡须列 Trigger/Filter/Scope、Cost/ProgressGate、输出事件、继承、RNG、并发优先、目标失效处理、模式准入、玩家反馈。首批[30 Relic与8 Fusion候选](../content/relics-and-fusions.md)不等于最终平衡。

## 边界

BLD-009 · PROPOSED · 来源：本轮系统扩写。

倒地后的已提交事件保留原Owner/Root；Target死亡时按效果声明终止或选合法新目标，不借呈现LOD重掷结果。Source消失后，已提交投射物仍使用提交时合法参数快照；后续新触发按现版本。每个世界反应只消费一次状态对，防双客户端重复Reaction。共享Scan不默认叠乘。断线/迁移连同队列、谱系、RNG、版本恢复。展示聚合不影响贡献/伤害。

## 参数与数学候选

| 参数 | 值/状态 | 来源 |
|---|---|---|
| 首批Relic集合 | 30：约8 Scalar、8 Connector、6 Rule Modifier、4 Transformer、4高交互材料；可重叠 · TEST | SRC-SSOT-2.0 §9.1、§40 |
| Curated Fusion初池 | 6–10 · TEST | SRC-SSOT-2.0 §40、§41.3 |
| Crit Tiers计算 | tier=floor(chance/100)+一次余数概率；每tier增量系数待测 · PROPOSED | 原文只确认超过100%有效，未给公式 |
| UI实时核心链显示 | 最多3条身份摘要 · TEST，非模拟cap | 本轮可读性实验 |

## 示例

BLD-010 · PROPOSED · 来源：本轮系统扩写。

正常：换弹事件使下一枪带电，电击引发状态反应，反应生成合法投射物；每条边都有来源过滤和推进。失败：A触发B、B同commit触发A且无成本/变化，候选图拒绝并指出最小环。跨系统：C由一把枪和回旋材料合成，把Magazine转换成OrbitCount、ReloadSpeed转换ReturnSpeed，预览明示转换；队友不能突然失去自己的武器。

## 验证与 OPEN

BLD-011 · TEST · 来源：本轮实验建议。

重放同种子同输入应得到相同消耗、事件和谱系；覆盖两个重叠配方、两次同时拾取、Fusion中迁移、已提交弹体离体、未知预览、循环编译拒绝。记录非预期后悔率与四人因果复述。仲裁顺序、Crit tier公式、跨玩家Fusion均待批准。
## 最新统一 Modification 候选合同

BLD-012 · PROPOSED · 来源：本轮用户“配件底层统一”讨论；SRC-USER-2026-09-04-MODULAR-REFINEMENT。

统一ModificationDefinition由target_scope、mount_point、compatible_tags、effect_graph、capability_permissions、tradeoffs、stack/conflict_group、visual_asset、mode_allowlist、save/network version组成。presentationKind可为WeaponModule、ToolModule、TeamProtocol或Relic；scope分别指向WeaponInstance、ToolInstance、Team或Player/ProcGraph/World。WeaponModule有实际挂点与外观/动画，TeamProtocol不得伪装成装在单枪上的团队隐形buff。

共用一个Effect schema与事务模型，不建立RelicBase层级或第二套配件效果系统。配件安装先验证目标实例/挂点/冲突/代价，再原子装配；并发替换旧revision拒绝，不吞旧件。Operation推荐profile采用明确安装，不启用BLD-003的自动Fusion；Lab/未来Descent才启用该机制。该模式化修改与源全局融合规则冲突，待[DDD-0004](../governance/decisions/DDD-0004-unified-modification-model.md)批准，不把提案冒充已确定事实。
