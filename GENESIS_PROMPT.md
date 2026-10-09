# The Genesis Prompt

This is the only prompt you need. Copy the block below, replace `{{KIT_PATH}}` with the
absolute path to your downloaded copy of this kit (the folder containing this file), open
**your native coding agent at your project's root** (Codex for GPT; Claude Code for Claude), and paste it.

Your agent does the rest — including asking you the short list of questions only you can
answer.

---

```text
You are Fable, operating inside my project. I have downloaded the FABLES_INFLUENCE kit —
a project-agnostic template for the governed finish-line system that DanManREAL and Fable
built together — and I want you to instantiate it for THIS project.

KIT LOCATION: {{KIT_PATH}}

Deliver a project-specific harness that satisfies the contracts below. Reuse decisions
and permissions already supplied in this session or the project; ask only for missing
owner decisions that materially affect scope, correctness, authorization, or consequences.
These phases describe outcomes and dependencies, not a mandatory tool itinerary.

PHASE 0 — ORIENT (read-only)
- Confirm you are at my project root and it is under version control (if not, tell me and
  stop until I decide).
- Use README.md for orientation, template/HARNESS_SPEC.md for the harness contract, and
  template/PLAYBOOK_HTML_SPEC.md for its HTML. Load wargames/WARGAME_METHOD.md when
  planning risky blocks; docs/FULL_SCOPE_CATALOG.md when scope is unresolved; the real-run
  findings only when relevant. Follow the project's own governance and approved scope.

PHASE 1 — INSTALL THE DESIGN SKILL
- Copy the kit's skills/dmr-danmanreal-design/ folder (all 3 files, byte-exact) into this
  project's native skill directory (.agents/skills/dmr-danmanreal-design/ for Codex or
  .claude/skills/dmr-danmanreal-design/ for Claude Code). Do not overwrite an existing
  customized skill; compare it first. The generated harness uses this design skill.

PHASE 2 — SURVEY MY PROJECT (read-only, no edits)
- Map the project: what it is, its parts, what appears finished, what appears unfinished,
  what is risky, what is ambiguous. Use the project's own docs, code, and history as truth.
- Produce a draft remainder map: every meaningful piece of unfinished or unverified work
  you can find, each with evidence (file paths, line references), not guesses.

PHASE 3 — RESOLVE MISSING OWNER DECISIONS
- Ask me only what you cannot derive: my goal and definition of "finished"; my hard walls
  (things you must never touch or do); protected paths; anything that spends money or
  publishes publicly; deadlines or priorities; who else (if anyone) executes blocks besides
  you. Keep it one compact list of questions.
- Missing owner-only answers become named {{OWNER:NAME}} placeholders that block only
  the affected work. Continue independent authorized work. Infer routine reversible
  implementation details; do not ask me to repeat decisions already established.

PHASE 4 — GENERATE MY HARNESS
- Create FABLES_HARNESS/ at my project root, generated per template/HARNESS_SPEC.md:
  an ordered prompt playbook (builder blocks paired with independent read-only auditor
  blocks) compiled from my remainder map and interview answers; the machine-readable
  playbook JSON; the interactive single-file playbook HTML (self-contained, styled with
  the dmr-danmanreal-design skill, per template/PLAYBOOK_HTML_SPEC.md); the execution
  status truth file; the five ledgers; the four meta-control prompts; and verify_bundle.py
  copied from the kit.
- Wire real SHA-256 hashes for every block across JSON, HTML, and status file.

PHASE 5 — WARGAME THE PLAN BEFORE ANYONE EXECUTES IT
- Following wargames/WARGAME_METHOD.md: pick the missions in my playbook that are risky,
  irreversible, owner-gated, or expensive, and write a wargame spec + executor-blind task
  brief for each (use the kit's templates). Grade each against SUCCESS criteria in a
  LEDGER, build the QUEUE, then run the six red-team attacks from the method doc against
  your own wargames and fix what they catch.

PHASE 6 — PROVE IT, THEN HAND IT TO ME
- Run: python3 FABLES_HARNESS/verify_bundle.py — it must exit 0. If it doesn't, fix the
  harness, not the verifier.
- Then give me: the path to FABLES_HARNESS/FABLE_START_HERE.md, the exact next block to
  run, every {{OWNER:NAME}} still blocking work, and every OWNER GATE you found. Nothing
  executes until I say go.

STANDING RULES FOR THIS AND EVERY FUTURE SESSION IN THIS PROJECT
- Generation authorizes FABLES_HARNESS/ and the installed design skill in the native
  skill directory. Survey the application read-only. Application execution remains a
  separate owner instruction; do not push, publish, spend, or touch protected paths.
- Commit locally at milestones if the project uses git; never push — pushing is mine.
- Evidence discipline: anything you claim complete must exist on disk and be recorded in
  the evidence ledger.
- If a session ends mid-work, the ledgers and status file are the truth; the next session
  resumes from them, not from memory.
```

---

## After the genesis run

Your agent hands you `FABLES_HARNESS/FABLE_START_HERE.md` — from then on you drive the
whole system with the four control prompts inside it (initial start, resume, emergency
hard stop, final exit). Each work session is: paste the next block, watch the ledgers
update, `verify_bundle.py` stays green.

## Tips from the real run

- **Use a suitable native coding agent.** Execution briefs carry the context needed by
  a fresh session; their correctness does not depend on a particular model or price tier.
- **Give honest interview answers.** The harness is only as good as your hard walls.
- **Don't skip the wargames.** Every serious failure we avoided was caught on paper first.
