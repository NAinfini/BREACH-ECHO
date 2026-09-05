# BREACH: ECHO · 裂界残响

**A 1–4 player cooperative PvE game about entering dangerous facilities, making limited resources count, changing the battlefield, and extracting together.**

This repository currently contains the game's design and production documentation, not a playable Unity project. The 2026-09-05 documentation baseline selects one implementable direction and records the remaining owner approvals. A decision being accepted does not mean it has been coded, playtested, legally cleared, or independently reviewed.

## Start here

| You are… | Read first | Then |
|---|---|---|
| The owner, with no game-development experience | [Start here](docs/start-here.md) | [Decisions only you need to make](docs/governance/owner-decisions.md) |
| A new programmer or coding agent | [Agent instructions](AGENTS.md) | [Implementation handoff](docs/production/implementation-handoff.md), then the responsibility documents for the assigned task |
| A designer, artist, writer, or tester | [Documentation map](docs/README.md) | [Release scope](docs/production/release-scope.md) and [complete document register](docs/governance/document-register.md) |
| Reviewing why something was chosen | [Decision register](docs/governance/decision-register.md) | The linked design decision record and its evidence |

## Current direction

Operation is the only base-game mode. Descent is a future expansion, not a second launch production. Unity 6.3 LTS, URP, GameObject-first C#, host-authoritative commands, a 60 Hz simulation, and semantic snapshot/event replication are the implementation baseline. Technical dependency choices are in [the stack specification](docs/technical/technology-stack.md); do not install competing frameworks from old proposals.

The four fixed characters survive in canon. Ordinary missions do not advance a personal campaign or permanent node-conquest map. Players bring two guns, one tool and one freely selectable tactical module; finite supplies, weapon modifications, facility decisions and shared heavy equipment create the variation. Staffs, unrestricted Relic accumulation and automatic Fusion are not Operation rules.

## Documentation maintenance

The detailed design remains primarily Chinese, with stable English technical identifiers. These English entry points explain the project without requiring knowledge of game-development terminology. File names use descriptive English kebab-case; version numbers belong in Git and metadata, not names such as `final-v7`.

Run `python3 tools/validate_docs.py` and `python3 tools/docs_audit.py` from the repository root. These validate documentation structure and preserve an inventory; they are not game tests. Historical source snapshots remain under [docs/sources](docs/sources/evidence-register.md). Current rules are owned by the indexed design and technical documents, not those snapshots.
