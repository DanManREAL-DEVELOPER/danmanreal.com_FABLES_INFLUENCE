# FABLE NEXT AGENT HANDOFF — {{PROJECT_NAME}}

Written for the next session, which knows nothing. Overwritten (not appended) at the end
of every session — this file always describes the CURRENT baton, and history lives in the
evidence index.

## Baton (update every session)

- Last session ended: {{GENERATED_AT}} by {{GENERATED_BY}}
- State: harness freshly generated; no blocks executed yet
- Next block: see `current_state.current_next_block` in `FABLE_EXECUTION_STATUS.json`
  (that file wins over this one if they ever disagree)
- Verifier at last session end: exit 0

## What the next agent must know

1. Read `FABLE_START_HERE.md` and follow its reading order before touching anything.
2. Open items that bit us this run (update as they accumulate):
   - (none yet)
3. Owner gates currently blocking work: see `ledgers/FABLE_OWNER_DECISIONS.md` OPEN rows.

## Do-not list (carry forward every session)

- Do not execute more than one block per prompt.
- Do not touch anything in the owner's protected paths: {{OWNER_PROTECTED_PATHS}}
- Do not push, publish, deploy, spend, or delete without the owner's quoted OK.
