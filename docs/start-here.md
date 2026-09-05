---
doc_id: GUIDE-START
doc_type: guide
stage: BASELINE
updated: 2026-09-05
owner_role: Product and production lead
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; DDD-0013"
depends_on: ["production/release-scope.md", "governance/owner-decisions.md", "production/implementation-handoff.md"]
---

# Start here: how we will turn this into a game

## What this project is

BREACH: ECHO is a cooperative game for one to four players. You are a fixed team working for a city called 壁垒. The city needs supplies and working machinery. Your team enters abandoned or hostile facilities, chooses how to use limited ammunition and resources, completes a contract, and tries to leave alive. Opening a route or restoring power can help you and also create danger.

The base game is **Operation**, not two games developed at once. Missions are assembled from carefully authored rooms and situations. Randomization rearranges compatible content; it is not expected to invent interesting levels by itself. Descent, the faster roguelike planetary expedition mode, is future work with its own approval gate.

## What has been decided and what has not

The baseline is a set of instructions for building and testing, not evidence that the game is already fun or finished. `CANON` means an explicit owner requirement; `DECIDED` means a choice made under your delegation; `TEST` means an initial value or experiment we must measure. Narrative candidates that need your approval remain clearly marked. The [complete authority rules](governance/authoring-guide.md) explain how conflicts are resolved.

Ordinary technical choices have winners. We will not ask you to choose unfamiliar networking libraries or code architecture. We will ask you about the game's final identity, the four characters, the final story, actual budgets and contracts, and any proposed change to something you explicitly required. The [owner decision queue](governance/owner-decisions.md) is the only place that asks for those approvals.

## You do not need to code the game

Your practical role is to approve identity and spending, give access through safe account connections when required, play builds, and describe what feels good or bad. An implementation agent or developer creates and tests the project, diagnoses bugs, writes the build instructions, and provides an executable for you to play. A specialist may still be needed for animation, art, sound, platform work or security when a gate cannot be met; nothing here assumes those people have been hired.

You should never need to copy unexplained scripts into a game directory, edit a server database, or repair an Inspector one field at a time just to evaluate a build. The agent must supply a short “open this, press this, report these observations” guide with each playable milestone.

## Build order

| Step | What you can see or play | What it proves |
|---|---|---|
| M0 — project bootstrap | One scene, one player, a target, automated checks, a Windows build | The chosen tools build reproducibly and the project is not just documents |
| M1 — feel and resource proof | A small room with movement, two guns, one tool, one tactical module and two enemies | Shooting, movement, readable threats and finite ammunition are enjoyable before progression hides weaknesses |
| M2 — miniature BLACKSTART | A complete short solo contract: enter, find information, make a power choice, fight, recover, extract, see a report | The core loop works without bots or a giant map |
| M3 — cooperative reliability | Two, then four players; join/rejoin, host loss, shared pickups and resource transactions | The game survives real network failures without duplicate rewards or lost authority |
| M4 — procedural replayability | Several authored room sets assembled into valid new contracts | Variety, route choice and resource solvability survive changing layouts |
| M5 — complete base-game features | Remaining mission families, content, bots, TPS, accessibility, safe mods, final art and presentation | The release contract is implemented rather than inferred from a prototype |
| M6 — release evidence | Stranger playtests, Steam Deck profiling, recovery/security tests, licenses and release checklist | Whether we should actually ship |

Milestones are dependencies, not calendar promises. We have no approved staffing, spending plan or measured velocity. Failing a gate means fixing the cause or proposing a documented scope change—not pretending the gate passed.

## How to read without reading everything at once

First read [the scope](production/release-scope.md) and [owner decisions](governance/owner-decisions.md). For the experience, read [vision](gdd/vision.md), [Operation](gdd/operations.md), and [BLACKSTART](content/blackstart.md). For the story, read [the complete overview for your review](gdd/story-overview.md), then the character and world documents it links.

A new developer starts with [implementation handoff](production/implementation-handoff.md) and [technology stack](technical/technology-stack.md), then follows the linked rule owners. A writer, artist or tester uses the role paths in [the documentation map](README.md). The [document register](governance/document-register.md) lists every Markdown document, including historical sources, templates and the skill; nothing relies on remembering a chat title.

## Small glossary

A **prototype** tests a risky idea cheaply. A **vertical slice** is one small but complete representative part of the game. A **host** is the player's machine running the shared world. **Authority** means who is allowed to decide the real result. A **package** is a named, versioned set of content. A **gate** is a test that must pass before we spend more effort. A **decision record** explains a choice and what evidence could overturn it. More definitions are in [the glossary](glossary.md).

## What to do next

Development can start at M0 without final character art, paid models or complete voice acting. Read the story overview and the small owner queue while the first implementation task remains a reproducible graybox project. No subscription purchase or public launch action is authorized merely because it appears in these documents.
