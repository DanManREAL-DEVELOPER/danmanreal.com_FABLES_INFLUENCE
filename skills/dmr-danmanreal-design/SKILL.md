---
name: dmr-danmanreal-design
description: DanManREAL DESIGN — Dan-canonized brand design system (2026-07-08, blessed "nailed it, ONE TRY" from the brand wall exemplar). Use when Dan says "Use DanManREAL DESIGN", "DMR DESIGN", "my brand style", or asks for any danmanreal.com-branded page, YouTube-shareable brand page, or hard-in-the-paint look. Wet liquid paint drips (goo filter) on bronze-veined gunmetal frames with jewel corners over a green-tinted abyss — NOT FABLES DESIGN (parchment) and NOT Clean Curator (ivory/teal). Exemplar = truth.
---

# DANMANREAL DESIGN (Hard in the Paint)

Dan's blessing, 2026-07-08, on `DMR_BRAND_SYSTEM_WALL.html`: *"nailed it!! ONE TRY —
exactly what I had in my EYE!"* This skill IS that save. Do not freestyle a "close
enough" version — the canon is written and the exemplar is byte-exact.

## The one rule

Before styling anything in DanManREAL DESIGN, open BOTH:

1. `references/DANMANREAL_DESIGN.md` — the written canon (tokens, frame, paint physics, type, laws)
2. `references/exemplar.html` — the byte-exact blessed brand wall. When in doubt about ANY
   value, copy from the exemplar verbatim. It outranks memory and it outranks this file.

## Identity in one paragraph

A gallery wall in a green-tinted abyss (`#030c09`): every block hangs in a chunky
bronze-veined gunmetal frame (`#1d2322` + `#755934→#b18b4e` veins) with four breathing
jewel corners (`#0cb6f8→#156faa` — the fade is sacred); wet street paint runs off every
frame's top rail as LIVING liquid (SVG goo filter: gaussian blur + alpha-contrast; tongues
swell, neck, and tear droplets free), blue (`#12b7f8→#197cc1`) leading, green
(`#26f296→#1fb06f`) answering, purple/pink (`#8b3df0`/`#f04fb0`) only as street accents;
display type is huge (Archivo/Arial Black), body text never drops below mint
(`#cdeede`) — deep grey on the abyss is outlawed; chapters get FABLES-style structure,
Roman-numeral kickers, and generous air. Film grain at ~5%. The saying: **"HARD IN THE
PAINT"** — heritage: every early asset was drawn in Microsoft Paint, and the paint never dried.

## Build contract (non-negotiable)

- ONE self-contained file: inline CSS/JS, zero CDNs, zero network, zero external assets.
- Copy the `:root` token block from the exemplar VERBATIM — colors are GLB-measured
  (source: `danmanreal.com_DANMANREAL_SHELL/frontend/BRAND_TOKENS.css`); never invent hex.
- Every block wears the frame: 24px bronze-veined gunmetal rim, bezel line, 28px jewel
  corners, paint off the top rail. No naked blocks, no naked media.
- Paint is goo-filtered liquid caught mid-drip (copy the exemplar's `#goo` filter +
  tongue/drop keyframes) with a sharp gloss OUTSIDE the filter. Never flat static banners.
- Keep the chapter grammar (cover → ledger → feature labs → anatomy → voice → moves →
  law → epilogue); drop chapters that don't apply, never reorder the ones kept.
- Include the `prefers-reduced-motion` block from the exemplar.
- Verify before handoff: `node Product_Design_Showcase_Template/scripts/check_html_fit.mjs
  <file>` must pass, and view a screenshot with your own (canary-proven) eyes.

## What it is NOT

- Not FABLES DESIGN (parchment war-room atlas) — that is `dmr-fables-design`.
- Not Clean Curator (ivory/teal/mascot) — that is `dmr-clean-curator-brand`.
- Not a neon cyber theme — the field is a deep green abyss and the metal is aged bronze,
  not chrome; paint is wet street color, not glow-tubes.
