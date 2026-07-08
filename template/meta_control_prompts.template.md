# META-CONTROL PROMPTS — {{PROJECT_NAME}}

The late-game layer. These prompts close the playbook (the last three become its final
blocks) and maintain the five meta-artifacts that turn a finished run into a durable
system. Same laws as every block: durable artifacts after every prompt, hard stops on
owner gates, verifier green before the session ends.

The five meta-artifacts (all live in `FABLES_HARNESS/meta/`):

| File | Job | Status vocabulary |
|---|---|---|
| `FABLE_OPEN_QUESTIONS_AND_RECON.md` | Every open question and follow-up, deduplicated, with what recon would close it | OPEN · PARTIAL · DEFERRED · CLOSED |
| `FABLE_DECISION_REGISTER.md` | Every decision the run produced or needs, each with risk tier and owner | DECIDED · RECOMMENDED · DEFERRED · REJECTED · NEEDS_RECON |
| `FABLE_INTEGRATION_ROADMAP.md` | How the harness's outputs integrate into daily work, phased 0→6 (audit-only → docs/templates → evals → memory → hooks/gates → live) with a yes/no automation call per row | per-phase |
| `FABLE_VALUE_SCORECARD.md` | Honest after-action value: what measurably helped, what was noise, before/after where measurable | measured · TBD_MEASURE |
| `FABLE_ARTIFACT_INDEX.md` | Master index of every durable artifact with state | CREATED · NOT_CREATED · NEEDS_RECON |

---

## META PROMPT A — OPEN QUESTIONS & RECON SWEEP (read-only)

```text
Read-only mission for the {{PROJECT_NAME}} FABLES_HARNESS: sweep every ledger, report,
and wargame for open questions, unverified claims, and deferred follow-ups. Deduplicate
into meta/FABLE_OPEN_QUESTIONS_AND_RECON.md: one row per question — status (OPEN /
PARTIAL / DEFERRED / CLOSED), what exact read-only recon would close it, and whether it
is owner-gated. Invent nothing; every row cites its source file. No writes outside
meta/. Finish with the verifier.
```

## META PROMPT B — DECISION REGISTER (read-only)

```text
Read-only mission: compile meta/FABLE_DECISION_REGISTER.md from the ledgers, the owner
decisions file, and META PROMPT A's output. One row per decision: status (DECIDED /
RECOMMENDED / DEFERRED / REJECTED / NEEDS_RECON), risk tier (HIGH = spend, publish,
delete, protected paths, security; MEDIUM = architecture/governance; LOW = the rest),
affected files/systems, and who decides (owner vs agent). Owner-only decisions must
never appear as DECIDED unless the owner's OK is quoted in FABLE_OWNER_DECISIONS.md.
No writes outside meta/. Verifier before ending.
```

## META PROMPT C — INTEGRATION ROADMAP (read-only)

```text
Read-only mission: write meta/FABLE_INTEGRATION_ROADMAP.md — how this project keeps the
harness's value after the finish line. Phase every candidate 0–6: (0) keep as reference,
(1) audit-only reruns, (2) low-risk docs/templates, (3) evals/tests, (4) memory/indexing,
(5) hooks/gates, (6) live/automated. Per row: a yes/no "safe to automate" call, and
DRAFT_ONLY / must-never-automate marks for anything owner-gated. No writes outside
meta/. Verifier before ending.
```

## META PROMPT D — VALUE SCORECARD (read-only)

```text
Read-only mission: write meta/FABLE_VALUE_SCORECARD.md — the honest after-action review.
Score what the harness measurably improved (blocks completed vs abandoned, audit catches,
owner gates that prevented real mistakes, verifier catches), call out what was vanity or
noise, and mark unmeasurable claims TBD_MEASURE rather than asserting them. Cite the
ledgers for every score. No writes outside meta/. Verifier before ending.
```

## META PROMPT E — ARTIFACT INDEX (read-only)

```text
Read-only mission: write meta/FABLE_ARTIFACT_INDEX.md — the master index of every durable
artifact this harness produced or promised (harness files, ledgers, wargames, reports,
meta files, and every artifact named inside completed blocks). One row each: path, state
(CREATED / NOT_CREATED / NEEDS_RECON), and which block owns it. Check disk for every row
— an artifact listed by a complete block but missing on disk is a finding, not a
footnote. No writes outside meta/. Verifier before ending.
```

---

## CLOSING BLOCK 1 — FINAL AUDIT (read-only; becomes playbook block N-2)

```text
Read-only final audit of the {{PROJECT_NAME}} FABLES_HARNESS. Verify: every block's
status against its on-disk evidence; every ledger internally consistent; every
{{OWNER:*}} placeholder either owner-resolved (quoted) or still honestly blocking; the
five meta-artifacts current; verifier exit 0. Output an audit verdict into
ledgers/FABLE_EVIDENCE_INDEX.md: PASS, or a numbered list of exact discrepancies. Do not
fix anything — auditors report, builders fix.
```

## CLOSING BLOCK 2 — OWNER-GATED COMMIT (becomes playbook block N-1)

```text
OWNER GATE: {{OWNER:APPROVE_FINAL_COMMIT}} — do not proceed without it, quoted.

With the gate quoted: stage EXACT paths only (never a blanket add) for the harness and
the project work it governed, commit locally with a message that names the playbook
blocks covered, and record the commit hash in ledgers/FABLE_EVIDENCE_INDEX.md. Never
push, publish, or deploy — those are the owner's own acts. Verifier before ending.
```

## CLOSING BLOCK 3 — POST-COMMIT WRAP (becomes playbook block N)

```text
Wrap the run: write FABLES_HARNESS/FABLE_FINAL_USE_REPORT.md (what was built, what was
skipped and why, every owner decision, every remaining OPEN row from the meta files),
final entries in all five ledgers, final verifier run (exit 0), and a closing handoff in
FABLE_NEXT_AGENT_HANDOFF.md marked FINAL so any future session knows this run is closed.
```
