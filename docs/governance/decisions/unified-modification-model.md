---
doc_id: DECISION-UNIFIED-MODIFICATION-MODEL
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["operation-field-modifications.md"]
---

# 统一修改模型而非统一玩家概念

## 背景与用户意图

用户提出把武器配件底层做成Relic，方便未来rework。

## 已考虑方案

配件继承RelicBase；两套效果系统；统一ModificationDefinition/Effect，按scope和presentation区分。

## 证据与假设

共同点是效果与事件，差异是目标/挂点/成本/视觉/模式；共享数据结构不能证明共享平衡。

## 决定

MODMODEL-001 · CANON/DIRECTION · 来源：本轮用户确认与技术收敛；源依据见责任文档。

单一ModificationDefinition含scope、mount、compatible_tags、effect_graph、权限、tradeoffs、冲突、visual、allowlist与版本；WeaponModule/ToolModule/TeamProtocol/Relic用同一schema。Operation推荐不启用自动Fusion。

## 风险与取舍

自动吞实体配件伤害所有权；给所有效果同mode资格会破坏资源管理；提前冻结schema产生兼容债。

## 决策状态

CANON：武器、工具、团队协议与未来 Relic 共用统一修改/效果模型；Operation 不启用自动 Fusion。DIRECTION：具体字段在实现与作者测试中收敛，未发布前允许破坏性调整。

## 责任设计文档

[修改与Fusion](../../gdd/field-modifications-and-effect-system.md)；[注册与权限](../../technical/modding-and-toolchain.md)；[内容卡](../../content/modification-catalog.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## 替代关系与下一 Gate

SUPERSEDES：源 §9.5 在 Operation 中的自动全局应用。自动 Fusion 只保留为 Lab/未来 Descent 实验，不进入基础版奖励池。
