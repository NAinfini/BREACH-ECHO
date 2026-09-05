---
doc_id: GOV-DECISIONS
doc_type: governance
stage: BASELINE
updated: 2026-09-05
owner_role: 文档与设计治理负责人
canon_basis: "本轮用户确认；现行描述性决策记录"
depends_on: ["authoring-guide.md"]
---

# 当前决策登记

本文件只负责索引当前决定，不复制各系统规则。文件名和内部 `doc_id` 都使用可读的主题名称；设计与技术的现行规则以各责任文档为准，决策文件记录为什么这样选、拒绝了什么、何时需要重审。

| 决策 | 状态 | 决策记录 | 现行责任文档 |
|---|---|---|---|
| 基础版模式 | CANON | [Operation 与 Roguelike](decisions/operation-vs-roguelike.md) | [愿景](../gdd/game-vision-and-design-pillars.md)、[Operation](../gdd/operation-game-mode.md)、[Descent](../gdd/descent-future-game-mode.md) |
| 模块化边界 | CANON/DIRECTION | [模块化产品架构](decisions/modular-product-architecture.md) | [架构](../technical/architecture-and-performance.md)、[Mod 工具链](../technical/modding-and-toolchain.md) |
| 入场配装与局内改装 | CANON | [Operation 局内改装](decisions/operation-field-modifications.md) | [玩家与输入](../gdd/player-and-input.md)、[修改系统](../gdd/field-modifications-and-effect-system.md) |
| 统一修改数据模型 | CANON/DIRECTION | [统一修改模型](decisions/unified-modification-model.md) | [修改系统](../gdd/field-modifications-and-effect-system.md) |
| 团队重资产 | CANON/DIRECTION | [团队重资产](decisions/team-ordnance.md) | [战斗与武器](../gdd/combat-and-arsenal.md) |
| Predator 与破障任务 | CANON/DIRECTION | [Predator 与破障任务](decisions/predator-and-breach-missions.md) | [任务与空间](../gdd/missions-and-spaces.md) |
| 唯一客观正史 | CANON | [单一客观正史](decisions/single-canonical-story.md) | [故事总览](../gdd/story-overview.md)、[叙事圣经](../gdd/canonical-world-history-and-lore.md) |
| 引擎与渲染 | CANON | [Unity 6 与 URP](decisions/unity-engine-and-rendering.md) | [技术栈](../technical/unity-steam-and-modding-technology-stack.md)、[视觉方向](../gdd/art-direction.md) |
| Agent-first 与内容包 | CANON/DIRECTION | [Agent-first Mod Runtime](decisions/agent-first-modding-runtime.md) | [Mod 工具链](../technical/modding-and-toolchain.md) |
| 权威与 Gameplay Command | CANON/DIRECTION | [Host Authority](decisions/host-authority-and-gameplay-commands.md) | [网络与持久化](../technical/network-and-persistence.md) |
| 固定时基与分频 | CANON/DIRECTION | [固定 Tick 与多频模拟](decisions/fixed-tick-and-multirate-simulation.md) | [架构与性能](../technical/architecture-and-performance.md) |
| 状态复制 | CANON/DIRECTION | [状态复制](decisions/state-replication.md) | [网络与持久化](../technical/network-and-persistence.md) |
| 延迟补偿 | CANON/DIRECTION，参数 TEST | [服务器回溯](decisions/lag-compensation-and-server-rewind.md) | [技术栈](../technical/unity-steam-and-modding-technology-stack.md)、[网络与持久化](../technical/network-and-persistence.md) |
| Steam 联机与主机恢复 | CANON/DIRECTION，参数 TEST | [网络运行与恢复](decisions/network-runtime-and-recovery.md) | [技术栈](../technical/unity-steam-and-modding-technology-stack.md)、[主机迁移](../technical/host-migration.md) |
| Steam Workshop 与安全 Mod | CANON/DIRECTION，Luau 发布需 Spike | [Steam Workshop Mod Runtime](decisions/steam-workshop-mod-runtime.md) | [Mod 安全](../technical/mod-security-and-sync.md)、[Mod Manager](../gdd/mod-manager.md) |

## 当前仍需所有者决定

只保留会改变创作身份、真实支出、账号授权或明确需求的事项，见[所有者决策队列](project-owner-decision-queue.md)。普通库选择、格式、实现参数与测试阈值由负责 Agent 提出并用证据验证，不反复要求所有者替技术负责人投票。

## 变更规则

若新证据推翻决定，直接修改或新增一个描述性命名的决策文件，并在本表标出替代关系。不要创建 `final-v2`、带流水号前缀的新文件、平行 SSOT 或兼容旧结论的双轨文档。历史由 Git 保存；当前树只保留当前可执行结论。
