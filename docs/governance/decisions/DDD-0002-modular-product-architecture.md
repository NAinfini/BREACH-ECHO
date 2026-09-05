---
doc_id: DDD-0002
doc_type: decision
stage: ARCHIVE
updated: 2026-09-05
owner_role: 产品与系统设计负责人
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["../decision-register.md"]
---

# 模块化与公开API

## Context / User intent

用户希望官方本体拆模块、玩家可改大部分游戏；担心不留Roguelike接口会重写，随后接受不保留专用接口，但仍期望后期换模块简单。

## Options considered

字面全API公开；所有核心随意热替换；Roguelike专用接口；稳定内核+通用ruleset+内容包；完全不预留边界。

## Evidence / assumptions

源§27与§36支持包/权限/版本固定方向；Factorio/Workshop/UE只作方法案例。未来整模式制作成本未知。

## Review recommendation

DDD-0002-REC · PROPOSED · 来源：本轮讨论评审；源依据见责任文档。

当前由Operation实际消费通用Action/Effect/Ruleset/ResourcePolicy/RewardSource/ContentPackage/SaveSchema，并用10分钟Lab验证第二消费者；不建IRoguelike，不冻结未验证public API。

## Risks / tradeoffs

内容模块复用高，完整模式仍有内容/平衡/UI/教程/QA；核心authority/physics/序列化与整体手感可替换性低。公开所有系统能力有安全/兼容债。

## Decision status

DIRECTION：用户模块化偏好明确；PROPOSED：具体接缝、权限与冻结时机。

## Owner GDD links

[模块化合同](../../technical/modding-and-toolchain.md)；[模拟架构](../../technical/architecture-and-performance.md)；[持久化](../../technical/network-and-persistence.md)。具体规则只由责任文档维护，本文件保留选择理由，不复制整套规范。

## Supersedes / next gate

没有已批准替代架构；Week8 Operation/Lab不改Kernel切规则，slice后精选作者验证。



## 2026-09-05 disposition / 历史状态

本文件保留当时的选项和理由，旧OPEN不是当前未决入口。产品/装备/技术/制作问题已由DDD-0013–0018决定，人物与完整故事仍通过OWNER-01审阅；请读[当前决策登记](../decision-register.md)。不再按本文旧日期或未批准推荐直接实施。
