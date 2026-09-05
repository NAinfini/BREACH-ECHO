---
doc_id: DDD-0017
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: BREACH ECHO documentation stewardship
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; delegated decisions DDD-0013–0018"
depends_on: []
---

# 安全模组首版、精确包锁与原生管理器

**Date:** 2026-09-05 · **Authority:** delegated by owner · **Status:** DECIDED, implementation NOT STARTED.

## Decision
首版Data/有界Graph/允许资源；无任意脚本/Native；完整内置Mod Manager；Workshop分支版本配合应用hash缓存，旧hash不可得明确拒绝。

## Problem and rationale
全开放愿景与普通玩家自动同步的安全/授权边界必须可执行。

## Alternatives and rejection reasons
拒绝加入Lobby即运行DLL；拒绝把hash当安全认证；拒绝静默更新挂起Run；拒绝Host直传他人购入资产或另建公共分发市场。

## Constraints and architecture impact
官方内容同路径验证，敏感运行时权力不公开；依赖/资源/Graph成本有界；完整TC/Forge/更强脚本未来单独Gate。

## Supersedes / preserves
细化DDD-0003/0004/0009及MOD-015/018的语言、UI、Native和旧版本未决项；Steam-only既有要求保留。

## Reconsideration trigger
恶意包执行、路径逃逸、半激活、旧hash丢失被掩盖即阻止发布；新脚本能力需新的威胁建模和独立评审。

## Implementation and tests
按实施交接的M0–M6任务落实；验收矩阵保留所有未运行状态。每个实现PR提供原子性、取消/并发/恢复负面测试、真实构建与设备证据。不得把本文选择当作测试结果。

## Responsibility documents and evidence
[mod-security-and-sync](../../technical/mod-security-and-sync.md)；[mod-manager](../../gdd/mod-manager.md)；[modding-and-toolchain](../../technical/modding-and-toolchain.md)

决策来源为当前所有者授权；外部技术事实及限制见[技术证据](../../research/technical-evidence-2026-09-05.md)。保留原用户来源与历史Git差异；本文不是用户逐字选择每个技术的记录。
