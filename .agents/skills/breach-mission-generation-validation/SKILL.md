---
name: breach-mission-generation-validation
description: Use when creating, changing, or validating BREACH procedural Operation layouts, mission graphs, side objectives, glyph secrets, encounters, resource placement, extraction routes, or generation weights.
---

# BREACH Mission Generation Validation

## Read first

- `../../../docs/gdd/missions-and-spaces.md`
- `../../../docs/gdd/operation-game-mode.md`
- `../../../docs/gdd/encounters-and-difficulty.md`
- `../../../docs/content/blackstart-greybox-mission.md`

## Validation contract

For every tested seed, prove:

- spawn, critical path, objective dependencies, and extraction are connected;
- every required key, tool, terminal, heavy weapon, target, and interaction spawns before mandatory use;
- doors, glyph reroutes, secret rooms, lockdowns, and destructible barriers cannot permanently soft-lock the run;
- runtime navigation reaches all required combat and interaction spaces;
- enemy, ammo, medical, resource, and reward budgets stay inside declared difficulty bounds;
- hidden glyph routes add optional risk/reward and never conceal mandatory progression;
- the same seed and content package lock reproduce the same mission structure.

Run deterministic batch generation when a harness exists, then manually play representative edge seeds. Store failure seeds and the smallest reproducing package set. Never silently reroll invalid seeds at runtime.

## Output

Report seed count, generation and invariant failures, worst resource extremes, representative captures, and retained regression seeds. Missing quantitative bounds are a design blocker.
