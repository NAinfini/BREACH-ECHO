---
doc_id: DECISION-BASE-GAME-MODE
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["../authoring-guide.md"]
---

# 产品分叉与首发核心

## 背景与用户意图

用户最初同时想要 GTFO 式 Operation 与 Roguelike，后来明确基础版优先做高紧张、资源管理和合作任务；Descent 只在未来 DLC 中作为真正的 Roguelike 模式出现。

## 已考虑方案

纯Operation无成长；Operation加少量局内变化；纯Descent；对等双模式首发；固定解谜本体后加Roguelike。

## 证据与假设

源§4双模式是现有归档基线；GTFO与Rogue Core市场页面只证明相邻产品存在。任务层是否提高复玩尚无测试。

## 决定

MODEDEC-001 · CANON · 来源：本轮用户确认；源依据见责任文档。

基础版只有 Operation：明确任务、不确定局势、稀缺资源、团队执行，以及少量武器/工具改装。Descent 不进入基础版范围；内部 Combat Lab 只验证规则扩展性，不作为第二个发布模式。底层保持通用模块边界，但不预建 Roguelike 专用接口。

## 风险与取舍

牺牲部分肉鸽玩家即时成长满足；需证明设施规划值得其等待/失败成本；单模式仍不自动降低枪感与合作难度。

## 决策状态

CANON：Operation-only 基础版。FUTURE：Descent DLC 是否进入制作，必须在基础循环被试玩证明后另立范围与 Gate。

## 责任设计文档

[产品愿景](../../gdd/game-vision-and-design-pillars.md)；[Operation](../../gdd/operation-game-mode.md)；[Descent](../../gdd/descent-future-game-mode.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## 替代关系与下一 Gate

SUPERSEDES：SRC-SSOT-2.0 §1.1、§4 中“两个模式对等进入基础版”的解读。若裸战斗、资源规划或程序任务在垂直切片中失败，先修或缩减 Operation，不自动恢复双模式首发。
