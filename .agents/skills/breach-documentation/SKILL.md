---
name: breach-documentation
description: Review, finalize, and maintain BREACH ECHO game-design and technical documents, with explicit delegated decisions, evidence, scope control, and complete handoff.
---

# BREACH ECHO documentation skill

Use this skill for game documentation, architecture decisions, scope changes, audits, or handoffs. It is a project-local skill, not a claim that an external specialist or independent reviewer has participated.

## Read and establish authority

Read the root README and AGENTS when present, then docs/README.md, the authoring guide, decision register, relevant responsibility documents, and referenced decisions. Inspect the actual repository, not memory alone. Preserve explicit owner decisions. Source snapshots are immutable historical evidence, not an alternative active specification.

The owner delegated ordinary design and technical choices on 2026-09-05: choose a defensible winner without asking them to select unfamiliar technology. Label a delegated decision as delegated, never as a direct owner quote. Ask only about non-delegated creative identity, actual spending/contractual commitments, account access, or changes to explicit owner requirements. Do not accept a weak suggestion merely because the owner proposed it; explain tradeoffs respectfully.

## Review four passes

1. Product and gameplay: identify the player promise, complete playable loop, smallest proof, explicit release versus later scope, input/state/resource/ownership/failure semantics, solo/co-op differences, accessibility and measurable acceptance.
2. Architecture and production: trace commands through authority, transactions, state replication, persistence and recovery. Choose concrete dependencies with primary-source evidence. Distinguish a capability offered by a library from a BREACH implementation that must still be written. No speculative platform framework or legacy runtime compatibility.
3. Content and safety: check narrative causality and knowledge boundaries, procedural solvability, asset provenance, mod trust boundaries, permissions, save integrity and licensing review gates. Do not invent legal clearance, purchased licenses, benchmarks or completed tests.
4. Handoff and integrity: one responsibility owner per rule, stable IDs, descriptive kebab-case names, relative links, complete registry, a beginner reading path, implementation order, owner decision queue and automated validation.

## Decision record

For each consequential decision record: ID; date; authority (owner/delegated); decision; problem; alternatives and rejection reasons; constraints; affected documents and interfaces; failure/reconsideration condition; implementation and test follow-ups; evidence. A selected approach may have TEST tuning values and an unpassed implementation gate. Never relabel an experiment as measured proof.

## Completion and honesty

Preserve all unreplaced design details and original sources. Resolve conflicts in their responsibility documents, not only in a new overview. Archive superseded proposals explicitly. No blanket conversion of every PROPOSED/OPEN value to CANON. Separate document maturity, decision authority, implementation status and validation evidence.

Run document checks; inspect their output; correct failures; verify the remote commit and changed files. Do not claim a game build, a playtest, a security audit, an independent blind review or a performance target passed unless that work actually occurred. If repository access or a check fails, record the failure and the exact unfinished boundary. Finish with the actual repository result and only the decisions that still require the owner.
