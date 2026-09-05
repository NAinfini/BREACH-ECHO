---
name: breach-network-soak
description: Use when testing BREACH multiplayer authority, lag compensation, host migration, join-in-progress, Steam lobby behavior, package locks, or networked replay consistency under latency, jitter, packet loss, and disconnects.
---

# BREACH Network Soak

## Read first

- `../../../docs/technical/network-and-persistence.md`
- `../../../docs/governance/decisions/network-runtime-and-recovery.md`
- `../../../docs/governance/decisions/host-authority-and-gameplay-commands.md`
- `../../../docs/governance/decisions/state-replication.md`
- `../../../docs/governance/decisions/lag-compensation-and-server-rewind.md`

## Required matrix

Test 1, 2, and 4 clients where the harness supports them. Include clean LAN, 80 ms, 120 ms, asymmetric latency, jitter, packet loss, host loss, reconnect, late join, and a mismatched mod/package hash. Fix and retain the random seed for every failure.

## Invariants

- Host authority is the only gameplay truth; clients cannot commit damage, inventory, objective, or resource state.
- Reconciliation never duplicates shots, pickups, rewards, enemies, or objective completion.
- Authority epoch changes exactly once per successful migration and stale commands are rejected.
- Rewind stays inside the documented window and never treats projectiles as hitscan.
- Package-lock mismatch fails clearly before gameplay.
- A dropped client cannot leave an unrecoverable objective or permanent reservation.

## Evidence

Capture build/version, runtime version, topology, seed, impairment profile, duration, synchronized client logs, authority epochs, disconnect timeline, final state hash, and reproduction steps. Stop on divergence, duplicate reward, split-brain, crash, or boundary bypass; do not hide failures with retries.
