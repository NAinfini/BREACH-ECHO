---
doc_id: DDD-0013
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: BREACH ECHO documentation stewardship
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; delegated decisions DDD-0013–0018"
depends_on: []
---

# 授权定稿与Operation唯一基础产品

**Date:** 2026-09-05 · **Authority:** delegated by owner · **Status:** DECIDED, implementation NOT STARTED.

## Decision
采用Operation-only基础版；允许助手关闭普通技术/设计分叉；明确CANON/DECIDED/TEST与创作审批，完整登记和可复现交接。

## Problem and rationale
项目有大量历史提案，所有者不懂编程；逐项技术投票会让责任空转。

## Alternatives and rejection reasons
拒绝对等双模式首发（内容/教程/QA/匹配成本翻倍）；拒绝全量无条件CANON（会伪造用户批准与测试）；拒绝只加新概要而不改旧责任规则。

## Constraints and architecture impact
TPS、Bot、Deck、主机迁移和详细战报等明确要求保留，按阶段证明；修改它们需OWNER-04。历史来源不改。

## Supersedes / preserves
DDD-0001与DDD-0006的未决产品/排期方向；旧DEC-001/005等普通分叉。

## Reconsideration trigger
若M1/M2不能证明裸战斗和设施选择有价值，停止扩内容并以证据改设计；不是自动恢复双模式。

## Implementation and tests
按实施交接的M0–M6任务落实；验收矩阵保留所有未运行状态。每个实现PR提供原子性、取消/并发/恢复负面测试、真实构建与设备证据。不得把本文选择当作测试结果。

## Responsibility documents and evidence
[owner-decisions](../owner-decisions.md)；[release-scope](../../production/release-scope.md)；[implementation-handoff](../../production/implementation-handoff.md)

决策来源为当前所有者授权；外部技术事实及限制见[技术证据](../../research/technical-evidence-2026-09-05.md)。保留原用户来源与历史Git差异；本文不是用户逐字选择每个技术的记录。
