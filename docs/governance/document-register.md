---
doc_id: GOV-DOCUMENT-REGISTER
doc_type: governance
stage: BASELINE
updated: 2026-09-05
owner_role: BREACH ECHO documentation stewardship
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; delegated decisions DDD-0013–0018"
depends_on: ["../README.md"]
---

# 完整文档登记 / All documents

这份登记包含所有Markdown：根入口、项目skill、当前规格、创作审阅、未来设计、历史source和模板。BASELINE不是游戏实现状态。按角色先读[文档地图](../README.md)，再阅读相关职责文件。

自动登记文件数：83。新增或改名后运行`python3 tools/validate_docs.py --reindex`更新本表。

| ID / path | 用途/状态 | 文档 |
|---|---|---|
| `.agents/skills/breach-documentation/SKILL.md` | ENTRY/SKILL | [BREACH ECHO documentation skill](../../.agents/skills/breach-documentation/SKILL.md) |
| `AGENTS.md` | ENTRY/SKILL | [BREACH ECHO contributor and agent instructions](../../AGENTS.md) |
| `README.md` | ENTRY/SKILL | [BREACH: ECHO · 裂界残响](../../README.md) |
| `DOC-README` | BASELINE | [BREACH ECHO 文档地图 / Documentation map](../README.md) |
| `CONTENT-BLACKSTART` | BASELINE | [BLACKSTART：可搭建灰盒规格](../content/blackstart.md) |
| `CONTENT-CHARACTERS` | REVIEW | [壁垒外勤小队：四名固定角色 v1](../content/characters.md) |
| `CONTENT-COMBAT-BALANCE` | BASELINE | [战斗试制参数：第一版可以直接搭建的数值](../content/combat-balance.md) |
| `CONTENT-COMBAT` | BASELINE | [战斗原型卡](../content/combat-prototypes.md) |
| `CONTENT-MODIFICATIONS` | BASELINE | [Operation修改目录与Lab实验](../content/modification-catalog.md) |
| `GDD-ART` | BASELINE | [视觉方向与可识别性](../gdd/art-direction.md) |
| `GDD-AUDIO` | BASELINE | [音频、音乐、字幕与触觉](../gdd/audio-and-haptics.md) |
| `GDD-CENTRAL-STORY` | BASELINE | [玩家故事与单一世界时间线](../gdd/central-story-spine.md) |
| `GDD-COMBAT` | BASELINE | [战斗与武器家族](../gdd/combat-and-arsenal.md) |
| `GDD-COOP` | BASELINE | [合作、单人、Bots 与公共匹配](../gdd/coop-and-social.md) |
| `GDD-DEBRIEF-REPLAY` | BASELINE | [任务战报与行动回放](../gdd/debrief-and-replay.md) |
| `GDD-DESCENT` | FUTURE | [Descent：保留基线与未来候选](../gdd/descent.md) |
| `GDD-ECONOMY` | BASELINE | [资源、Support 与公共物资](../gdd/economy-and-support.md) |
| `GDD-ENCOUNTERS` | BASELINE | [敌人、遭遇与难度](../gdd/encounters-and-difficulty.md) |
| `GDD-MISSIONS` | BASELINE | [任务语法、空间生成与可解性](../gdd/missions-and-spaces.md) |
| `GDD-MOD-MANAGER` | BASELINE | [游戏内Mod Manager：页面、状态与玩家流程](../gdd/mod-manager.md) |
| `GDD-BUILD` | BASELINE | [修改、效果、数值与模式隔离](../gdd/modifications-and-effects.md) |
| `GDD-NARRATIVE` | REVIEW | [世界观与故事圣经](../gdd/narrative-bible.md) |
| `GDD-NARRATIVE-DELIVERY` | BASELINE | [叙事交付、对白与本地化](../gdd/narrative-delivery.md) |
| `GDD-OPERATIONS` | BASELINE | [Systemic Tactical Operation](../gdd/operations.md) |
| `GDD-PLAYER` | BASELINE | [玩家、配装与输入](../gdd/player-and-input.md) |
| `GDD-PROGRESSION` | BASELINE | [知识、永久进度与壁垒](../gdd/progression-and-bastion.md) |
| `GDD-STORY-OVERVIEW` | REVIEW | [完整故事总览：供所有者最终审阅](../gdd/story-overview.md) |
| `GDD-SURVIVAL` | BASELINE | [生存、倒地与失败恢复](../gdd/survival-and-recovery.md) |
| `GDD-UX` | BASELINE | [HUD、控制器、信息与可访问性](../gdd/ux-and-accessibility.md) |
| `GDD-VISION` | BASELINE | [产品体验、受众与模式选择](../gdd/vision.md) |
| `GDD-WORLD` | BASELINE | [设施、信息、Door、Cart 与 Earned Safety](../gdd/world-and-information.md) |
| `GDD-WORLD-NAMING` | BASELINE | [世界命名规范](../gdd/world-naming.md) |
| `GUIDE-GLOSSARY` | BASELINE | [术语表 / Glossary](../glossary.md) |
| `GOV-AUTHORING` | BASELINE | [文档权威、命名、决定和维护规则](authoring-guide.md) |
| `GOV-DECISIONS` | BASELINE | [当前决策登记与覆盖关系](decision-register.md) |
| `DDD-0001` | ARCHIVE | [产品分叉与首发核心](decisions/DDD-0001-operation-vs-roguelike.md) |
| `DDD-0002` | ARCHIVE | [模块化与公开API](decisions/DDD-0002-modular-product-architecture.md) |
| `DDD-0003` | ARCHIVE | [固定配装与局内改装](decisions/DDD-0003-operation-field-modification.md) |
| `DDD-0004` | ARCHIVE | [统一修改模型而非统一玩家概念](decisions/DDD-0004-unified-modification-model.md) |
| `DDD-0005` | ARCHIVE | [团队重资产](decisions/DDD-0005-team-ordnance.md) |
| `DDD-0006` | ARCHIVE | [Predator、破障与前向重接](decisions/DDD-0006-predator-and-breach-missions.md) |
| `DDD-0007` | ARCHIVE | [单一客观正史与非递进玩家故事](decisions/DDD-0007-single-canonical-story.md) |
| `DDD-0008` | BASELINE | [引擎锁定：Unity 6](decisions/DDD-0008-engine-unity6.md) |
| `DDD-0009` | BASELINE | [AI-Agent-first 工程结构与内置 Mod Runtime](decisions/DDD-0009-agent-first-modding-runtime.md) |
| `DDD-0010` | BASELINE | [Host Authority 与 Gameplay Command Replication](decisions/DDD-0010-host-authority-gameplay-commands.md) |
| `DDD-0011` | BASELINE | [Tick Architecture：固定60Hz权威模拟与多频率更新](decisions/DDD-0011-tick-architecture.md) |
| `DDD-0012` | BASELINE | [Replication Architecture：Snapshot + Delta State + Reliable Gameplay Events](decisions/DDD-0012-replication-architecture.md) |
| `DDD-0013` | BASELINE | [授权定稿与Operation唯一基础产品](decisions/DDD-0013-delegated-baseline-and-scope.md) |
| `DDD-0014` | BASELINE | [Operation装备、有限经济与修改规则](decisions/DDD-0014-operation-loadout-and-modifications.md) |
| `DDD-0015` | BASELINE | [Steam网络栈、数据格式与命中历史](decisions/DDD-0015-steam-networking-and-data-stack.md) |
| `DDD-0016` | BASELINE | [主机迁移、租约和认证恢复点](decisions/DDD-0016-host-migration-and-recovery-certificates.md) |
| `DDD-0017` | BASELINE | [安全模组首版、精确包锁与原生管理器](decisions/DDD-0017-safe-mods-and-native-manager.md) |
| `DDD-0018` | BASELINE | [制作顺序、资产管线和完整交接](decisions/DDD-0018-production-assets-and-handoff.md) |
| `GOV-DISCUSSION-20260904` | ARCHIVE | [2026-09-04 讨论记录](discussion-log-2026-09-04.md) |
| `GOV-DOCUMENT-REGISTER` | BASELINE | [完整文档登记 / All documents](document-register.md) |
| `GOV-FINALIZATION-REVIEW` | BASELINE | [定稿审阅、覆盖范围与未完成边界](finalization-review.md) |
| `GOV-DECISIONS-HISTORY-20260905` | ARCHIVE | [定稿前决策与未决问题（历史，2026-09-05）](history/decision-register-before-finalization-2026-09-05.md) |
| `GOV-OWNER` | BASELINE | [Only the decisions that need you / 仅需所有者裁决](owner-decisions.md) |
| `GOV-SOURCE-MAP` | ARCHIVE | [源章节与规则迁移索引](source-map.md) |
| `PROD-ACCEPTANCE` | BASELINE | [验收矩阵与证据要求](../production/acceptance-matrix.md) |
| `PROD-ASSETS` | BASELINE | [资产来源、图像到可动模型、许可与导入管线](../production/asset-pipeline.md) |
| `PROD-HANDOFF` | BASELINE | [Implementation handoff / 从文档开始制作](../production/implementation-handoff.md) |
| `PROD-PLATFORM` | BASELINE | [平台、商业、Demo 与发行关卡](../production/platform-and-release.md) |
| `PROD-SCOPE` | BASELINE | [产品范围、首发合同与明确不做的事](../production/release-scope.md) |
| `PROD-RISKS` | BASELINE | [风险登记与否决条件](../production/risk-register.md) |
| `PROD-ROADMAP` | BASELINE | [制作路线与验证关卡](../production/roadmap-and-validation.md) |
| `PROD-TEST-PROFILE` | BASELINE | [初始测试参数：可执行起点，不是假平衡定稿](../production/test-profile.md) |
| `RESEARCH-METHODS` | BASELINE | [研究资料、技能与文档格式](../research/references-and-methods.md) |
| `RESEARCH-TECH-20260905` | BASELINE | [技术选择证据与核验限制 · 2026-09-05](../research/technical-evidence-2026-09-05.md) |
| `docs/sources/chatgpt-brutal-review-v1.0.md` | ARCHIVE | [GAME PROJECT — 残酷外部审查 v1.0](../sources/chatgpt-brutal-review-v1.0.md) |
| `SRC-REGISTER` | BASELINE | [证据登记与覆盖限制](../sources/evidence-register.md) |
| `docs/sources/ssot-v2.0-original.md` | ARCHIVE | [GAME PROJECT — 全项目统计与唯一真相 SSOT v2.0](../sources/ssot-v2.0-original.md) |
| `GUIDE-START` | BASELINE | [Start here: how we will turn this into a game](../start-here.md) |
| `TECH-ARCH` | BASELINE | [模拟架构与性能合同](../technical/architecture-and-performance.md) |
| `TECH-DATA` | BASELINE | [数据、命令、事务和存档合同](../technical/data-contracts.md) |
| `TECH-MIGRATION` | BASELINE | [主机迁移：快照、选主、租约与恢复协议](../technical/host-migration.md) |
| `TECH-MOD-SECURITY` | BASELINE | [Mod信任边界、包固定与自动同步](../technical/mod-security-and-sync.md) |
| `TECH-MODDING` | BASELINE | [模块化产品、公开能力与工具链](../technical/modding-and-toolchain.md) |
| `TECH-NETWORK` | BASELINE | [网络权威、存档与版本固定](../technical/network-and-persistence.md) |
| `TECH-REPLAY` | BASELINE | [行动回放记录、存储与播放](../technical/replay-recording.md) |
| `TECH-STACK` | BASELINE | [选定技术栈与安装验收](../technical/technology-stack.md) |
| `TPL-CONTENT` | TEMPLATE | [内容卡模板](../templates/content-spec.md) |
| `TPL-SYSTEM` | TEMPLATE | [系统规格模板](../templates/system-spec.md) |
