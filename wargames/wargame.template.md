# WARGAME {{NN}} — {{MISSION_NAME}}

Planner: {{GENERATED_BY}} · Drafted: {{GENERATED_AT}} · Status: DRAFTED
Playbook blocks covered: {{BLOCK_IDS}}
REPORT HOME: `reports/{{NN}}-{{SLUG}}-REPORT.md` (mandatory; written during execution)

## OBJECTIVE (observable end-state)

{{One paragraph. A condition verifiable from disk/output alone: what exists, where, and
which command proves it. Not an activity.}}

## SOURCES TO INSPECT (read-only)

{{Exact paths/files/systems the executor may read for this mission, and anything they
must NOT open. Scope is a wall, not a suggestion.}}

## RECON SUMMARY (LOCAL_EVIDENCE, line-cited)

{{What the planner verified read-only while drafting, each claim with file:line or
command output. This is the mission's factual floor — executors trust it over memory.}}

## THE ROUTE

{{Numbered moves. EVERY move uses this exact shape:}}

### M1 — {{move name}}
- DO: {{the action, exact paths and commands}}
- EXPECT: {{the observation that says it worked}}
- LIKELY FAILURE: {{the most probable way this goes wrong}}
- CAUSE: {{why it goes wrong when it does}}
- COUNTER-MOVE: {{the prepared response — not "investigate"}}
- FORK TRIGGER (when shared state/concurrency is involved):
  IF {{condition observed}} THEN {{explicit alternate route}}

### M2 — …

## RECON NEEDED (could not verify read-only)

{{One row per unknown: what is unknown → the exact recon that closes it → which moves it
gates. Empty section = "fully verified", which is itself an auditable claim.}}

## OWNER GATES

{{Every spend / publish / push / delete / protected-path decision, one per line:}}
- `{{OWNER:GATE_NAME}}` — {{what it authorizes, in one sentence}} — blocks: {{moves}}

## ABORT CONDITIONS

{{Conditions under which the executor stops the whole mission and reports, rather than
improvising. Include the "two failed counter-moves on one move" rule.}}

## VERIFICATION RUNS

{{The exact commands (and expected outputs/exit codes) that prove the OBJECTIVE. These
run at the end of execution and their output goes in the report.}}
