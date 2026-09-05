---
doc_id: GOV-DECISIONS
doc_type: governance
stage: BASELINE
updated: 2026-09-05
owner_role: BREACH ECHO documentation stewardship
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; delegated decisions DDD-0013–0018"
depends_on: ["owner-decisions.md", "authoring-guide.md"]
---

# 当前决策登记与覆盖关系

这是一份当前索引，不是另一个复制GDD。每条决定的理由、替代方案、边界、影响、重审条件和测试在DDD中。历史DEC-001…问题账完整保存在[定稿前历史](history/decision-register-before-finalization-2026-09-05.md)，不要把其中旧OPEN当现行要求。

| 决定 | 当前状态 | 责任记录 |
|---|---|---|
| DDD-0013 | DECIDED / delegated | [授权定稿与Operation唯一基础产品](decisions/DDD-0013-delegated-baseline-and-scope.md) |
| DDD-0014 | DECIDED / delegated | [Operation装备、有限经济与修改规则](decisions/DDD-0014-operation-loadout-and-modifications.md) |
| DDD-0015 | DECIDED / delegated | [Steam网络栈、数据格式与命中历史](decisions/DDD-0015-steam-networking-and-data-stack.md) |
| DDD-0016 | DECIDED / delegated | [主机迁移、租约和认证恢复点](decisions/DDD-0016-host-migration-and-recovery-certificates.md) |
| DDD-0017 | DECIDED / delegated | [安全模组首版、精确包锁与原生管理器](decisions/DDD-0017-safe-mods-and-native-manager.md) |
| DDD-0018 | DECIDED / delegated | [制作顺序、资产管线和完整交接](decisions/DDD-0018-production-assets-and-handoff.md) |
| DDD-0001 | ARCHIVE：被后续决定承接 | [DDD-0001-operation-vs-roguelike](decisions/DDD-0001-operation-vs-roguelike.md) |
| DDD-0002 | ARCHIVE：被后续决定承接 | [DDD-0002-modular-product-architecture](decisions/DDD-0002-modular-product-architecture.md) |
| DDD-0003 | ARCHIVE：被后续决定承接 | [DDD-0003-operation-field-modification](decisions/DDD-0003-operation-field-modification.md) |
| DDD-0004 | ARCHIVE：被后续决定承接 | [DDD-0004-unified-modification-model](decisions/DDD-0004-unified-modification-model.md) |
| DDD-0005 | ARCHIVE：被后续决定承接 | [DDD-0005-team-ordnance](decisions/DDD-0005-team-ordnance.md) |
| DDD-0006 | ARCHIVE：被后续决定承接 | [DDD-0006-predator-and-breach-missions](decisions/DDD-0006-predator-and-breach-missions.md) |
| DDD-0007 | ARCHIVE：被后续决定承接 | [DDD-0007-single-canonical-story](decisions/DDD-0007-single-canonical-story.md) |
| DDD-0008 | 保留CANON，具体未决实现见DDD-0015–0017 | [DDD-0008-engine-unity6](decisions/DDD-0008-engine-unity6.md) |
| DDD-0009 | 保留CANON，具体未决实现见DDD-0015–0017 | [DDD-0009-agent-first-modding-runtime](decisions/DDD-0009-agent-first-modding-runtime.md) |
| DDD-0010 | 保留CANON，具体未决实现见DDD-0015–0017 | [DDD-0010-host-authority-gameplay-commands](decisions/DDD-0010-host-authority-gameplay-commands.md) |
| DDD-0011 | 保留CANON，具体未决实现见DDD-0015–0017 | [DDD-0011-tick-architecture](decisions/DDD-0011-tick-architecture.md) |
| DDD-0012 | 保留CANON，具体未决实现见DDD-0015–0017 | [DDD-0012-replication-architecture](decisions/DDD-0012-replication-architecture.md) |

## 旧问题如何关闭

产品单/双模式、固定配装/槽位、角色Active绑定、枪械/Staff、有限Energy、改装与Fusion：DDD-0013/0014。网络Provider、回溯算法、选主/快照、存档格式：DDD-0015/0016。脚本语言、Native政策、完整Mod Manager、Workshop旧hash、公开TC时间：DDD-0017。Demo、阶段范围、资产生产、语言、交接、排期：DDD-0018。数值采用测试参数和内容试制卡，不以“未实测”要求新手用户选。

## 仍需所有者的决定

仅[OWNER-01–04](owner-decisions.md)：故事/人物、钱与账户/商业承诺、最终视听身份、明确需求缩减。创作REVIEW没有被本次技术授权偷换成CANON。未来Descent/未发布脚本等FUTURE条目只在实际启动该范围时重开，不阻塞基础游戏。

## 改变决定

新信息使决定失效时增加新的DDD并在责任文档同步修改；记录被否决方案和证据，不删除坏消息，不把聊天当唯一记录。普通架构可重构，未发布旧运行时可移除；已发布用户进度需明确迁移。
