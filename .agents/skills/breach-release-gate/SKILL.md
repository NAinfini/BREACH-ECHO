---
name: breach-release-gate
description: Use when preparing any BREACH Steam playtest, demo, beta, release candidate, depot upload, public branch, rollback, or store submission.
---

# BREACH Release Gate

## Read first

- `../../../docs/production/platform-and-release.md`
- `../../../docs/production/roadmap-and-validation.md`
- `../../../docs/production/asset-policy-and-provenance.md`
- `../../../docs/technical/modding-and-toolchain.md`

## Gate order

1. Freeze commit, content package lock, Unity/SDK versions, build configuration, target depot, and rollback branch.
2. Require a clean reproducible build with symbols/logs; validate Windows first and Steam Deck when in scope.
3. Run smoke, save/load, migration, network, mod mismatch, controller, accessibility, localization, performance, replay/debrief, and crash-recovery checks appropriate to the release tier.
4. Audit every shipped asset against provenance; unresolved license or AI-disclosure status is a hard stop.
5. Validate Steamworks packages, depots, branches, ownership, Workshop dependencies, store metadata, content survey, languages, and launch options.
6. Upload to a non-public branch, install through Steam as a player would, and retest before promotion.
7. Record promotion and rollback. Never set a public branch live without explicit user authorization.

## Output

Produce an evidence-linked checklist with build/depot IDs, known issues, owner, severity, go/no-go, and rollback target. `NOT RUN` and waivers must be visible.
