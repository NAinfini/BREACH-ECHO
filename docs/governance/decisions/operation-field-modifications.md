---
doc_id: DECISION-OPERATION-FIELD-MODIFICATIONS
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["operation-vs-roguelike.md"]
---

# 固定配装与局内改装

## 背景与用户意图

用户希望像GTFO先选两把枪和工具进入，局内不要不断选换武器；更想要下挂、稳枪、增伤等配件。

## 已考虑方案

频繁随机武器掉落；传统Relic为主；固定loadout+少量Weapon/Tool Modules；完全无局内变化。

## 证据与假设

源§5为2Weapon+2Utility+1Active，用户提及两枪一工具，槽位存在OPEN；原Operation Relic目标需重审。

## 决定

FIELDMOD-001 · CANON · 来源：本轮用户确认；源依据见责任文档。

玩家以两把枪、一件工具和一个自由选择的战术模块入场。局内只获得少量、有明确挂点和取舍的武器/工具修改，不进行随机换枪或彩色等级上位武器循环。具体投放次数由 Operation 责任文档维护。

## 风险与取舍

纯稳枪增伤会变成必拿数值；频繁挂点管理同样会变家务；不能因为工具数量口头例子自动删槽位。

## 决策状态

CANON：两枪、一工具、一自由战术模块；入场装备决定身份；局内是少量修改而非换枪。Operation 不加载无限 Relic 堆叠或自动 Fusion；数值与投放频率仍为 TEST。

## 责任设计文档

[玩家](../../gdd/player-and-input.md)；[模式配置](../../gdd/operation-game-mode.md)；[配件候选](../../content/modification-catalog.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## 替代关系与下一 Gate

SUPERSEDES：SRC-SSOT-2.0 §4A.15、§5、§9 中与当前 Operation 槽位和 Relic/Fusion 冲突的解释。用同场景无改装对照验证这一层是否真的增加可复述选择。
