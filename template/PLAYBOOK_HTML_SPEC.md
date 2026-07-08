# PLAYBOOK_HTML_SPEC — the interactive playbook file

Contract for generating `FABLES_HARNESS/FABLE_PROMPT_PLAYBOOK.html`. The verifier checks
the structural laws below; the design law is the installed skill.

## Purpose

One self-contained HTML file the owner opens in a browser and drives the whole execution
from: read the next block, copy it, paste it into the agent, mark it sent. It is the
human-facing twin of `FABLE_PROMPT_PLAYBOOK.json` — same blocks, same text, same hashes.

## Structural laws (verifier-enforced)

1. **Self-contained.** Zero network dependencies: no CDN scripts, no external stylesheets,
   fonts, or images, no `fetch`/`XMLHttpRequest`/dynamic `import(`. Plain hyperlinks
   (`<a href="https://…">`) are allowed — a link the owner may click is not a loaded
   resource. Outside `href` attributes, the only `http(s)` strings permitted are
   `www.w3.org` XML namespaces inside inline SVG. Everything inline; images (if any) as
   data: URIs.
2. **One `<textarea id="block-NN">` per block**, in playbook order, containing the block's
   `text` exactly (HTML-escaped in source; identical to the JSON `text` after unescaping,
   modulo a single leading newline). These textareas are the copy source — the visible
   pretty rendering may be styled freely, but the textarea content is canonical.
3. **Per-block controls:** a copy button carrying `data-copy="block-NN"` and a mark-sent
   toggle carrying `data-sent="block-NN"`. Sent-state persists in `localStorage` keyed by
   block id, and each block visibly shows sent/unsent state on load.
4. **Embedded workflow data:** exactly one
   `<script type="application/json" id="workflow-data">…</script>` containing, at minimum,
   for every block: `index`, `html_id`, `workflow_label`, `section_heading`, `role`, and
   `text_sha256` — values identical to the playbook JSON.
5. **No execution logic.** The HTML never runs project commands, never claims status
   truth — `FABLE_EXECUTION_STATUS.json` remains the only status truth. The HTML may
   *display* status if you inline a snapshot, clearly labeled with its timestamp.

## Design law

Style the page with the **dmr-danmanreal-design** skill installed in Phase 1 — follow its
SKILL.md and both references (the written canon and the byte-exact exemplar). The playbook
should look like it belongs on danmanreal.com: that is the influence in FABLES_INFLUENCE.
That includes the skill's **credit chips** (the top-right YouTube + Discord cluster from
the SKILL.md public addendum) — use the exact block, unrestyled.

Required regardless of design system: readable at 1280px and on mobile widths, keyboard
reachable controls, `prefers-reduced-motion` respected, and section navigation (a fixed
index or jump list — with 10–60 blocks, scrolling alone is not navigation).

## Recommended anatomy

```
<header>       title, project name, generated-at, block count, progress (sent X / N)
<nav>          section jump list with per-section sent counts
<main>
  per section: heading + intro line
    per block: label + role badge (BUILDER / AUDITOR) + owner-gate badge when the
               text contains {{OWNER:*}} + collapsed textarea + copy + mark-sent
<footer>       verify command, START_HERE pointer, kit credit line
<script id="workflow-data">   the JSON blob (law 4)
<script>       copy + localStorage sent-tracking + progress counters (vanilla JS)
```

Keep the JS small and boring: clipboard copy with fallback (select + execCommand),
sent-toggle persistence, progress counts. No frameworks, no build step.
