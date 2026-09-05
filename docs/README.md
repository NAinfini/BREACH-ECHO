---
doc_id: DOC-README
doc_type: guide
stage: BASELINE
updated: 2026-09-05
owner_role: 文档维护负责人
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; DDD-0013"
depends_on: ["governance/authoring-guide.md", "governance/document-register.md"]
---

# BREACH ECHO 文档地图 / Documentation map

这是当前设计基线入口，不是游戏已完成的声明。首次参与请先看 [Start here](start-here.md)。所有文件、状态、职责及入口由[完整文档登记](governance/document-register.md)列出；这里不手写容易过期的文件总数。

## 四条阅读路径

| 读者 | 建议顺序 |
|---|---|
| 项目所有者 / 新手 | [入门](start-here.md) → [首发范围](production/release-scope.md) → [仅需所有者裁决的事项](governance/owner-decisions.md) → [故事总览](gdd/story-overview.md) |
| 程序员 / AI agent | [AGENTS](../AGENTS.md) → [实施交接](production/implementation-handoff.md) → [技术栈](technical/technology-stack.md) → [架构](technical/architecture-and-performance.md) → 当前任务的规则责任文档 → [验收矩阵](production/acceptance-matrix.md) |
| 设计 / 内容 / 美术 / 音频 | [愿景](gdd/vision.md) → [Operation](gdd/operations.md) → [范围](production/release-scope.md) → 对应GDD和内容卡 → [资产管线](production/asset-pipeline.md) |
| 测试 / 接手维护 | [决策登记](governance/decision-register.md) → [风险登记](production/risk-register.md) → [验收矩阵](production/acceptance-matrix.md) → [实施交接](production/implementation-handoff.md) → [完整登记](governance/document-register.md) |

## 体验与系统责任

| 问题 | 唯一责任文档 |
|---|---|
| 为什么玩、做什么产品 | [愿景](gdd/vision.md)、[首发范围](production/release-scope.md) |
| 一局怎么开始和结束 | [Operation](gdd/operations.md)、[合作与社交](gdd/coop-and-social.md) |
| 操作、枪械、近战、部位、重资产 | [玩家与输入](gdd/player-and-input.md)、[战斗与军械](gdd/combat-and-arsenal.md)、[战斗原型](content/combat-prototypes.md) |
| 配件与效果的统一规则 | [修改与效果](gdd/modifications-and-effects.md)、[修改目录](content/modification-catalog.md) |
| 弹药、支援、物资与成长 | [经济与支援](gdd/economy-and-support.md)、[进度与壁垒](gdd/progression-and-bastion.md) |
| 倒地、救人、Wipe | [生存与恢复](gdd/survival-and-recovery.md) |
| 任务、程序关卡、AI与难度 | [任务与空间](gdd/missions-and-spaces.md)、[遭遇](gdd/encounters-and-difficulty.md)、[BLACKSTART](content/blackstart.md) |
| 终端、门、电力、Cart与情报 | [世界与信息](gdd/world-and-information.md) |
| 菜单、可访问性、反馈 | [UX](gdd/ux-and-accessibility.md)、[音频](gdd/audio-and-haptics.md)、[美术](gdd/art-direction.md)、[Mod Manager](gdd/mod-manager.md) |
| 结算、统计与临时回放 | [战报](gdd/debrief-and-replay.md)、[记录技术](technical/replay-recording.md) |
| 世界、名字、人物、交付 | [世界圣经](gdd/narrative-bible.md)、[命名](gdd/world-naming.md)、[角色](content/characters.md)、[玩家时代](gdd/central-story-spine.md)、[叙事交付](gdd/narrative-delivery.md) |
| 后续模式 | [Descent](gdd/descent.md)，FUTURE，不能进入首发关键路径 |

## 技术与制作责任

[架构与性能](technical/architecture-and-performance.md)负责模块和性能纪律；[技术栈](technical/technology-stack.md)负责具体依赖；[网络与持久化](technical/network-and-persistence.md)负责整体会话语义；[主机迁移](technical/host-migration.md)负责选主、恢复和失败边界；[数据合同](technical/data-contracts.md)负责标识、事务和持久化；[模组与工具链](technical/modding-and-toolchain.md)和[模组安全](technical/mod-security-and-sync.md)负责公开能力和同步。

[发行](production/platform-and-release.md)、[阶段路线](production/roadmap-and-validation.md)、[交接](production/implementation-handoff.md)、[验收](production/acceptance-matrix.md)、[风险](production/risk-register.md)、[资产管线](production/asset-pipeline.md)和[初始测试参数](production/test-profile.md)共同组成执行计划。测试参数不是平衡定稿；没有任何设备、玩家或游戏代码验证被本次文字工作替代。

## 决策、证据与历史

[权威规则](governance/authoring-guide.md)解释CANON、DECIDED、TEST与文档成熟度；[决策登记](governance/decision-register.md)索引全部DDD；[所有者队列](governance/owner-decisions.md)只保留真正需要本人决定的内容。

[原证据登记](sources/evidence-register.md)、[新增技术证据](research/technical-evidence-2026-09-05.md)、[方法与参考](research/references-and-methods.md)分别说明历史来源、新核验事实和研究方法。[原文映射](governance/source-map.md)及[旧讨论](governance/discussion-log-2026-09-04.md)是历史迁移记录，不是另一套现行规则。两份原始快照保持不变。

新增文档时使用[系统模板](templates/system-spec.md)或[内容模板](templates/content-spec.md)，更新完整登记并运行文档检查。不要新增`final-v2`、`最终版-新`、平行SSOT或只有聊天知道的决策。
