---
doc_id: DDD-0016
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: BREACH ECHO documentation stewardship
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; delegated decisions DDD-0013–0018"
depends_on: []
---

# 主机迁移、租约和认证恢复点

**Date:** 2026-09-05 · **Authority:** delegated by owner · **Status:** DECIDED, implementation NOT STARTED.

## Decision
每Run小型Durable Object协调epoch/租约；1s逻辑快照+备份ACK认证；快照/已提交状态变更恢复，不重跑PhysX输入。

## Problem and rationale
玩家主机离开与网络分区需要明确唯一权威和实际可恢复状态。

## Alternatives and rejection reasons
拒绝Lobby owner即完整游戏Host方案、全世界60Hz云模拟、零延迟零丢失虚假承诺、分区各侧都继续写。

## Constraints and architecture impact
在线需要可用协调器与合法身份；实际部署/费用OWNER-02。已认证状态无重复遗漏，未认证窗口有明确RPO；拿不到一致证据冻结/挂起。

## Supersedes / preserves
细化NET-002/003/005/006与DDD-0010–0012原恢复要求，区分普通复制与持久恢复水位。

## Reconsideration trigger
分区双主、证书遗漏、可恢复组件不完整即阻止公开联机；若TTL造成过多暂停按真实网络证据重新调TEST，不能牺牲唯一权威。

## Implementation and tests
按实施交接的M0–M6任务落实；验收矩阵保留所有未运行状态。每个实现PR提供原子性、取消/并发/恢复负面测试、真实构建与设备证据。不得把本文选择当作测试结果。

## Responsibility documents and evidence
[host-migration](../../technical/host-migration.md)；[network-and-persistence](../../technical/network-and-persistence.md)；[acceptance-matrix](../../production/acceptance-matrix.md)

决策来源为当前所有者授权；外部技术事实及限制见[技术证据](../../research/technical-evidence-2026-09-05.md)。保留原用户来源与历史Git差异；本文不是用户逐字选择每个技术的记录。
