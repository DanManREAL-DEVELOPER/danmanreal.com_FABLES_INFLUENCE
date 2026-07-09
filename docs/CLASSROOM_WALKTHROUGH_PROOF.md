# FABLES_INFLUENCE Classroom Walkthrough Proof

This is the current proof packet for `FABLES_INFLUENCE_CLASSROOM_WALKTHROUGH.html`.

Dan's approval is still required before this work is considered done. This report proves the current state; it does not close the goal.

## Artifact Under Test

- HTML: `FABLES_INFLUENCE_CLASSROOM_WALKTHROUGH.html`
- Verifier: `scripts/verify_classroom_walkthrough.mjs`
- Durable proof folder: `docs/classroom_walkthrough_proof/`

## What Was Proven

The verifier proves:

- The HTML exists, is substantial, ASCII, and has no TODO/FIXME markers.
- The module script parses successfully with `node --check`.
- All nine major sections exist: home, map, steps, files, generated, uses, teacher, glossary, questions.
- Kid-facing teaching copy exists, including `10-year-old answer`, `Say it to a kid`, `Teacher bridge`, `30-second demo`, and `Common mix-up`.
- DanManREAL DESIGN tokens and primitives exist: abyss, paint blue/green, bronze/gunmetal frame, jewel colors, goo filter, paint rails, and jewel corners.
- Three.js WebGPU wiring exists: `three/webgpu`, `WebGPURenderer`, and `navigator.gpu`.
- Runtime counts match the intended classroom scope:
  - 12 end-to-end stages
  - 12 file cards
  - 8 generated-harness cards
  - 18 use-case cards
  - 7 lesson cards
  - 9 glossary word-lab cards
  - 11 topic buttons
  - 500 generated student questions
- Every stage card, file card, generated card, and use-case card produces an answer.
- The glossary word lab updates for `Verifier`, including kid answer, demo, source pills, and 3 class-check prompts.
- The question engine search/click path works for `wargame`.
- All nine page-section screenshots were captured.
- Real Windows Chrome through rtx-eyes proves the WebGPU canvas renders with real GPU pixels.

## Commands And Outputs

```bash
node scripts/verify_classroom_walkthrough.mjs > /tmp/fables_verify_5.json 2>/tmp/fables_verify_5.err
```

Observed output:

```text
rc=0
passed=52
proofDir=/tmp/fables-classroom-proof
```

Saved durable proof:

```text
docs/classroom_walkthrough_proof/verification-results.json
docs/classroom_walkthrough_proof/section-contact-sheet.png
docs/classroom_walkthrough_proof/real-gpu-webgpu-map.png
docs/classroom_walkthrough_proof/real-gpu-webgpu-state.json
```

Real-GPU proof summary:

```text
gpu_backend=webgpu
gpu_renderer=Three.js WebGPU running
gpu_canvas=[{"w":816,"h":636,"clientW":816,"clientH":636}]
gpu_events=0
```

Image-stat proof:

```text
section-contact-sheet.png: 1140x960, nonblank, high color variety
real-gpu-webgpu-map.png: 1440x1100, nonblank, WebGPU node map visible
```

Serve proof:

```bash
curl -s -o /dev/null -w 'serve=%{http_code} bytes=%{size_download}\n' \
  http://127.0.0.1:4458/FABLES_INFLUENCE_CLASSROOM_WALKTHROUGH.html
```

Observed output:

```text
serve=200 bytes=92319
```

## Visual Evidence

- Full section contact sheet: `docs/classroom_walkthrough_proof/section-contact-sheet.png`
- Real-GPU WebGPU map: `docs/classroom_walkthrough_proof/real-gpu-webgpu-map.png`

The contact sheet covers the full page flow:

1. Home hero
2. WebGPU system map
3. Start-to-finish stages
4. File backpack
5. Generated FABLES_HARNESS
6. Use cases
7. Teacher board
8. Glossary word lab
9. Question engine

The real-GPU screenshot is separate because headless Chrome can render the DOM while failing to composite a true WebGPU canvas. The rtx-eyes proof uses Windows Chrome with the real GPU.

## Current Limits

- This is not marked final until Dan approves.
- The local server is currently expected at `http://127.0.0.1:4458/FABLES_INFLUENCE_CLASSROOM_WALKTHROUGH.html`.
- The raw per-section screenshots from the verifier are in `/tmp/fables-classroom-proof/`; the durable repo copy keeps the contact sheet plus real-GPU evidence.
