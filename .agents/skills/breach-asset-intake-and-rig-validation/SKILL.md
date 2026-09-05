---
name: breach-asset-intake-and-rig-validation
description: Use when buying, generating, importing, modifying, rigging, retargeting, texturing, LODing, or approving any BREACH 3D character, creature, weapon, prop, environment kit, animation, or material.
---

# BREACH Asset Intake and Rig Validation

## Read first

- `../../../docs/production/asset-policy-and-provenance.md`
- `../../../docs/gdd/art-direction.md`
- `../../../docs/technical/architecture-and-performance.md`

## Intake gate

Record creator/vendor, source URL or generation tool, acquisition date, invoice/evidence, license text/version, allowed uses, attribution, AI status, source-file availability, and modification history. Quarantine unknown or incompatible provenance.

## DCC gate

Verify meters, axes, transforms, pivots, naming, topology, normals/tangents, UVs, texel density, PBR channels, material count, texture dimensions, transparency, and dependencies. For rigs verify hierarchy, root-motion policy, bind pose, bone orientation, deformation coverage, normalized weights, IK targets, facial setup when present, and retarget pose.

For animation, test idle-to-move, locomotion extremes, aim offsets, reload/interaction contacts, foot planting, hand-to-prop alignment, clipping, root motion, and loop seams. AI-generated meshes do not bypass retopology, UV, rigging, weight, or license gates.

## Unity gate and evidence

Use the project import preset; verify scale, Avatar, clips/events, materials, LODGroup, colliders, sockets, bounds, culling, batching/instancing, memory, and target build. Test one real gameplay action, not only a turntable. Retain provenance, source/export hashes, wireframe/weight captures, turntable, Unity import, gameplay capture, budgets, and an accepted/repair/rejected disposition.
