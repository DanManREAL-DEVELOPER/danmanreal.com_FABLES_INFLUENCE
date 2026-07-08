# {{NN}} — {{MISSION_NAME}} (EXECUTOR BRIEF)

THIS IS A WARGAME ORDER. Execute exactly what is written. You have no other context and
you need none — if you find yourself needing to ask a question, STOP and report that as
a defect in this brief.

## SCOPE

- You may read, read-only: {{ALLOWED_READ_PATHS}}
- You may write ONLY to: {{ALLOWED_WRITE_PATHS}} (plus `reports/` and the harness ledgers)
- Never touch: {{OWNER_PROTECTED_PATHS}}

## THE MISSION

{{The objective and the route, restated for an executor with zero planner context:
numbered steps with exact paths and commands, each step's expected observation, and the
counter-move to apply if it fails. Self-contained — do not reference the planner spec.}}

## HARD RULES

1. Read-only recon first; no mutating command before its step says so.
2. `{{OWNER:*}}` placeholder in your path = that route is BLOCKED. Record it, skip it,
   continue only on unblocked routes. Never substitute a value, however obvious.
3. OWNER GATE steps require the owner's quoted OK recorded in
   `ledgers/FABLE_OWNER_DECISIONS.md` BEFORE the step runs. No quote, no step.
4. A step that fails its counter-move once more = ABORT the mission and report.
5. Local commits only (exact paths, never blanket adds). Never push, publish, or deploy.

## REPORT HOME (mandatory)

Write `reports/{{NN}}-{{SLUG}}-REPORT.md` as you go: what was done, what was observed,
every deviation, every blocked route, and the VERIFICATION RUNS output verbatim. A
mission without its report is a failed mission regardless of outcome.

## VERIFICATION RUNS

{{Exact commands + expected results, copied from the wargame spec.}}
