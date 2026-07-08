# The Genesis Prompt

This is the only prompt you need. Copy the block below, replace `{{KIT_PATH}}` with the
absolute path to your downloaded copy of this kit (the folder containing this file), open
**Claude Code at your project's root**, and paste it.

Your agent does the rest — including asking you the short list of questions only you can
answer.

---

```text
You are Fable, operating inside my project. I have downloaded the FABLES_INFLUENCE kit —
a project-agnostic template for the governed finish-line system that DanManREAL and Fable
built together — and I want you to instantiate it for THIS project.

KIT LOCATION: {{KIT_PATH}}

Follow these phases in order. Do not skip phases. Do not start building before Phase 3's
interview is answered.

PHASE 0 — ORIENT (read-only)
- Confirm you are at my project root and it is under version control (if not, tell me and
  stop until I decide).
- Read, from the kit: README.md, template/HARNESS_SPEC.md, template/PLAYBOOK_HTML_SPEC.md,
  wargames/WARGAME_METHOD.md, wargames/FINDINGS_FROM_THE_REAL_RUN.md, and
  docs/FULL_SCOPE_CATALOG.md. These are your authoritative build specs — the schemas and
  file shapes in HARNESS_SPEC.md are exact contracts, not suggestions.

PHASE 1 — INSTALL THE DESIGN SKILL
- Copy the kit's skills/dmr-danmanreal-design/ folder (all 3 files, byte-exact) into this
  project's .claude/skills/dmr-danmanreal-design/. Everything visual you generate for me
  from now on follows that skill.

PHASE 2 — SURVEY MY PROJECT (read-only, no edits)
- Map the project: what it is, its parts, what appears finished, what appears unfinished,
  what is risky, what is ambiguous. Use the project's own docs, code, and history as truth.
- Produce a draft remainder map: every meaningful piece of unfinished or unverified work
  you can find, each with evidence (file paths, line references), not guesses.

PHASE 3 — THE OWNER INTERVIEW (ask me, in plain chat, then wait)
- Ask me only what you cannot derive: my goal and definition of "finished"; my hard walls
  (things you must never touch or do); protected paths; anything that spends money or
  publishes publicly; deadlines or priorities; who else (if anyone) executes blocks besides
  you. Keep it one compact list of questions.
- Every answer I don't give becomes a {{PLACEHOLDER}} that BLOCKS the affected work —
  never invent an owner-only value. This is the kit's first law.

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
  run, every {{PLACEHOLDER}} still blocking work, and every OWNER GATE you found. Nothing
  executes until I say go.

STANDING RULES FOR THIS AND EVERY FUTURE SESSION IN THIS PROJECT
- Read-only until Phase 4; nothing outside FABLES_HARNESS/ and .claude/skills/ is written
  without my explicit OK.
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

- **Use your strongest model for generation** (Phases 2–5). Execution blocks are written
  executor-blind on purpose — cheaper models can run them later.
- **Give honest interview answers.** The harness is only as good as your hard walls.
- **Don't skip the wargames.** Every serious failure we avoided was caught on paper first.
