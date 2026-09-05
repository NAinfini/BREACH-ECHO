---
doc_id: GDD-BUILD
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 构筑系统设计
canon_basis: "用户确认的 Operation-first 方向；统一 Modification 决策"
depends_on: ["player-and-input.md", "../governance/decisions/operation-field-modifications.md", "../governance/decisions/unified-modification-model.md"]
---

# 统一修改与效果系统

## 单一责任

本文档只定义武器配件、工具模块、战术模块与未来 Relic 如何共用一套数据和效果语义。基础版可发布的具体内容池由[改装目录](../content/modification-catalog.md)负责，入场槽位由[玩家与输入](player-and-input.md)负责，数值由[战斗平衡](../content/combat-balance.md)负责。

## Operation 基线

BLD-001 · CANON · 来源：用户确认的 Operation-first 方向与[局内改装决策](../governance/decisions/operation-field-modifications.md)。

Operation 每人带入两把枪、一件工具和一个可自由选择的个人战术模块。局内只提供有限、可读、需要明确安装的 Modification；不启用无限 Relic 累积、自动 Fusion、Staff 或无限弹药效果。这是当前产品规则，不得因旧 SSOT 的 Roguelike 设计而建立第二套运行路径。

BLD-002 · DECIDED · 来源：[统一修改模型决策](../governance/decisions/unified-modification-model.md)。

所有修改共用 `ModificationDefinition`：`id`、`presentation_kind`、`target_scope`、`mount_point`、`compatible_tags`、`effect_graph`、`capability_permissions`、`tradeoffs`、`stack/conflict_group`、`visual_asset`、`mode_allowlist` 与存档/网络版本。`presentation_kind` 只决定呈现与安装方式，不偷偷授予额外能力。

| 呈现类型 | 合法目标 | Operation 状态 |
|---|---|---|
| Weapon Module | 具体 WeaponInstance 的挂点 | 可用；必须有外观/动作反馈 |
| Tool Module | 具体 ToolInstance | 可用；不得绕过工具资源 |
| Tactical Module / Team Protocol | Player 或 Team | 可用；不得伪装成单枪配件 |
| Relic | Player / ProcGraph / World | 不进入 Operation 内容池；仅 Lab/FUTURE |

## 安装、所有权与权威

BLD-003 · DECIDED。

拾取只创建候选；安装时由 Authority 在同一事务中校验玩家所有权、目标实例、挂点、兼容 Tag、冲突组、模式准入和代价。成功时一次性替换并增加 `BuildRevision`；任一校验失败时不吞旧件、不生成新件。重复网络请求返回原结果，过期 revision 被明确拒绝。

BLD-004 · DECIDED。

团队不能默默改写队友私有装备。任何跨玩家消耗或替换都需独立 SharedDecision 合同；基础内容不使用这类效果。玩家倒地或来源实例销毁后，已提交的投射物/事件使用提交时快照；后续触发使用当前版本。

## 效果图语义

BLD-005 · DECIDED。

每个效果声明 Trigger、Filter、SourceScope、Cost/ProgressGate、Target、RNG stream、输出事件、目标失效处理和玩家反馈。事件带 `event_id`、`root_id`、`parent_id`、`owner_player`、`source_instance`、`tags`、`simulation_time` 与 `authority_epoch`，使因果、战报和恢复可追溯。

BLD-006 · DECIDED。

有时间、弹道飞行、资源/冷却、目标状态或动作节奏推进的循环可以合法；同一 commit 内零时间、零成本、零状态变化的非终止环必须在内容编译阶段拒绝。不用隐藏 Proc-depth cap 或 Boss 自适应减伤掩盖错误因果图。

BLD-007 · DIRECTION。

数值通道只有一套：`Base → Equipment → Character/Core → Modification → Team/Conditional → Crit → Target DamageTaken → Reaction → Defense`。同区加算、跨区乘算；具体顺序和 Crit 公式在第一批内容实作时用单元测试冻结，不建第二个 Stat Engine。

## 未来 Descent / Combat Lab

BLD-008 · FUTURE · 来源：旧 SSOT Roguelike 设计。

Relic 无限累积、Proc-from-proc、Crit Tiers 和自动确定 Fusion 仅作为未来规则集候选。它们可以复用 `ModificationDefinition` 和事件协议，但不得因此进入 Operation 奖励池或迫使基础版实现 Fusion UI、配方仲裁与谱系存档。只有 Descent 通过独立制作 Gate 后才把这些候选升为正式系统。

## 验证

BLD-009 · TEST。

基础测试覆盖：相同种子和输入得到相同效果；同时拾取与替换不复制/吞噬道具；无权限、错挂点、冲突组、过期 revision、非终止环和越界 capability 全部可诊断拒绝；断线/主机迁移后 `BuildRevision`、已提交事件、RNG 和所有权一致。游玩测试记录“改装前后差异能否被玩家复述”和“是否出现无脑上位选项”，不用文档代替实测。
