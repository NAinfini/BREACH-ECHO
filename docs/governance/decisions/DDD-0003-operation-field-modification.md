---
doc_id: DDD-0003
doc_type: decision
stage: DRAFT
updated: 2026-09-04
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["../decisions-and-questions.md"]
---

# 固定配装与局内改装

## Context / User intent

用户希望像GTFO先选两把枪和工具进入，局内不要不断选换武器；更想要下挂、稳枪、增伤等配件。

## Options considered

频繁随机武器掉落；传统Relic为主；固定loadout+少量Weapon/Tool Modules；完全无局内变化。

## Evidence / assumptions

源§5为2Weapon+2Utility+1Active，用户提及两枪一工具，槽位存在OPEN；原Operation Relic目标需重审。

## Review recommendation

DDD-0003-REC · PROPOSED · 来源：本轮讨论评审；源依据见责任文档。

入场确定武器身份，局内少量改装、优先可见tradeoff，不做彩色等级上位武器循环。具体次数归Operation模式参数，勿多处复制。

## Risks / tradeoffs

纯稳枪增伤会变成必拿数值；频繁挂点管理同样会变家务；不能因为工具数量口头例子自动删槽位。

## Decision status

DIRECTION：固定配装/配件偏好；OPEN：槽位、次数、是否首发排除Relic。

## Owner GDD links

[玩家](../../gdd/player-and-input.md)；[模式配置](../../gdd/operations.md)；[配件候选](../../content/relics-and-fusions.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## Supersedes / next gate

拟重审SRC-SSOT-2.0 §4A.15、§5、§9的Operation应用；Week8/12对照。

