---
doc_id: DECISION-TEAM-ORDNANCE
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["operation-vs-roguelike.md"]
---

# 团队重资产

## 背景与用户意图

用户提出手持、切枪放下、不占常规loadout、固定弹药且普通补给不能补、用完作废的超强团队重武器，希望代价来自搬运/双手/掩护。

## 已考虑方案

作为第三武器槽；普通Heavy进入背包；持久世界资产；一次性任务钥匙。

## 证据与假设

用户意图明确；源§6.6已有Heavy problem-solving方向，未完整定义新世界资产。强火力是否有趣与恶意耗弹尚无测试。

## 决定

ORDNANCE-001 · CANON/DIRECTION · 来源：本轮用户确认；源依据见责任文档。

持久Team Ordnance，权威唯一Instance、弹量守恒、倒地/离线放下、合法越界回收。用途是强/快/耗资产的解法，不成为唯一mandatory key。

## 风险与取舍

队友提前耗尽、卡地图、携带者断线、过强让队友观战；反制靠旁路/空间/真实成本，不偷偷补弹。

## 决策状态

CANON：重资产是需要双手携带、切换常规武器即放下、弹药有限且普通补给不能补充的世界实体。DIRECTION：状态机、越界回收和防 grief 规则由战斗责任文档与原型验证。

## 责任设计文档

[资产规则](../../gdd/combat-and-arsenal.md)；[候选卡](../../content/combat-prototypes.md)；[灰盒分支](../../content/blackstart-greybox-mission.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## 替代关系与下一 Gate

扩展源 Heavy 方向，不占常规 Weapon 槽。必须验证耗空、丢失、断线、恶意浪费与可替代通关路径。
