# FABLE START HERE — {{PROJECT_NAME}}

Generated {{GENERATED_AT}} by {{GENERATED_BY}} from the FABLES_INFLUENCE kit.
Harness root: `{{PROJECT_ROOT}}/FABLES_HARNESS`

This file is the owner's cockpit. You drive everything with the four control prompts
below; agents drive everything from the files this folder contains.

## Reading order (for any fresh agent)

1. This file — do not re-open the kit; the harness is self-sufficient.
2. `FABLE_EXECUTION_STATUS.json` — the only status truth; it names the next block.
3. `ledgers/FABLE_REENTRY_NOTE.md` — what the last session was doing.
4. `ledgers/FABLE_NEXT_AGENT_HANDOFF.md` — what the last session left for you.
5. `FABLE_PROMPT_PLAYBOOK.json` — the blocks (the HTML is the human view of the same).

## The loop

Open `FABLE_PROMPT_PLAYBOOK.html` → find the next block (matches
`current_state.current_next_block`) → copy → paste into the right agent (BUILDER blocks
into your main Claude Code session; AUDITOR blocks into a fresh, read-only second agent)
→ the agent works, updates the ledgers and status file, runs the verifier → mark the
block sent in the HTML → repeat. One block at a time, always.

---

## CONTROL PROMPT 1 — INITIAL START (first execution session)

```text
You are executing the FABLES_HARNESS for {{PROJECT_NAME}}. Work from the project root.

1. Read FABLES_HARNESS/FABLE_START_HERE.md and follow its reading order.
2. Run: python3 FABLES_HARNESS/verify_bundle.py — if it does not exit 0, STOP and report;
   do not execute any block against a broken harness.
3. Execute exactly the block named by current_state.current_next_block in
   FABLE_EXECUTION_STATUS.json — that one block, nothing more.
4. Honor every hard-stop category in the playbook's execution_control_contract. An
   unresolved {{OWNER:*}} placeholder or an OWNER GATE means stop that block, record it,
   and tell me.
5. Before ending: update FABLE_EXECUTION_STATUS.json and all ledgers, re-run the verifier
   (must exit 0), and tell me the next block.
```

## CONTROL PROMPT 2 — RESUME (every later session)

```text
Resume the FABLES_HARNESS for {{PROJECT_NAME}} from durable state, not from memory.

1. Read, in order: FABLES_HARNESS/FABLE_EXECUTION_STATUS.json,
   ledgers/FABLE_REENTRY_NOTE.md, ledgers/FABLE_NEXT_AGENT_HANDOFF.md.
2. Run the verifier. If a block is in_progress, first reconcile: check its claimed
   evidence against disk, finish or honestly demote it, update the ledgers.
3. Then proceed exactly as in the INITIAL START prompt from step 3.
```

## CONTROL PROMPT 3 — EMERGENCY HARD STOP

```text
HARD STOP the FABLES_HARNESS work for {{PROJECT_NAME}} right now.

Do not start anything new. Bring the files to a truthful state and freeze: set the
current block to in_progress or blocked_on_owner (whichever is true), write exactly what
was and wasn't done to ledgers/FABLE_REENTRY_NOTE.md and FABLE_NEXT_AGENT_HANDOFF.md,
update FABLE_EXECUTION_STATUS.json, run the verifier, report state, and end the session.
```

## CONTROL PROMPT 4 — FINAL EXIT (project finish line)

```text
Close out the FABLES_HARNESS for {{PROJECT_NAME}}.

1. Run the verifier; reconcile until exit 0 with every block complete, complete_static,
   or owner-approved skipped_superseded.
2. Execute the closing meta blocks from meta_control_prompts.md that I approve: the
   read-only final audit, then (only on my explicit OK) the commit block, then the wrap.
3. Write the final entries in every ledger, produce FABLE_FINAL_USE_REPORT.md in
   FABLES_HARNESS/ summarizing what was built, what was skipped and why, and every
   decision I made. Nothing pushes, publishes, or deploys — those remain mine.
```

---

## Standing walls (owner's answers, resolved at generation)

- Definition of finished: {{OWNER_DEFINITION_OF_DONE}}
- Protected paths / never-touch: {{OWNER_PROTECTED_PATHS}}
- Spend & publish policy: {{OWNER_SPEND_PUBLISH_POLICY}}
- Executors: {{OWNER_EXECUTORS}}

*From the FABLES_INFLUENCE kit — built by Fable, with Fable, for us all.*
