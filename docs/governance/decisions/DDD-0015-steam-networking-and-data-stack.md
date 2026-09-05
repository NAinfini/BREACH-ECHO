---
doc_id: DDD-0015
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: BREACH ECHO documentation stewardship
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; delegated decisions DDD-0013–0018"
depends_on: []
---

# Steam网络栈、数据格式与命中历史

**Date:** 2026-09-05 · **Authority:** delegated by owner · **Status:** DECIDED, implementation NOT STARTED.

## Decision
Unity6.3LTS/URP、FishNet+FishySteamworks+Steamworks.NET、Steam Lobbies/SDR；uGUI/TMP；JSON作者定义和有界版本化binary DTO；自有受限hitscan历史。

## Problem and rationale
必须给实现者具体依赖赢家，同时保持Kernel不依赖平台。

## Alternatives and rejection reasons
拒绝NGO/EOS/Photon等并行方案；拒绝以Steam Lobby转移冒充恢复；拒绝假装FishNet内建迁移或已购买Pro ColliderRollback；拒绝任意对象图反序列化。

## Constraints and architecture impact
M0真实构建后固定精确补丁/commit/许可证；未安装兼容组合不编造版本。离线Solo不依赖Steam/云。

## Supersedes / preserves
DDD-0008继续有效并细化6.3；DDD-0010–0012继续拥有命令/60Hz/复制；其中历史provider与rewind OPEN由本决定关闭。

## Reconsideration trigger
实际依赖兼容或性能Spike失败时重审适配实现，保持Gameplay合同；禁止因示例连网就宣布4人恢复通过。

## Implementation and tests
按实施交接的M0–M6任务落实；验收矩阵保留所有未运行状态。每个实现PR提供原子性、取消/并发/恢复负面测试、真实构建与设备证据。不得把本文选择当作测试结果。

## Responsibility documents and evidence
[technology-stack](../../technical/technology-stack.md)；[data-contracts](../../technical/data-contracts.md)；[technical-evidence-2026-09-05](../../research/technical-evidence-2026-09-05.md)

决策来源为当前所有者授权；外部技术事实及限制见[技术证据](../../research/technical-evidence-2026-09-05.md)。保留原用户来源与历史Git差异；本文不是用户逐字选择每个技术的记录。
