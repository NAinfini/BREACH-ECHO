# BREACH ECHO contributor and agent instructions

## Read before changing anything

Read `README.md`, `docs/start-here.md`, `docs/governance/authoring-guide.md`, `docs/production/release-scope.md`, `docs/production/implementation-handoff.md`, and the responsibility documents for your task. Use `.agents/skills/breach-documentation/SKILL.md` for documentation and decisions. The complete document register is `docs/governance/document-register.md`; do not substitute a chat summary for reading the relevant files.

## Authority and delegated judgment

The owner is new to making games and explicitly delegates ordinary technical and design decisions. Choose a clear, defensible winner; do not ask the owner to pick networking libraries, serialization formats, folder structures, balancing coefficients, or routine implementation details. Record the decision, reasoning, rejected alternatives, constraints, impacts and tests in Git in the same change.

Preserve explicit owner requirements. Approval is still required for the items in `docs/governance/owner-decisions.md`: final narrative/character identity, irreversible brand/art/voice commitments, actual spending/contracts/account access, and changing an explicit requirement. Offer a recommendation with each genuine owner question. Never call a delegated decision a direct owner confirmation. Challenge weak suggestions respectfully rather than agreeing automatically.

## Implementation discipline

Implement a complete thin playable path before broad content. Follow the milestone dependencies; a document is not an implementation. Do not scaffold an entire engine, a second mode, a general-purpose visual editor or arbitrary native mod execution to satisfy hypothetical future users. Architectural rework is permitted when justified. Remove superseded runtime paths rather than maintaining legacy implementations. Released user progression still requires a deliberate preservation/migration policy; “no legacy code” is not permission to destroy saves.

Use the selected stack. Core gameplay cannot depend on Steam IDs, transport callbacks, Unity scene instance IDs, view frame rate, audio playback duration, or a particular mod marketplace. Host and client actions use the same validated command path. No hidden enemy rescaling, outcome-dropping performance caps, infinite-resource exploits, checkpoint reload exploits, or client-authored rewards.

Official content uses the same validated package path as supported mods. A hash is not a trust signature. Untrusted content cannot access arbitrary C#, native DLLs, process execution, filesystem, sockets, credentials, account writes or coordinator signing keys. Never upload licensed purchased assets to this public repository, a public SDK, Workshop examples or a public CI artifact without explicit redistribution rights.

## Work and verification

Start each substantial task with a durable task plan, rule IDs, acceptance tests and the current commit. Report progress and blockers in the current session. Use small coherent commits; do not force-push or overwrite another contributor's changes. Test negative paths, rollback and reconnection as well as the happy path. Update the responsible documents, decision register, backlog and handoff when a rule changes.

Run `python3 tools/validate_docs.py`, its self-tests, and `python3 tools/docs_audit.py` for documentation changes. When game tooling exists, run the task's specified EditMode, PlayMode, build, integration and device tests. Record exact commands, commit/build, seed, hardware, input mode, settings and measured results. Do not invent logs, screenshots, benchmarks, external reviewers or completed gates. Do not replace an unpassed test with a weaker threshold merely to make it pass.

## Narrative review boundary

The owner must review the complete story overview before a genuinely new, read-only, no-project-context reviewer examines the story. Do not call yourself an independent blind reviewer or silently approve the four character candidates. Missing age/body/appearance/voice decisions are intentional owner deferrals, not blanks to fill with stereotypes.

## Handoff at the end of a task

State what changed, the commit, tests actually run, unrun tests and why, known risks, and the next executable task. Mark implementation status separately from design authority. Leave enough information for a new person to continue without this conversation. Never promise unattended future work unless a real authorized automation was created.
