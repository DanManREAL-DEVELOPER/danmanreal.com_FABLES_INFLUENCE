# SUCCESS.md — definition of done for every wargame ({{PROJECT_NAME}})

A wargame may be marked `DONE` in `LEDGER.md` only when ALL eight hold, point-by-point,
with the grade recorded — **and one honest attempt to break it has failed** (the
red-team pass). These are the same eight points the method was proven with, verbatim in
spirit:

1. **Expected observation per move.** Every move in THE ROUTE states the observation
   that says it worked — not "run X" but "run X and see Y".
2. **Failure + cause + counter-move per move.** Every move carries its most-likely
   failure, why it happens, and the prepared response. No move is "just works".
3. **Explicit fork triggers.** Wherever shared state, concurrency, or a branching
   outcome exists, the fork is written as IF→THEN — a trigger, never a vibe. (A fork
   phrased as a counter-move instead of a trigger is a graded defect; it happened in the
   real run.)
4. **RECON NEEDED with settling checks.** Everything the planner could not verify
   read-only is listed, each item with the exact check that settles it. An empty section
   means "fully verified", and that claim is itself auditable.
5. **Abort conditions.** The spec says when the executor stops the whole mission and
   reports rather than improvising.
6. **Verification runs.** The exact commands (with expected results) that prove the
   OBJECTIVE, run at the end and pasted into the report.
7. **Survived the red-team.** The wargame survived the six attacks in
   WARGAME_METHOD.md, or every landed attack's fix is recorded in the LEDGER and
   re-graded.
8. **Executable blind.** The paired task brief could be run by a mid-tier model with
   zero planner context and zero questions.

## Standing conventions (graded inside the points above)

- **No invented owner values** (point 2/4): every owner-only value is a `{{OWNER:*}}`
  placeholder with NO default; a placeholder blocks its route, never guesses.
- **Explicit owner gates** (point 5): every spend, publish, push, delete, or
  protected-path touch sits behind a named OWNER GATE in both spec and brief.
- **REPORT HOME** (point 6): the report path `reports/NN-<slug>-REPORT.md` is declared
  in every brief — the defect that landed on all 24 first drafts in the real run.

## Owner's standing walls (addendum — resolved at generation)

Graded as part of point 6 for every wargame:

- Protected paths: {{OWNER_PROTECTED_PATHS}}
- Spend & publish policy: {{OWNER_SPEND_PUBLISH_POLICY}}
- Additional hard walls: {{OWNER_HARD_WALLS}}
