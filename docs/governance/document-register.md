---
doc_id: GOV-DOCUMENT-REGISTER
doc_type: governance
stage: BASELINE
updated: 2026-09-05
owner_role: 文档治理负责人
canon_basis: "当前文档治理基线"
depends_on: ["authoring-guide.md"]
---

# 完整文档登记

这份登记包含全部 Markdown：根入口、项目技能、现行规格、创作审阅、未来设计、历史来源和模板。`BASELINE` 表示文档权威，不代表游戏已经实现。按角色先读[文档总览](../README.md)，再阅读相关责任文件。两份受保护的原始来源快照保持原文，只用于证据追溯，不是现行设计。

自动登记文件数：88。新增或改名后运行 `python3 tools/validate_docs.py --reindex` 更新本表。

| ID / 路径 | 用途 / 状态 | 文档 |
|---|---|---|
| `AGENTS.md` | ENTRY/SKILL | [BREACH ECHO 贡献者与智能体工作准则](../../AGENTS.md) |
| `CONTENT-BLACKSTART` | BASELINE | [BLACKSTART：可搭建灰盒规格](../content/blackstart-greybox-mission.md) |
| `CONTENT-COMBAT-BALANCE` | BASELINE | [战斗试制参数：第一版可以直接搭建的数值](../content/combat-balance.md) |
| `CONTENT-COMBAT` | BASELINE | [战斗原型卡](../content/combat-prototypes.md) |
| `CONTENT-ENEMIES` | BASELINE | [首发敌人目录与行为卡](../content/enemy-catalog.md) |
| `CONTENT-FACILITY-CLUSTERS` | BASELINE | [设施模块、空间指标与首发套件](../content/facility-cluster-catalog.md) |
| `CONTENT-CHARACTERS` | REVIEW | [壁垒外勤小队：四名固定角色 v1](../content/field-team-character-personalities.md) |
| `CONTENT-MISSIONS` | BASELINE | [首发任务目录与兼容矩阵](../content/mission-catalog.md) |
| `CONTENT-MODIFICATIONS` | BASELINE | [Operation 改装目录与实验室实验](../content/modification-catalog.md) |
| `GDD-ART` | BASELINE | [视觉方向与可识别性](../gdd/art-direction.md) |
| `GDD-AUDIO` | BASELINE | [音频、音乐、字幕与触觉](../gdd/audio-and-haptics.md) |
| `GDD-NARRATIVE` | REVIEW | [世界观与故事圣经](../gdd/canonical-world-history-and-lore.md) |
| `GDD-COMBAT` | BASELINE | [战斗与武器家族](../gdd/combat-and-arsenal.md) |
| `GDD-COOP` | BASELINE | [合作、单人、Bots 与公共匹配](../gdd/coop-and-social.md) |
| `GDD-DEBRIEF-REPLAY` | BASELINE | [任务战报与行动回放](../gdd/debrief-and-replay.md) |
| `GDD-DESCENT` | FUTURE | [Descent：保留基线与未来候选](../gdd/descent-future-game-mode.md) |
| `GDD-ECONOMY` | BASELINE | [资源、Support 与公共物资](../gdd/economy-and-support.md) |
| `GDD-ENCOUNTERS` | BASELINE | [敌人、遭遇与难度](../gdd/encounters-and-difficulty.md) |
| `GDD-WORLD` | BASELINE | [设施、信息、Door、Cart 与 Earned Safety](../gdd/facility-systems-and-information-rules.md) |
| `GDD-BUILD` | BASELINE | [统一修改与效果系统](../gdd/field-modifications-and-effect-system.md) |
| `GDD-FRONTEND-FLOW` | BASELINE | [前端、房间与会话状态流](../gdd/frontend-and-session-flow.md) |
| `GDD-VISION` | BASELINE | [产品体验、受众与模式选择](../gdd/game-vision-and-design-pillars.md) |
| `GDD-MISSIONS` | BASELINE | [任务语法、空间生成与可解性](../gdd/missions-and-spaces.md) |
| `GDD-MOD-MANAGER` | BASELINE | [游戏内Mod Manager：页面、状态与玩家流程](../gdd/mod-manager.md) |
| `GDD-NARRATIVE-DELIVERY` | BASELINE | [叙事交付、对白与本地化](../gdd/narrative-delivery.md) |
| `GDD-ONBOARDING` | BASELINE | [新手教学、首局与长期学习](../gdd/onboarding-and-learning.md) |
| `GDD-OPERATIONS` | BASELINE | [系统化战术行动（Operation）](../gdd/operation-game-mode.md) |
| `GDD-PLAYER` | BASELINE | [玩家、配装与输入](../gdd/player-and-input.md) |
| `GDD-CENTRAL-STORY` | BASELINE | [玩家故事与单一世界时间线](../gdd/player-story-and-canonical-timeline.md) |
| `GDD-PROGRESSION` | BASELINE | [知识、永久进度与壁垒](../gdd/progression-and-bastion.md) |
| `GDD-STORY-OVERVIEW` | REVIEW | [完整故事总览：供所有者最终审阅](../gdd/story-overview.md) |
| `GDD-SURVIVAL` | BASELINE | [生存、倒地与失败恢复](../gdd/survival-and-recovery.md) |
| `GDD-UX` | BASELINE | [HUD、控制器、信息与可访问性](../gdd/ux-and-accessibility.md) |
| `GDD-WORLD-NAMING` | REVIEW | [世界命名规范](../gdd/world-naming.md) |
| `GUIDE-GLOSSARY` | BASELINE | [术语表 / Glossary](../glossary.md) |
| `GOV-AUTHORING` | BASELINE | [文档权威、命名与维护规则](authoring-guide.md) |
| `GOV-DECISIONS` | BASELINE | [当前决策登记](decision-register.md) |
| `DECISION-AGENT-FIRST-MOD-RUNTIME` | BASELINE | [智能体优先工程结构与内置模组运行时](decisions/agent-first-modding-runtime.md) |
| `DECISION-FIXED-TICK-MULTIRATE` | BASELINE | [Tick 架构：固定 60 Hz 权威模拟与多频率更新](decisions/fixed-tick-and-multirate-simulation.md) |
| `DECISION-HOST-AUTHORITY-COMMANDS` | BASELINE | [主机权威与玩法命令复制](decisions/host-authority-and-gameplay-commands.md) |
| `DECISION-LAG-COMPENSATION` | BASELINE | [延迟补偿与服务器历史判定](decisions/lag-compensation-and-server-rewind.md) |
| `DECISION-MODULAR-PRODUCT-ARCHITECTURE` | BASELINE | [模块化与公开API](decisions/modular-product-architecture.md) |
| `DECISION-NETWORK-RUNTIME-RECOVERY` | BASELINE | [网络运行与恢复：Steam + FishNet + 小型协调器](decisions/network-runtime-and-recovery.md) |
| `DECISION-OPERATION-FIELD-MODIFICATIONS` | BASELINE | [固定配装与局内改装](decisions/operation-field-modifications.md) |
| `DECISION-BASE-GAME-MODE` | BASELINE | [产品分叉与首发核心](decisions/operation-vs-roguelike.md) |
| `DECISION-PREDATOR-BREACH-MISSIONS` | BASELINE | [Predator、破障与前向重接](decisions/predator-and-breach-missions.md) |
| `DECISION-SINGLE-CANONICAL-STORY` | BASELINE | [单一客观正史与非递进玩家故事](decisions/single-canonical-story.md) |
| `DECISION-STATE-REPLICATION` | BASELINE | [复制架构：快照 + 增量状态 + 可靠玩法事件](decisions/state-replication.md) |
| `DECISION-STEAM-WORKSHOP-MOD-RUNTIME` | BASELINE | [Steam Workshop 模组运行时、管理器与安全边界](decisions/steam-workshop-mod-runtime.md) |
| `DECISION-TEAM-ORDNANCE` | BASELINE | [团队重资产](decisions/team-ordnance.md) |
| `DECISION-UNIFIED-MODIFICATION-MODEL` | BASELINE | [统一修改模型而非统一玩家概念](decisions/unified-modification-model.md) |
| `DECISION-UNITY-ENGINE-RENDERING` | BASELINE | [引擎锁定：Unity 6](decisions/unity-engine-and-rendering.md) |
| `DECISION-VISUAL-DNA-ART-DIRECTION` | BASELINE | [Visual DNA：分层壁垒](decisions/visual-dna-and-art-direction.md) |
| `GOV-DOCUMENT-REGISTER` | BASELINE | [完整文档登记](document-register.md) |
| `GOV-OWNER` | BASELINE | [仅需项目所有者裁决的事项](project-owner-decision-queue.md) |
| `GOV-SOURCE-MAP` | ARCHIVE | [源章节与规则迁移索引](source-to-document-migration-map.md) |
| `PROD-ACCEPTANCE` | BASELINE | [验收矩阵与证据要求](../production/acceptance-matrix.md) |
| `PROD-ASSETS` | BASELINE | [资产制作、绑定与 Unity 导入管线](../production/asset-pipeline.md) |
| `PROD-ASSET-POLICY` | BASELINE | [资产采购、来源与许可政策](../production/asset-policy-and-provenance.md) |
| `PROD-DEVELOPMENT-READINESS` | BASELINE | [游戏开发准备度与责任覆盖矩阵](../production/development-readiness-matrix.md) |
| `PROD-AGENT-SKILLS` | BASELINE | [游戏制作 Agent Skills 能力地图](../production/game-production-agent-skills.md) |
| `PROD-HANDOFF` | BASELINE | [实施交接：从文档开始制作](../production/implementation-handoff.md) |
| `PROD-TEST-PROFILE` | BASELINE | [初始测试参数：可执行起点，不是假平衡定稿](../production/initial-test-parameters.md) |
| `PROD-PLATFORM` | BASELINE | [平台、商业、Demo 与发行关卡](../production/platform-and-release.md) |
| `PROD-SCOPE` | BASELINE | [产品范围、首发合同与明确不做的事](../production/release-scope.md) |
| `PROD-RISKS` | BASELINE | [风险登记与否决条件](../production/risk-register.md) |
| `PROD-ROADMAP` | BASELINE | [制作路线、范围与验证](../production/roadmap-and-validation.md) |
| `DOC-README` | BASELINE | [BREACH: ECHO 文档总览](../README.md) |
| `RESEARCH-METHODS` | BASELINE | [研究资料、技能与文档格式](../research/references-and-methods.md) |
| `RESEARCH-TECH-20260905` | BASELINE | [技术选择证据与核验限制 · 2026-09-05](../research/technical-evidence-2026-09-05.md) |
| `docs/sources/chatgpt-brutal-review-v1.0.md` | ARCHIVE | [GAME PROJECT — 残酷外部审查 v1.0](../sources/chatgpt-brutal-review-v1.0.md) |
| `SRC-REGISTER` | BASELINE | [证据登记与覆盖限制](../sources/evidence-register.md) |
| `docs/sources/ssot-v2.0-original.md` | ARCHIVE | [GAME PROJECT — 全项目统计与唯一真相 SSOT v2.0](../sources/ssot-v2.0-original.md) |
| `GUIDE-START` | BASELINE | [入门：如何把文档做成游戏](../start-here.md) |
| `TECH-AI` | BASELINE | [AI决策、感知、群组与导航架构](../technical/ai-runtime.md) |
| `TECH-ARCH` | BASELINE | [模拟架构与性能合同](../technical/architecture-and-performance.md) |
| `TECH-CAMERA-ANIMATION` | BASELINE | [FPS/TPS摄像机、动画与玩法时序合同](../technical/camera-and-animation.md) |
| `TECH-DATA` | BASELINE | [数据、命令、事务和存档合同](../technical/gameplay-data-command-and-save-contracts.md) |
| `TECH-MIGRATION` | BASELINE | [主机迁移：快照、选主、租约与恢复协议](../technical/host-migration.md) |
| `TECH-MOD-SECURITY` | BASELINE | [模组信任边界、包固定与自动同步](../technical/mod-security-and-sync.md) |
| `TECH-MODDING` | BASELINE | [模块化产品、公开能力与工具链](../technical/modding-and-toolchain.md) |
| `TECH-NETWORK` | BASELINE | [网络权威、存档与版本固定](../technical/network-and-persistence.md) |
| `TECH-PROCEDURAL-OPERATIONS` | BASELINE | [程序Operation生成、种子与验证架构](../technical/procedural-operation-generation.md) |
| `TECH-REPLAY` | BASELINE | [行动回放记录、存储与播放](../technical/replay-recording.md) |
| `TECH-STACK` | BASELINE | [选定技术栈与安装验收](../technical/unity-steam-and-modding-technology-stack.md) |
| `TPL-CONTENT` | TEMPLATE | [内容卡模板](../templates/content-spec.md) |
| `TPL-SYSTEM` | TEMPLATE | [系统规格模板](../templates/system-spec.md) |
| `README.md` | ENTRY/SKILL | [BREACH: ECHO · 裂界残响](../../README.md) |
