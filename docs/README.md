---
doc_id: DOC-README
doc_type: index
stage: BASELINE
updated: 2026-09-05
owner_role: 文档与设计治理负责人
canon_basis: "当前决策登记与责任文档"
depends_on: ["start-here.md", "governance/authoring-guide.md", "governance/decision-register.md", "governance/document-register.md"]
---

# BREACH: ECHO 文档总览

本仓库目前是可交接的游戏设计与生产基线，不是已完成或已证明好玩的游戏。基础版只做 1–4 人合作 PvE `Operation`；`Descent` 是未来扩展。玩家扮演四名正史中持续存活的壁垒外勤队员，从中央任务板进入程序生成的设施合同，在有限资源、潜行失误、设施决策、局内改装和团队重资产之间作取舍。

## 从这里开始

| 读者 | 阅读顺序 |
|---|---|
| 项目所有者 | [入门](start-here.md) → [只需所有者决定的事项](governance/project-owner-decision-queue.md) → [故事总览](gdd/story-overview.md) |
| 程序员或实现 Agent | [项目规则](../AGENTS.md) → [实施交接](production/implementation-handoff.md) → [技术栈](technical/unity-steam-and-modding-technology-stack.md) → 当前任务责任文档 → [验收矩阵](production/acceptance-matrix.md) |
| 设计、内容、美术、音频 | [愿景](gdd/game-vision-and-design-pillars.md) → [Operation](gdd/operation-game-mode.md) → [首发范围](production/release-scope.md) → 对应 GDD/内容卡 → [资产政策](production/asset-policy-and-provenance.md) |
| 测试与审查 | [决策登记](governance/decision-register.md) → [风险登记](production/risk-register.md) → [测试配置](production/initial-test-parameters.md) → [验收矩阵](production/acceptance-matrix.md) |

## 设计责任

| 问题 | 唯一责任文档 |
|---|---|
| 游戏卖点、目标体验与明确不做什么 | [产品愿景](gdd/game-vision-and-design-pillars.md) |
| 单局从任务板到撤离 | [Operation](gdd/operation-game-mode.md) |
| 新玩家首次启动、短合同与长期学习 | [新手教学](gdd/onboarding-and-learning.md) |
| 装备、输入与高级操作 | [玩家与输入](gdd/player-and-input.md) |
| 启动、Hub、任务板、房间、设置与结算页面流 | [前端与会话流](gdd/frontend-and-session-flow.md) |
| 枪械、能量/电磁武器、近战与重资产 | [战斗与武器](gdd/combat-and-arsenal.md) |
| 局内修改、效果与组合边界 | [修改与效果](gdd/field-modifications-and-effect-system.md) |
| 程序任务、空间语法与可解性 | [任务与空间](gdd/missions-and-spaces.md) |
| 敌人、难度与导演 | [遭遇与难度](gdd/encounters-and-difficulty.md) |
| 首发任务、敌人与设施模块的生产目录 | [任务目录](content/mission-catalog.md)、[敌人目录](content/enemy-catalog.md)、[设施模块](content/facility-cluster-catalog.md) |
| 资源、失败、恢复与长期经济 | [经济](gdd/economy-and-support.md)、[生存](gdd/survival-and-recovery.md)、[进度](gdd/progression-and-bastion.md) |
| 世界真实历史 | [叙事圣经](gdd/canonical-world-history-and-lore.md)、[故事总览](gdd/story-overview.md) |
| 玩家如何获得故事 | [中央故事边界](gdd/player-story-and-canonical-timeline.md)、[叙事交付](gdd/narrative-delivery.md) |
| 四名固定角色 | [角色候选](content/field-team-character-personalities.md) |
| Visual DNA、几何档位与识别规则 | [视觉方向](gdd/art-direction.md) |
| 战报与轻量本地回放 | [战报设计](gdd/debrief-and-replay.md)、[记录格式](technical/replay-recording.md) |
| 未来 Descent | [Descent](gdd/descent-future-game-mode.md) |

## 技术与生产责任

[技术栈](technical/unity-steam-and-modding-technology-stack.md)记录唯一框架组合；[架构与性能](technical/architecture-and-performance.md)记录模块边界；[AI运行架构](technical/ai-runtime.md)、[程序生成](technical/procedural-operation-generation.md)和[摄像机与动画](technical/camera-and-animation.md)拥有对应实现合同；[网络与持久化](technical/network-and-persistence.md)、[主机迁移](technical/host-migration.md)和[数据合同](technical/gameplay-data-command-and-save-contracts.md)共同定义联机真相。Mod 由[工具链](technical/modding-and-toolchain.md)、[安全与同步](technical/mod-security-and-sync.md)和[游戏内管理器](gdd/mod-manager.md)负责。Steam 是首发唯一商业、在线平台与公开 Mod 分发渠道；运行时 ID 和玩法协议仍保持平台解耦。

生产由[开发准备度矩阵](production/development-readiness-matrix.md)、[首发范围](production/release-scope.md)、[路线与验证](production/roadmap-and-validation.md)、[实施交接](production/implementation-handoff.md)、[验收矩阵](production/acceptance-matrix.md)、[风险登记](production/risk-register.md)、[资产管线](production/asset-pipeline.md)与[资产来源政策](production/asset-policy-and-provenance.md)共同约束。资产没有“免费/购买/AI”的预设比例；每项选择最低总风险且能通过统一视觉、技术、许可与修整 Gate 的来源。

## 当前成熟度

| 领域 | 已锁定 | 仍未证明或待审 |
|---|---|---|
| 产品 | Operation-only 基础版；Descent 后置；Steam-only 首发 | 核心玩法是否真的有趣、市场与留存 |
| 战斗 | 固定入场装备、有限资源、少量局内修改、团队重资产 | 枪感、数值、四人可读性 |
| 叙事 | 唯一客观历史、非递进程序合同、碎片收藏 | 四名人物最终批准、完整故事盲审 |
| 视觉 | Unity 6 + URP；“分层壁垒”；中等多边形风格化工业 | Unity同屏Style Target、Deck性能与五秒识别 |
| 网络 | Steam/SDR + FishNet + 自有权威/恢复合同；有限回溯 | 真实公网、Host Migration、Steam Deck 与性能 Spike |
| Mod | 官方与社区同包模型；Workshop；Luau Core Sandbox；禁社区 DLL | Luau/IL2CPP 绑定、安全配额、资产 Cooker 与作者 UX |
| 制作 | 里程碑、风险、验收与 Agent 技能已登记 | 团队容量、预算、排期和发行承诺 |

完整的首发责任域、唯一Owner、实现准备度和仍需证据见[开发准备度矩阵](production/development-readiness-matrix.md)。它用于判断能否开始开发，不把“文档存在”冒充“功能完成”。

## 治理与证据

[作者指南](governance/authoring-guide.md)定义权威、状态和命名；[决策登记](governance/decision-register.md)索引当前决定；[完整文档登记](governance/document-register.md)由工具自动生成。[证据登记](sources/evidence-register.md)区分用户确认、原始快照、外部资料与 Agent 推导。[源章节迁移映射](governance/source-to-document-migration-map.md)负责旧 SSOT 的覆盖追溯；聊天结论只进入责任文档、决策记录与证据登记，不保留讨论日志。

新增或改名后运行 `python tools/validate_docs.py --reindex`，再运行验证与审计。不要手写第二份完整文件清单。
