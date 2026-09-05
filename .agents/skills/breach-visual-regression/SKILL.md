---
name: breach-visual-regression
description: Use when validating BREACH art direction, lighting, materials, VFX, UI rendering, model imports, camera presentation, or renderer changes against approved references across target scenes and quality settings.
---

# BREACH Visual Regression

## Read first

- `../../../docs/gdd/art-direction.md`
- `../../../docs/production/asset-policy-and-provenance.md`
- `../../../docs/governance/decisions/unity-engine-and-rendering.md`

## Capture contract

Use fixed scene, camera, seed, resolution, aspect, quality, render-pipeline version, color space, and exposure. Record hardware and build type. Never compare uncontrolled Editor viewpoints.

Capture bright, dark, combat, stealth, VFX-heavy, UI-overlay, and character/weapon inspection states. Compare composition, silhouette readability, value hierarchy, material response, temporal stability, safe areas, clipping, missing shaders, particles, shadows, and exposure.

Pixel diffs are supporting evidence, not the verdict: TAA, film grain, particles, and nondeterministic simulation require masks or perceptual thresholds. A baseline change must cite the design decision it implements; never regenerate a baseline only to make a test green.

## Output

Retain baseline, candidate, diff/overlay, capture metadata, threshold, disposition, and reviewer notes. Hard-stop on missing shaders, broken framing, illegible critical UI, severe clipping, or contradiction of approved art direction.
