---
doc_id: DECISION-PREDATOR-BREACH-MISSIONS
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["operation-vs-roguelike.md"]
---

# Predator、破障与前向重接

## 背景与用户意图

用户希望先躲和控制威胁、找到改变能力的武器/装置后反杀；破障也可找工具，但避免取枪后漫长原路返程。

## 已考虑方案

固定取钥匙回跑；纯DPS大枪解锁；可交互Threat→临时控制→前向能力取得→快速重接→反转；多解破障。

## 证据与假设

源§13.5和§15已有语法；当前只文档未有关卡。工具可耗尽却为唯一钥匙必然可能软锁。

## 决定

MISSIONREV-001 · CANON/DIRECTION · 来源：本轮用户确认；源依据见责任文档。

显式状态、可读Threat规则、真实路径转移、前向分支重接；重武器用在捷径/Optional或有慢险旁路的必经障碍。BLACKSTART只试Breach小分支，完整Predator另模板。

## 风险与取舍

加工具支路可能变跑腿；隐藏规则逼Wiki；永久不能杀若所有攻击无意义会折磨人；过多语法使单模板过载。

## 决策状态

CANON：任务池允许先困住不可常规击杀的威胁、取得改变条件的装置后反杀，以及寻找重资产破除障碍。DIRECTION：每种模板必须有清晰状态、前向重接和防软锁旁路。

## 责任设计文档

[任务语法](../../gdd/missions-and-spaces.md)；[世界互作](../../gdd/facility-systems-and-information-rules.md)；[实例](../../content/blackstart-greybox-mission.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## 替代关系与下一 Gate

不替代 no-backtracking 原则。空重武器仍须存在更慢、更危险但可行的通关路径；Predator 规则必须通过专门模板测试，不能塞进第一个灰盒冒充范围完成。
