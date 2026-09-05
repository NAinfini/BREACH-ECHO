---
name: breach-mod-package-validation
description: Use when reviewing or validating a BREACH Steam Workshop mod, modpack, ContentPackage schema, dependency graph, Luau script, cooked asset bundle, hash lock, or host-to-client synchronization behavior.
---

# BREACH Mod Package Validation

## Read first

- `../../../docs/technical/modding-and-toolchain.md`
- `../../../docs/governance/decisions/agent-first-modding-runtime.md`
- `../../../docs/governance/decisions/steam-workshop-mod-runtime.md`
- `../../../docs/governance/decisions/modular-product-architecture.md`

## Hard rules

- Steam and Steam Workshop are the initial-release distribution boundary.
- Native DLL loading is forbidden.
- Luau uses a capability sandbox with explicit budgets; filesystem, process, arbitrary network, reflection, and native interop are denied by default.
- Every content object uses a stable namespaced ID, never a display name, file path, or load order.
- Resolve a dependency DAG, reject cycles, verify versions and hashes, and produce deterministic package order.
- Host package lock is authoritative. Missing, extra, or mismatched required content cannot enter gameplay.
- First-party and Workshop weapons, characters, maps, missions, and data pass the same schema/runtime gates.

## Checks and output

Validate manifest/schema, dependency closure, hashes, asset allowlist, cooked-asset compatibility, Luau policy and quotas, ID collisions, localization keys, replication declarations, save/replay compatibility, and unload cleanup. Fuzz hostile parser inputs. Return machine-readable results plus package ID/version/hash, dependencies, denied capabilities, warnings, failures, and reproduction inputs. Never auto-grant a capability.
