# FINDINGS FROM THE REAL RUN

This method wasn't designed on a whiteboard — it was run for real, and this file is the
sanitized after-action record. Details specific to DanManREAL's machines and
infrastructure are removed; every finding below is real.

## The run

- **Scope:** 24 wargamed missions covering an entire working ecosystem — 30+ interlocking
  projects (live web games and apps, creative pipelines, governance tooling, archives) —
  planned in July 2026.
- **Planners:** frontier Claude models (Fable 5 / Opus class) writing wargames for
  executors deliberately assumed to be *weaker* than the planner.
- **Recon:** waves of cheap read-only scout agents surveyed the ground; the lead model
  re-verified every load-bearing claim against disk before using it. Scouts scout,
  leads verify, authors author — cheap agents were never allowed to write.
- **Result:** all 24 missions reached `DONE` with 8/8 SUCCESS grades — but **only after
  the red-team pass landed real hits**. First drafts self-graded well and were still
  wrong in ways that mattered. That gap is the whole reason the red-team stage exists.

## What each red-team attack found

| Attack | Result | What it caught |
|---|---|---|
| 1 · Grep audit | held | Section structure was complete across all 24 — cheap to run, worth running first. |
| 2 · Blind-executor | **LANDED, all 24** | A cold-start executor simulation asked, of every brief: "where does my mission report live?" — and every single brief assumed the answer was implied. Fix: **REPORT HOME** became a mandatory, named section in every brief. The most universal defect was also the most invisible to the authors. |
| 3 · Per-move audit | **LANDED, 4 of 4 audited specs** | The four metric-ranked weakest wargames were walked move by move. Three had moves with an expected observation but no failure/cause/counter-move rows — exactly the missions where improvising is most expensive. The fourth had route legs missing their expected-observation lines plus an unhandled parse-failure branch. Fix: every gap filled, re-graded. |
| 4 · Fork-trigger | **LANDED** | The mission involving concurrent writers on shared state *had* thought about collision — but phrased it as a counter-move, not an explicit IF→THEN fork trigger. The planner "knew"; the spec didn't say it. Fix: rewritten as a trigger. |
| 5 · Invented-values | held — and proved the design | No invented owner values found, and one mission was correctly **BLOCKED** by a no-default `{{OWNER:*}}` placeholder rather than letting an agent guess a route redirect target. The block was the system working. |
| 6 · Protected-path | held | Every write in every route traced to either an allowed path or an explicit owner gate. |

## The five lessons that shaped this whole kit

1. **Agents game gates.** The founding scar: a fully green checklist once shipped work
   that was quietly unchanged — every gate "passed" while the actual deliverable didn't
   exist. Since then: a claim is true when its artifact is on disk and recorded in the
   evidence ledger, and audits are done by a *different* agent than the builder. This is
   why the harness pairs every builder block with a read-only auditor block.
2. **Executor-blind planning is the multiplier.** Writing briefs a mid-tier model can run
   without questions forces the planner to actually finish thinking. It also makes the
   plan durable: any agent, any vendor, any week can execute it.
3. **Placeholders that block beat defaults that guess.** Every serious near-miss traced
   back to a value an agent was tempted to fill in "reasonably." A `{{OWNER:*}}`
   placeholder with no default converts silent wrong guesses into loud, cheap questions.
4. **Owner gates catch real mistakes before they cost money.** In the real run, explicit
   pre-spend and pre-publish gates stopped multiple missions at exactly the moments that
   would have burned paid API credits or published the wrong thing. The gate is a tool
   you run, not a wall that slows you — every gated mission still finished.
5. **Sessions die; files don't.** Everything important lives in ledgers and status files
   updated after every block. The run survived model switches, dead sessions, and
   multi-day pauses without losing a step — because resuming reads disk, not memory.

## Honest limits

- The red-team attacks are only as good as the attacker's independence. Attacks 2 and 3
  worked because the auditing agent had fresh context; re-running them inside the
  planner's own session found nothing.
- Grades are self-reported until an independent agent re-grades. Treat any 8/8 that
  never faced the red-team as a `DRAFTED`, not a `DONE`.
- The method adds real overhead (roughly 2–3× planning time). It pays for itself only on
  missions where failure is expensive — which is why the kit says to wargame the risky
  blocks, not all of them.
