---
name: breach-localization-and-accessibility
description: Use when adding or changing BREACH player-facing text, subtitles, HUD, menus, prompts, controller navigation, language support, fonts, color communication, or accessibility settings in Unity.
---

# BREACH Localization and Accessibility

## Read first

- `../../../docs/gdd/ux-and-accessibility.md`
- `../../../docs/gdd/narrative-delivery.md`
- `../../../docs/gdd/world-naming.md`

## Localization rules

- Player-facing strings use stable semantic keys; never concatenate sentences or use display text as identity.
- Use parameterized messages and locale-aware plural, number, date, and input-glyph formatting.
- Preserve Chinese and English terminology from the naming source of truth.
- Define font fallback for Simplified Chinese, Latin, symbols, and controller glyphs.
- Run pseudo-localization for expansion, truncation, bidirectional safety where supported, and unlocalized-string detection.
- Subtitles separate speaker, text, timing, non-speech audio, and presentation from recorded audio.

## Accessibility and evidence

Verify text scaling, contrast, color-independent information, subtitle controls, remapping, hold/toggle alternatives, motion/camera options, audio cues, keyboard/gamepad focus, and no pointer-only critical flow. Capture localized keys, pseudo-localized screenshots at supported aspects, font coverage, focus tests, missing-key report, and exceptions. Do not claim language support until the packaged build displays it correctly.
