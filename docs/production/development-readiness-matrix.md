---
doc_id: PROD-DEVELOPMENT-READINESS
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: 制作与文档治理负责人
canon_basis: "当前文档全集与本轮游戏开发完整性审计"
depends_on: ["release-scope.md", "implementation-handoff.md", "acceptance-matrix.md", "../governance/authoring-guide.md"]
---

# 游戏开发准备度与责任覆盖矩阵

## 如何解释“文档齐全”

READY-001 · DECIDED。

本矩阵证明每个首发责任域都有唯一入口、可执行合同或明确Gate；它不证明游戏已经实现、好玩、性能合格、资产合法或能卖。`已规格化`表示可以拆实施任务，`需原型`表示规则与起始参数齐全但必须用构建验证，`需审阅`表示涉及创作/品牌的所有者裁决，`未来`不进入基础版，`缺实现`表示文档存在但仓库没有对应游戏代码或制品。

## 产品、玩法与内容覆盖

| 责任域 | 唯一入口 | 当前准备度 | 进入制作前/中的必要证据 |
|---|---|---|---|
| 产品承诺、受众、支柱 | [愿景](../gdd/game-vision-and-design-pillars.md) | 已规格化；需市场/玩法验证 | 裸战斗与任务价值对照 |
| 单局循环与模式 | [Operation](../gdd/operation-game-mode.md) | 已规格化；需原型 | BLACKSTART端到端构建 |
| 新手、首局、长期学习 | [新手教学](../gdd/onboarding-and-learning.md) | 已规格化；需玩家测试 | 8名新手无口头指导 |
| 玩家动作、输入、配装 | [玩家与输入](../gdd/player-and-input.md) | 已规格化；需手感测试 | 键鼠/控制器/FPS差异 |
| 前端、房间、设置、结算流 | [前端会话流](../gdd/frontend-and-session-flow.md) | 已规格化；缺UI实现 | 全流程状态与错误测试 |
| 战斗、武器、重资产 | [战斗](../gdd/combat-and-arsenal.md)、[数值](../content/combat-balance.md) | 可搭灰盒；需原型 | A-COMBAT与资源守恒 |
| 修改与效果 | [修改系统](../gdd/field-modifications-and-effect-system.md)、[目录](../content/modification-catalog.md) | 可搭灰盒；需组合测试 | 非法环、可读性、资源压力 |
| 敌人、难度、遭遇 | [遭遇](../gdd/encounters-and-difficulty.md)、[敌人目录](../content/enemy-catalog.md) | 首发最低目录已定义；需AI/美术 | 前兆识别、Source与角色差异 |
| 任务与程序生成 | [任务规则](../gdd/missions-and-spaces.md)、[任务目录](../content/mission-catalog.md) | 十二主变体/六支线已规划；需先做三原型 | A-PCG与人工多样性 |
| 空间模块与关卡指标 | [设施模块目录](../content/facility-cluster-catalog.md) | 灰盒套件已定义；需实际指标 | 两区域套件、导航/相机验证 |
| 世界设施与信息 | [世界交互](../gdd/facility-systems-and-information-rules.md) | 已规格化；需原型 | Terminal、Door、Power、权限事务 |
| 资源、支援与经济 | [经济](../gdd/economy-and-support.md) | 已规格化；需平衡 | 公共资源争议与零复制 |
| 生存、倒地、失败 | [生存](../gdd/survival-and-recovery.md) | 已规格化；需压力测试 | 单人/多人恢复和Wipe |
| 长期进度、奖励、Hub | [进度](../gdd/progression-and-bastion.md) | 已规格化；需留存测试 | 横向解锁、收藏、无战力门锁 |
| 合作、匹配、Bots | [合作](../gdd/coop-and-social.md) | 联机规则已规格化；Bot需后期原型 | 陌生人/无语音/Bot资源行为 |
| 战报与临时回放 | [战报](../gdd/debrief-and-replay.md)、[回放技术](../technical/replay-recording.md) | 已规格化；缺实现 | 统计对账、体积和删除生命周期 |
| 角色 | [四名角色候选](../content/field-team-character-personalities.md) | 需所有者审阅 | 代号、人格与关系最终批准 |
| 客观历史与玩家叙事 | [故事总览](../gdd/story-overview.md)、[叙事圣经](../gdd/canonical-world-history-and-lore.md) | 连接因果需所有者确认/盲审 | OWNER-01后独立挑错 |
| 叙事交付与本地化 | [叙事交付](../gdd/narrative-delivery.md) | 已规格化；需内容样本 | 收藏、字幕、可信度与随机放置 |
| 视觉 | [视觉方向](../gdd/art-direction.md) | 三候选；需最终Visual DNA | 灰盒上真实样张与OWNER-03 |
| 音频、音乐、触觉 | [音频](../gdd/audio-and-haptics.md) | 系统合同已定义；缺资产与混音 | 战斗可读性、字幕与声部预算 |
| UX与可访问性 | [UX](../gdd/ux-and-accessibility.md) | 已规格化；需设备/玩家测试 | A-ACCESS、Deck、超宽屏、200%文字 |

## 技术覆盖

| 责任域 | 唯一入口 | 当前准备度 | 必要证据 |
|---|---|---|---|
| 引擎、包与平台栈 | [技术栈](../technical/unity-steam-and-modding-technology-stack.md) | 选择已锁；版本未实构建 | M0版本/许可/Windows Build |
| 模拟、事务、性能 | [架构](../technical/architecture-and-performance.md)、[数据合同](../technical/gameplay-data-command-and-save-contracts.md) | 合同已定义；缺代码/Benchmark | 60Hz、稳定提交、压力Profile |
| AI与导航 | [AI运行架构](../technical/ai-runtime.md) | 实现合同已定义；缺代码 | 感知合法性、路径与分频负载 |
| 程序生成 | [PCG架构](../technical/procedural-operation-generation.md) | 实现合同已定义；缺代码 | Seed确定性、1000 Seed扫描 |
| 摄像机与动画 | [摄像机与动画](../technical/camera-and-animation.md) | 实现合同已定义；缺资产/代码 | FPS/TPS公平、IK与取消矩阵 |
| 网络、复制、回溯 | [网络](../technical/network-and-persistence.md)及相关决策 | 合同已定义；真实公网未测 | 4人ping/loss、命中与带宽 |
| 主机迁移与恢复 | [主机迁移](../technical/host-migration.md) | 具体协议已定义；未实现 | 故障矩阵和恢复证书 |
| 存档、Schema、迁移 | [数据合同](../technical/gameplay-data-command-and-save-contracts.md) | 格式原则已定义；DTO未实现 | 原子写、损坏、版本迁移 |
| Mod、Workshop、安全 | [工具链](../technical/modding-and-toolchain.md)、[安全同步](../technical/mod-security-and-sync.md)、[管理器](../gdd/mod-manager.md) | 体系已锁；Luau/IL2CPP未Spike | 精确hash、拒DLL、Sandbox配额 |
| 资产生产与来源 | [资产管线](asset-pipeline.md)、[资产政策](asset-policy-and-provenance.md) | Gate已定义；无正式资产清单 | Provenance、绑定、URP与性能 |
| 构建、测试、发行 | [实施交接](implementation-handoff.md)、[验收矩阵](acceptance-matrix.md)、[平台发行](platform-and-release.md) | 流程已定义；全部NOT RUN | M0–M6实际制品与Steam检查 |

## 当前真实阻碍与非阻碍

READY-002 · DECIDED。

可以立即开始M0/M1的设计输入已经足够：引擎、目录结构、输入、两把首枪、两类首敌、命令/伤害边界和验收都存在。没有最终角色代号、正式模型、配音、价格或Descent设计，不阻碍原创灰盒Combat Sandbox。

不能声称“完整游戏可直接量产”的原因是：仓库仍无Unity工程与可玩构建；玩法、网络、Steam Deck、Luau、安全、PCG、AI、摄像机和资产均未实测；最终历史、角色和Visual DNA仍需审阅；团队人数、预算、开发速率、价格与发布日期未知。解决这些问题需要原型和证据，不是再写更多预测性文档。

## 文档完成门

READY-003 · DECIDED。

一个首发系统只有在以下信息由唯一文档拥有时才算文档可实施：玩家目的；输入/输出；状态与数据所有权；正常/失败/取消/并发/断线；内容字段；首个可搭实例；数值状态与唯一Owner；日志；测试条件与否决门；与范围和依赖的链接。本轮矩阵中的首发责任域都已有该入口。后续发现缺口应修改责任文档，不创建平行“完整版GDD”。

## 下一批执行顺序

READY-004 · DECIDED。

下一批不再继续横向补文档，而是进入`M0：Unity项目骨架与Combat Sandbox`：建立可重复Unity 6 URP工程、锁准确包版本、实现本地权威命令到伤害的最小链、输入/相机/调试HUD和独立Windows构建。完成M0后按M1先做AR、Shotgun、逐能体、压射体与动作阶段，再决定哪些设计参数需要改写。

