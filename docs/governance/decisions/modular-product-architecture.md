---
doc_id: DECISION-MODULAR-PRODUCT-ARCHITECTURE
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["operation-vs-roguelike.md"]
---

# 模块化与公开API

## 背景与用户意图

用户希望官方本体拆模块、玩家可改大部分游戏；担心不留Roguelike接口会重写，随后接受不保留专用接口，但仍期望后期换模块简单。

## 已考虑方案

字面全API公开；所有核心随意热替换；Roguelike专用接口；稳定内核+通用ruleset+内容包；完全不预留边界。

## 证据与假设

源§27与§36支持包/权限/版本固定方向；Factorio/Workshop/UE只作方法案例。未来整模式制作成本未知。

## 决定

MODARCH-001 · CANON/DIRECTION · 来源：本轮用户确认与技术收敛；源依据见责任文档。

Operation 使用通用 Action、Effect、Ruleset、ResourcePolicy、RewardSource、ContentPackage 与 SaveSchema；官方内容和社区 Mod 走同一受验证的包模型。用内部 Combat Lab 验证第二消费者，不建立 `IRoguelike`，也不承诺 Authority、Physics、序列化或整体手感可热插拔。

## 风险与取舍

内容模块复用高，完整模式仍有内容/平衡/UI/教程/QA；核心authority/physics/序列化与整体手感可替换性低。公开所有系统能力有安全/兼容债。

## 决策状态

CANON：模块化本体和公开稳定能力。DIRECTION：具体接缝先由 Operation 的真实消费者塑形，外部作者验证后才冻结公共 API。

## 责任设计文档

[模块化合同](../../technical/modding-and-toolchain.md)；[模拟架构](../../technical/architecture-and-performance.md)；[持久化](../../technical/network-and-persistence.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## 替代关系与下一 Gate

SUPERSEDES：字面“全部 API 公开”和为未来模式预建空接口的解读。垂直切片必须证明 Operation 与 Combat Lab 能在不修改 Kernel 的情况下切换规则；之后再由外部作者测试公共面。
