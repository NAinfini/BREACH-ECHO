---
doc_id: GDD-BUILD
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 构筑系统设计
canon_basis: "SRC-SSOT-2.0 §9、§10、§37、§40"
depends_on: ["combat-and-arsenal.md"]
---

# 修改、效果、数值与模式隔离

## 玩家目的

看懂一次变化为什么发生，主动组合出新的行为；复杂度应让玩家获得控制感，不让队友只能观看无法解释的爆炸。

## 范围与术语

Provider 是提供属性/事件处理器的有效实例；Relic 是通用被动物品域；Synergy 保留原件，Fusion 消费原件并生成新实例，Loop 是因果闭环。事件协议由技术契约落地，本文件负责玩法语义。

## 已确认规则

BLD-001 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

官方Operation只注册允许的WeaponModule、ToolModule与TeamProtocol，有限挂点同位替换，不累计通用Relic。数值与事件声明Tag、Zone、SourceScope和目标；重要Proc是一等事件，默认可被明确允许的后续节点消费。Lab/FUTURE才可开启无限Relic容量，容量不等于无限供给。

BLD-002 · CANON · 来源：SRC-SSOT-2.0 §9.4、§10.4。

有时间、弹道飞行、资源/冷却、目标状态或动作节奏推进的循环合法；同一 commit 内零时间、零资源、零状态变化的 A→B→A 非终止循环非法，编译阶段应检测并拒绝或显式重写为周期过程。不设隐藏 Proc depth cap、Boss全局伤害cap或anti-build scaling；高密度优化表示，不删除合法结果。

BLD-003 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

Operation使用明确安装事务，不自动Fusion，不设Forge合成玩法。Lab/FUTURE可开启自动、确定的consuming synthesis A+B→C：预览消费对象与重大损失，未知只隐藏结果，继承Preserve/Merge/Convert/RebindScope/Promote/显式Discard，原件消失、新实例可继续合成。此隔离覆盖原来把自动Fusion当全局默认的表述。

BLD-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

Stat顺序为Base→装备/动作→角色Core（官方四人不设固定战力差）→已安装Modification/允许的Lab Relic→Team/Conditional→Crit→Target DamageTaken→Element/Reaction→Defense。同区加算、跨区乘算。初始暴击公式：tier=floor(chance/100)+Bernoulli((chance mod100)/100)，倍率=1+tier×(critMultiplier−1)，基础critMultiplier=2为TEST；chance需非负且有限。伤害/抗性/装甲路由由可验证定义执行，不使用隐藏Boss cap或随Build暗增抗性。Reaction以Tag/Registry定义，每一状态对消费一次。

## 玩家流程

BLD-005 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

Operation：找到兼容模块→预览目标、挂点、代价和被换下实例→在维护点安装→Authority原子切换Provider→旧件留合法世界位置→反馈行为变化。Lab自动合成另按BLD-003流程，不能把其拾取即消费UI复制到Operation。

## 状态与所有权

BLD-006 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

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

BLD-007 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

加载内容时拒绝完全相同材料/条件但没有明确优先级的配方冲突。运行时候选按显式 recipe priority→消耗材料种类数降序→namespaced recipeID排序；材料按稳定实例创建序选择。发现状态不参与顺序，避免老玩家账户知识偷偷改战斗结果。

最后材料预览展示当前胜出配方会消费的实例；若并发拾取改变BuildRevision，重新生成预览并让尚未提交的拾取重新确认获取，不能按过期预览吞物。已提交的多个拾取按权威排序逐个融合。循环合成 A→B→A 同样需编译检查；同事务连锁必须有严格减少材料或明确定义的终止秩，否则内容验证失败。

每件输出保存输入谱系与继承映射。规则判定中先创建候选快照，所有改动一起提交；中途异常保持旧Build且物品仍留世界。这是事务原子性，不是游戏失败回滚。

## 模式配置与内容接口

BLD-008 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

共享事件/数学/事务，但Operation禁用自动Fusion/无限Relic与ResourceMint能力。Lab是按需验证规则接缝的内部测试场，不是必须先做完30Relic才能开始M2。内容字段为Trigger/Filter/Scope、成本/推进、输出、继承、RNG、并发、失效、模式准入和反馈。目录保留未来样本但明确不进入Operation。

## 边界

BLD-009 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

倒地后的已提交事件保留原Owner/Root；Target死亡时按效果声明终止或选合法新目标，不借呈现LOD重掷结果。Source消失后，已提交投射物仍使用提交时合法参数快照；后续新触发按现版本。每个世界反应只消费一次状态对，防双客户端重复Reaction。共享Scan不默认叠乘。断线/迁移连同队列、谱系、RNG、版本恢复。展示聚合不影响贡献/伤害。

## 参数与数学候选

| 参数 | 值/状态 | 来源 |
|---|---|---|
| 首批Relic集合 | 30：约8 Scalar、8 Connector、6 Rule Modifier、4 Transformer、4高交互材料；可重叠 · TEST | SRC-SSOT-2.0 §9.1、§40 |
| Curated Fusion初池 | 6–10 · TEST | SRC-SSOT-2.0 §40、§41.3 |
| Crit Tiers计算 | tier=floor(chance/100)+一次余数概率；倍率1+tier×(基础暴击倍率−1)，基础2 · TEST | 原文只确认超过100%有效，未给公式 |
| UI实时核心链显示 | 最多3条身份摘要 · TEST，非模拟cap | 本轮可读性实验 |

## 示例

BLD-010 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

正常：换弹事件使下一枪带电，电击引发状态反应，反应生成合法投射物；每条边都有来源过滤和推进。失败：A触发B、B同commit触发A且无成本/变化，候选图拒绝并指出最小环。跨系统：C由一把枪和回旋材料合成，把Magazine转换成OrbitCount、ReloadSpeed转换ReturnSpeed，预览明示转换；队友不能突然失去自己的武器。

## 验收与尚未实测项

BLD-011 · TEST · 来源：本轮实验建议。

重放同种子同输入应得到相同消耗、事件和谱系；覆盖两个重叠配方、两次同时拾取、Fusion中迁移、已提交弹体离体、未知预览、循环编译拒绝。记录非预期后悔率与四人因果复述。仲裁顺序采用BLD-007，Crit公式采用BLD-004；跨玩家Fusion首版不支持，Lab扩展需新决策与共同消费授权。
## 最新统一 Modification 候选合同

BLD-012 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

采用唯一ModificationDefinition：target_scope、mount_point、compatible_tags、effect_graph、capability_permissions、tradeoffs、stack/conflict_group、visual_asset、mode_allowlist、schema version。presentationKind区分WeaponModule/ToolModule/TeamProtocol/Relic，不建立平行RelicBase效果引擎。枪的handling/behavior是逻辑槽，具体Receiver/Optic/Underbarrel/Magazine为视觉挂点；同逻辑槽冲突先于视觉位置。安装验证实例/revision/能力/代价，失败不吞件；TeamProtocol只一个共享协议位，所有人可见，先有效提交，不给Host特权。具体初值见测试参数。
