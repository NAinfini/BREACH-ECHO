---
name: breach-unity-verification
description: Use when verifying any BREACH Unity scene, prefab, gameplay change, package update, build, or release candidate. Enforces evidence-based EditMode, PlayMode, Console, build, screenshot, and performance checks for this repository.
---

# BREACH Unity Verification

Verify only the requested acceptance criteria.

## Read first

- `../../../docs/technical/architecture-and-performance.md`
- `../../../docs/production/roadmap-and-validation.md`
- The decision document governing the changed system.

## Procedure

1. Detect the actual Unity project, Editor version, package versions, and test assemblies. Never invent a command or assume a scene is open.
2. If Unity CLI is available, run `unity status --format json` before touching scenes or assets. Use connected-Editor commands when available; do not hand-edit serialized Unity YAML behind a live Editor.
3. Run the narrowest relevant EditMode and PlayMode tests. Record the exact command, exit code, failing test, and artifact path.
4. Read the Console after compilation and PlayMode. New errors are a hard failure; new warnings require an explicit disposition.
5. For visual or interaction changes, capture an in-game artifact at the target resolution and verify the active scene, camera, and state.
6. For build-affecting changes, run a headless Windows build through the project build entry point. Compilation alone is not a build pass.
7. For performance-sensitive changes, report hardware, scene, build type, sample duration, frame-time percentile, GC allocation, and profiler capture path.

## Output

Return a table of acceptance criterion, evidence, result, and unresolved risk. Mark blocked checks `NOT RUN` with the exact reason. Missing tools, licenses, or tests never count as a pass.

## Stop conditions

Stop mutation on serialization corruption, repeated Editor crash, unexpected scene-wide changes, missing project ownership, or risk of overwriting user work.
