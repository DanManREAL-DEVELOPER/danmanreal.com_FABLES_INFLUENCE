# DANMANREAL DESIGN — written canon (blessed 2026-07-08)

Exemplar: `references/exemplar.html` (byte-exact copy of the blessed
`danmanreal.com_DANMANREAL_SHELL/frontend/DMR_BRAND_SYSTEM_WALL.html`, shell commit
`2deadba`). The exemplar outranks this file. Color authority:
`frontend/BRAND_TOKENS.css` — GLB-measured (danmanreal-graffiti.glb + 3 hero frames).

## Tokens (verbatim)

| Token | Value | Role |
|---|---|---|
| --dmr-brand-blue | #197cc1 | brand mid-tone blue |
| --dmr-brand-green | #1fb06f | brand mid-tone green |
| --dmr-paint-blue | #12b7f8 | wet drip facet (leads) |
| --dmr-paint-green | #26f296 | wet drip facet (answers) |
| --dmr-frame-metal | #755934 | aged bronze (bright edge #b18b4e) |
| --dmr-jewel-blue | #0cb6f8 | jewel light (depth #156faa) |
| --dmr-bg-abyss | #030c09 | green-tinted near-black field |
| --dmr-frame-charcoal | #1d2322 | gunmetal frame body |
| --dmr-street-purple / -pink | #8b3df0 / #f04fb0 | artistic accents ONLY |
| ink / ink-soft / ink-dim | #eafcf4 / #cdeede / #a9d8c3 | legibility floor — never lower |
| --dmr-cta-bg | 135° blue→green | CTA pour |
| --dmr-loading-bg | radial #0d2a22→#030c09 | loading glow |

## The frame (every block wears it)

24px padding rim; background = two repeating-linear-gradient bronze vein layers
(112° at rgba(177,139,78,.45), −64° at rgba(117,89,52,.55)) over a 160° gunmetal
gradient (#39443f→#252d2b→#1d2322→#141a18→#2a3230); ::before = 2px bronze bezel inset
14px; ::after = 2px outer bronze line; shadow `--dmr-shadow-frame` + inset bronze
top-light. Four 28px jewel corners at −9px offsets, radial #d9f4ff→#0cb6f8→#156faa→#072c44,
bronze 1px ring, `jewelFade` 5.2s blue↔green glow breathing with staggered delays.
Frame body: #0b1712→#07120c, clamp(2rem,4.5vw,3.6rem) padding.

## The paint (liquid law — swell, neck, tear, gloss)

SVG filter `#goo`: feGaussianBlur stdDeviation 9 → feColorMatrix alpha row
`0 0 0 23 -11` → feComposite atop. `.paintline` (150px tall, frame top, z4) holds a
15px bar + tongues (26px wide, 52px tall, bottom-rounded, `tongue` 7s scaleY .42→1→.88)
+ drops (16px/11px circles, `drop` 7s translateY 0→118px, fade at 96%). Stagger
delays 0–5.2s. Gloss highlight rides OUTSIDE the filter (sharp wet edge). Color
classes: paint-blue / paint-green / paint-street (pink→purple). Never flat banners.

## Type & legibility law

Display: 'Archivo Black','Arial Black',Impact — hero clamp(3.2–7rem), chapters
clamp(2.1–3.4rem), one word per H1/H2 tinted paint-blue or paint-green (or
gradient-clipped). Kickers: Inter 800, .34em tracking, paint-green with paint-blue
Roman numeral. Body: 17px base, 1.72 leading, #cdeede floor — DEEP GREY IS OUTLAWED.
Mono for tokens in paint-blue.

## Structure & motion

Chapter grammar: cover (framed hero + saying "HARD IN THE PAINT" + MS Paint heritage)
→ I ledger (fade swatches) → II paint lab → III frame anatomy → IV voice → V moves
(CTA/loading/framed media) → VI law (ALWAYS/NEVER) → dark epilogue signed
*"Hard in the paint since MS Paint."* Air between chapters: clamp(5.5rem,13vh,9.5rem).
Motion: staged fadeup entrances (IntersectionObserver, ~120ms stagger, start opacity .3),
jewel breathing, drip loops, CTA hover lift. Film grain 5.5% fixed overlay.
`prefers-reduced-motion` kills everything.

## Laws (from the blessed wall)

ALWAYS: GLB-measured color only · frame every block · liquid goo paint · LARGE display
type, mint-bright body · one idea per frame, generous air · blue leads, green answers,
purple/pink accents only.
NEVER: invented hex / old-CSS drift · naked frameless blocks · static banner paint ·
deep grey body text · crammed sections · decoration owning the content.
