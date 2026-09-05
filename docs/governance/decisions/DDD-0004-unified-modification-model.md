---
doc_id: DDD-0004
doc_type: decision
stage: ARCHIVE
updated: 2026-09-05
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["../decision-register.md"]
---

# 统一修改模型而非统一玩家概念

## Context / User intent

用户提出把武器配件底层做成Relic，方便未来rework。

## Options considered

配件继承RelicBase；两套效果系统；统一ModificationDefinition/Effect，按scope和presentation区分。

## Evidence / assumptions

共同点是效果与事件，差异是目标/挂点/成本/视觉/模式；共享数据结构不能证明共享平衡。

## Review recommendation

DDD-0004-REC · PROPOSED · 来源：本轮讨论评审；源依据见责任文档。

单一ModificationDefinition含scope、mount、compatible_tags、effect_graph、权限、tradeoffs、冲突、visual、allowlist与版本；WeaponModule/ToolModule/TeamProtocol/Relic用同一schema。Operation推荐不启用自动Fusion。

## Risks / tradeoffs

自动吞实体配件伤害所有权；给所有效果同mode资格会破坏资源管理；提前冻结schema产生兼容债。

## Decision status

PROPOSED：统一模型建议；OPEN：用户对Operation融合与具体字段最终批准。

## Owner GDD links

[修改与Fusion](../../gdd/modifications-and-effects.md)；[注册与权限](../../technical/modding-and-toolchain.md)；[内容卡](../../content/modification-catalog.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## Supersedes / next gate

拟SUPERSEDES源§9.5在Operation中的自动全局应用；源自动Fusion本身保留Lab基线；Week8合同与后悔测试。



## 2026-09-05 disposition / 历史状态

本文件保留当时的选项和理由，旧OPEN不是当前未决入口。产品/装备/技术/制作问题已由DDD-0013–0018决定，人物与完整故事仍通过OWNER-01审阅；请读[当前决策登记](../decision-register.md)。不再按本文旧日期或未批准推荐直接实施。
