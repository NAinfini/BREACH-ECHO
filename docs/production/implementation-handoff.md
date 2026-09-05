---
doc_id: PROD-HANDOFF
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: 制作与工程负责人
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; DDD-0018"
depends_on: ["release-scope.md", "acceptance-matrix.md", "../technical/technology-stack.md", "../governance/owner-decisions.md"]
---

# Implementation handoff / 从文档开始制作

## Current reality

The repository is a documentation baseline. There is no playable Unity project, game build, measured benchmark, purchased asset inventory, deployed service or completed playtest in this change. Every milestone below is **NOT STARTED** until its evidence is attached. The documentation checks are real checks of documents, not substitutes for these milestones.

The owner is not expected to know Unity, C#, rigs, transports or build settings. A contributor must deliver a runnable build and an understandable test guide, not a pile of scripts that require the owner to assemble a game manually.

## First executable task: M0

Read root AGENTS, the project documentation skill, release scope, stack, architecture and data contracts. Create one Unity 6.3 LTS URP project under `game/`. Put gameplay code in local packages under `game/Packages/com.breach.*`, author definitions under `game/Content`, scene/prefab presentation under `game/Assets/Breach`, third-party licensed imports under a separately access-controlled asset workflow, and tests beside their owning packages. The eventual Unity repository layout is a planned implementation, not directories that already contain working code.

Create Bootstrap and CombatSandbox scenes, one local-authority player capsule, a camera, a hitscan target, one original graybox weapon, an Input System action map and a small debug HUD. Install only dependencies required to run this path; pin all exact versions that were actually built. Run one EditMode data-validation test, one PlayMode command-to-damage test, and a Windows x64 standalone build. Make game code independent of Steam so this build runs without online service credentials.

**M0 acceptance:** a clean checkout with the documented authorized asset source can reproduce the same build using written steps; no missing Inspector reference, compile error, unlicensed redistributable, embedded credential or hand-edited machine path. Deliver the package/version list, test logs, executable/artifact access location and a guide: launch, move, aim, shoot the target, quit, report what happened. M0 does not pass merely because a scene opens in the Editor.

## Milestone backlog and dependencies

| Work ID | Dependency | Deliverable | Acceptance evidence / responsibility |
|---|---|---|---|
| M0 Bootstrap | none | Reproducible scene, local authority, input and build | STACK installation matrix, clean clone build, automated smoke tests; engineering |
| M1 Combat feel | M0 | AR + shotgun, tool + tactical module, segmented reload, two enemy roles, damage/parts, quick melee | A-COMBAT; zero-modification player observations and frame-time captures; gameplay/UX |
| M2 Complete solo loop | M1 | Mini BLACKSTART, one route choice, Terminal, three-Cell Cart subset, support, down/recovery, upload, exit/wipe, detailed summary | A-SOLO/A-ECONOMY; end-to-end executable and recorded resource ledger; game design |
| M3a Network semantics | M2 | Two then four players, commands/prediction, reliable outcomes, interest, late join, claims | A-NET; transport-independent tests then real Steam devices/accounts; networking |
| M3b Recovery and packages | M3a | Exact package locks, durable checkpoints, coordinator lease, graceful/abrupt migration | A-RECOVERY/A-MODS; fault-injection matrix and actual bandwidth; networking/security |
| M4 Procedural content | M2 + stable M3 contracts | Typed room grammar, deterministic generation, resource/route solver, six mission-family progression | A-PCG; batch seed validation plus human variety tests; level/content |
| M5a Player completeness | M1–M4 | TPS, optional bots, all controller menus, accessibility, complete HUD | A-INPUT/A-BOTS; keyboard/controller and FPS/TPS parity; gameplay/UX |
| M5b Content and identity | M4 + OWNER-01/03 | Approved four characters, environment kit, six weapons, audio, story collections | A-NARRATIVE/A-ASSETS; provenance/rig review and context tests; content/art/audio |
| M5c Mod and replay experience | M3b + M4 | Full built-in Mod Manager, author CLI examples, bounded replay viewer | A-MODS/A-REPLAY; external author/new-user tests; tools/UX |
| M6 Release candidate | all release contracts + OWNER-02 | Platform build, performance/accessibility/security and licensing evidence, demo transfer | A-RELEASE; reproducible signed-off evidence set; production |

No task has an assigned fictional employee or fabricated estimate. The owner/developer records actual hours and blockers after each task; calendar forecasts follow observed throughput. A critical failure stops the dependent expansion, not unrelated cheap investigations.

## Interface ownership and review

Kernel owns commands, state, entity identity, effects and transactions. Operation owns the current mode policies and mission lifecycle. Content owns definitions and validated capabilities. Simulation owns mutable world truth. Network owns delivery/prediction/projection, not a competing truth. Persistence owns serialization and claim idempotency. Platform owns Steam/cloud bindings. Presentation owns camera, animation, UI, sound and visual density. Tests instantiate the same gameplay contracts as production.

An implementation PR names the rule IDs it implements, includes positive and negative tests, and states which design risks remain. No global event bus may hide mandatory data ownership. Service interfaces need actual consumers; do not add generic extension points solely because a future mode might need them. Changes to an explicit owner requirement go through OWNER-04, while ordinary evidence-led implementation changes are delegated.

## Definition of done for one feature

A feature is done only when the player path works in a standalone build; state ownership, cancellation, concurrency, save/recovery and solo/co-op behavior are tested; controller/UI errors are understandable; content can be authored without secret manual steps; tests and performance deltas are recorded; responsibility docs and the backlog reflect reality. A stub, a TODO, a class name, a mocked cloud response or an attractive screenshot is not the finished feature.

## Playtest delivery to the owner

Each build includes a one-page README explaining what to launch, controls, one specific thing to try, expected behavior, known issues and the log location. Ask the owner concrete experience questions such as “Was the power choice understandable?” rather than “Is the ECS architecture good?” Collect bugs as observed behavior, expected behavior, reproduction steps, build ID and seed. Do not require them to diagnose the cause.

## Unblocking dependencies

Unapproved character identity uses neutral Seat 01–04 and placeholder callouts. Unapproved assets use original grayboxes. Unapproved cloud spend uses local coordinator integration tests; this cannot satisfy real-online release gates. An absent Steam partner setup is a deployment blocker, not a reason to invent AppIDs or borrow credentials. Secret partner materials and licensed asset archives stay out of this public repository and public Actions artifacts.

## Handoff record to maintain after each implementation task

Record task ID; starting/ending commit; rule IDs; files and interfaces changed; exact tests/build commands and results; hardware/seed/settings; unrun tests with reasons; performance/bug evidence; new decisions; remaining risks; next single executable task. Do not replace this record with a promise to work later or a memory-only summary.
