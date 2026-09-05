---
doc_id: DDD-0006
doc_type: decision
stage: DRAFT
updated: 2026-09-04
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["../decisions-and-questions.md"]
---

# Predator、破障与前向重接

## Context / User intent

用户希望先躲和控制威胁、找到改变能力的武器/装置后反杀；破障也可找工具，但避免取枪后漫长原路返程。

## Options considered

固定取钥匙回跑；纯DPS大枪解锁；可交互Threat→临时控制→前向能力取得→快速重接→反转；多解破障。

## Evidence / assumptions

源§13.5和§15已有语法；当前只文档未有关卡。工具可耗尽却为唯一钥匙必然可能软锁。

## Review recommendation

DDD-0006-REC · PROPOSED · 来源：本轮讨论评审；源依据见责任文档。

显式状态、可读Threat规则、真实路径转移、前向分支重接；重武器用在捷径/Optional或有慢险旁路的必经障碍。BLACKSTART只试Breach小分支，完整Predator另模板。

## Risks / tradeoffs

加工具支路可能变跑腿；隐藏规则逼Wiki；永久不能杀若所有攻击无意义会折磨人；过多语法使单模板过载。

## Decision status

DIRECTION：用户玩法意图；PROPOSED：具体状态/路线。

## Owner GDD links

[任务语法](../../gdd/missions-and-spaces.md)；[世界互作](../../gdd/world-and-information.md)；[实例](../../content/blackstart.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## Supersedes / next gate

不替代源no-backtracking；Week12空重武器仍能前向通关，下一模板才测试Predator。

