# START HERE — the human tour

You're holding the FABLES_INFLUENCE kit. This page explains what it does in human terms.
(The machine-facing specs live in `template/` and `wargames/` — your agent reads those.)

## The problem this solves

AI coding agents are brilliant inside one session and amnesiac between them. Big projects
die in the gaps: half-finished work nobody can resume, "done" claims nothing verifies,
plans that drift every time a new session re-reads them, and agents happily inventing the
answers only you should give.

This kit is the countermeasure. It was built by running it for real — on a workspace of
30+ interlocking projects — and keeping only what survived contact.

## What your agent generates for you: `FABLES_HARNESS/`

| Generated file | Job |
|---|---|
| `FABLE_START_HERE.md` | Your cockpit. The four control prompts (start / resume / hard stop / final exit) and the reading order for everything else. |
| `FABLE_PROMPT_PLAYBOOK.html` | The interactive playbook — every prompt block, in order, with copy buttons and sent-tracking. Self-contained single file, styled with the DanManREAL DESIGN skill. Open it in any browser. |
| `FABLE_PROMPT_PLAYBOOK.json` | The machine-readable twin. Every block SHA-256 anchored. |
| `FABLE_EXECUTION_STATUS.json` | The single source of truth: per-block status, the exact next block, everything blocked on you. |
| `ledgers/` (five files) | Durable memory: evidence index, owner decisions, next-agent handoff, pre-block sanity check, re-entry note. |
| `meta_control_prompts.md` | The late-game prompts: read-only final audit, owner-gated commit, post-commit wrap, plus the five meta-artifacts (open questions, decision register, integration roadmap, value scorecard, artifact index). |
| `verify_bundle.py` | The integrity gate. Exit 0 = the playbook HTML, JSON, and status file all agree and nothing has drifted. Run it any time; trust it over anyone's summary — including your agent's. |
| `wargames/` | Mission specs + executor-blind briefs for your risky work, graded in a ledger, red-teamed before execution. |

## The working rhythm

```
you                      your agent(s)                      the files
───                      ─────────────                      ─────────
paste GENESIS_PROMPT  →  survey, interview you,
                         generate FABLES_HARNESS         →  verify_bundle.py exit 0
open playbook HTML    →
copy next block       →  execute ONE block               →  ledgers + status updated
                         (builder blocks build;
                          auditor blocks audit,
                          read-only, second agent)
verify + repeat       →  ...                             →  exit 0, next block advances
hit an OWNER GATE     →  agent stops and asks you        →  your decision recorded
```

One block at a time. Ledgers after every block. The status file always knows what's next.
Any fresh session resumes with the RESUME control prompt — no context lost.

## The two roles

- **Builder (Fable)** — your main Claude Code session. Builds, edits, commits locally.
- **Auditor** — a *different* agent (fresh Claude session, Codex CLI, anything capable),
  deliberately kept read-only. Every builder block has a paired auditor block that checks
  the work against the evidence. This pairing caught real problems in the original run
  that a single agent graded itself green on. Don't skip it.

## The wargames (why they're in here)

The wargames weren't part of the original harness — they were built *around* it, and they
turned out to be critical, which is why they ship in this kit. Before any risky mission
executes, it gets: an executor-blind brief (a mid-tier model could run it without asking
a single question), a counter-move for every predicted failure, explicit `{{PLACEHOLDER}}`
blocks for every owner-only value, and a six-attack red-team pass. Read
`wargames/FINDINGS_FROM_THE_REAL_RUN.md` for what this caught in practice — including the
finding that matters most: **agents game gates.** Every "done" must be disk-verified.

## FAQ

**Does this need Fable 5 specifically?** It's tuned for Claude Code with Fable 5 and that's
the tested path; any strong Claude model can run the genesis prompt. Executor-blind blocks
are deliberately runnable by weaker models afterward.

**Does it work on non-code projects?** Yes — the harness is about work, evidence, and
decisions, not languages. The survey phase adapts to whatever the project is.

**What if I don't have a second agent for audits?** Use a fresh Claude Code session with
the auditor block — the point is fresh context and read-only discipline, not a different
vendor.

**Is anything here specific to DanManREAL's machines?** No. The kit is fully
project-agnostic; every project-specific value in the original was replaced by a
`{{PLACEHOLDER}}` your agent fills from *your* project and *your* answers. The one
DanManREAL-specific gift is intentional: the design skill.

## Now go

Open [`GENESIS_PROMPT.md`](GENESIS_PROMPT.md) and paste the block. That's the whole
instruction.
