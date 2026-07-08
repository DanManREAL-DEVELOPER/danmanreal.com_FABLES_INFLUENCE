# FULL SCOPE CATALOG — the maximization artifact tree

When the original system ran at full scope, it didn't just finish the remaining work —
it left behind a durable artifact tree that made every future agent session smarter.
This catalog is that tree, genericized. During Phase 4, offer the owner these sections;
each accepted section becomes playbook blocks (builder + auditor pairs, like everything
else).

Generated artifacts live under `FABLES_HARNESS/` in the folders shown. Every artifact is
a durable file with an owner, a purpose, and a state tracked in
`meta/FABLE_ARTIFACT_INDEX.md`.

## docs/ — the project understood

| Artifact | What it is |
|---|---|
| `FABLE_REMAINDER_MAP.md` | Every meaningful piece of unfinished/unverified work, evidence-cited. The playbook compiles from this. |
| `FABLE_ARCHITECTURE_AUDIT.md` | The system as it actually is: parts, boundaries, seams, load-bearing pieces. |
| `FABLE_DEPENDENCY_MAP.md` | What depends on what — internal and external — with the risky edges flagged. |
| `FABLE_DEAD_CODE_AND_DRIFT_AUDIT.md` | What exists but no longer serves: dead paths, stale docs, drift between docs and reality. |
| `FABLE_SECURITY_AND_SECRETS_BOUNDARY_AUDIT.md` | Where secrets live, where they must never appear, and what enforces that boundary. Read-only findings; fixes are owner-gated blocks. |
| `FABLE_EXECUTOR_ONBOARDING.md` | The one page a brand-new agent reads to work in this project safely. |

## memory/ — lessons that survive sessions

| Artifact | What it is |
|---|---|
| `FABLE_LESSONS_SCHEMA.md` | The shape of a recorded lesson (what happened, why, how to apply). |
| `FABLE_LESSONS_SEED.jsonl` | The starting lesson set, harvested from this run's ledgers. |
| `FABLE_MEMORY_INDEXING_PLAN.md` | How lessons get found again (naming, linking, recall). |
| `FABLE_SESSION_HANDOFF_TEMPLATE.md` | The reusable end-of-session handoff shape. |

## evals/ — proof the project stays working

| Artifact | What it is |
|---|---|
| `FABLE_EVAL_STRATEGY.md` | What "verified" means for this project and what gets checked when. |
| `FABLE_GOLDEN_FIXTURES.md` | Known-good inputs/outputs worth protecting. |
| `FABLE_AGENT_FAILURE_CASES.md` | The ways agents have failed in this project, as regression material. |
| `FABLE_VERIFICATION_COMMANDS.md` | The exact commands that prove each subsystem works. |
| `FABLE_MINIMAL_TEST_PLAN.md` | The smallest test suite worth having, and where it starts. |

## agent-docs/ — how agents behave here

| Artifact | What it is |
|---|---|
| `FABLE_AGENTS_DRAFT.md` | Draft agent-facing project instructions (AGENTS.md-style), owner-reviewed before adoption. |
| `FABLE_CLAUDE_DRAFT.md` | Draft CLAUDE.md-style instructions for Claude Code specifically. |
| `FABLE_SECOND_AGENT_CONFIG_NOTES.md` | Setup notes for the auditor/second agent. |
| `FABLE_AGENT_RULES_CHANGELOG.md` | Every change to agent rules, dated and reasoned. |

## specs/ — how future work gets defined

| Artifact | What it is |
|---|---|
| `FABLE_SPEC_CONSTITUTION.md` | The standing rules every future spec must honor. |
| `FABLE_PRD_TEMPLATE.md` / `FABLE_PLAN_TEMPLATE.md` / `FABLE_TASKS_TEMPLATE.md` | The product → plan → tasks pipeline, sized for this project. |
| `FABLE_EXECUTOR_ACCEPTANCE_TEMPLATE.md` | What an executor must show for work to be accepted. |

## skills/ — reusable agent capabilities

| Artifact | What it is |
|---|---|
| `fable-debugging/reference.md` | This project's debugging playbook as a loadable skill reference. |
| `fable-governance/reference.md` | The harness discipline as a skill any session can load. |
| `fable-reporting/reference.md` | Report shapes: evidence rows, mission reports, handoffs. |
| `fable-executor-wargame/reference.md` | The wargame method as an executor-loadable skill. |

## governance/ — making the discipline enforceable

| Artifact | What it is |
|---|---|
| `FABLE_GOVERNANCE_REDTEAM.md` | Red-team results against the project's own rules: where an agent could bypass them. |
| `FABLE_GATE_RULE_CANDIDATES.md` | Rules worth promoting from prose to enforced gates. |
| `FABLE_HOOK_CANDIDATES.md` | Candidate automation hooks (draft-only; wiring is owner-gated). |
| `FABLE_BYPASS_TESTS.md` | Tests that prove the gates actually block what they claim to block. |

## ops/ — run-state hygiene

| Artifact | What it is |
|---|---|
| `FABLE_LOG_PRESERVATION_CHECKLIST.md` | What run evidence to keep, where, and for how long. |

## meta/ — the five meta-artifacts

Defined in `template/meta_control_prompts.template.md`: open questions & recon, decision
register, integration roadmap, value scorecard, artifact index.

---

**Scaling note:** a small project doesn't need all of this. The genesis interview asks
the owner which sections they want; "docs/ + evals/ + meta/" is the sensible minimum,
and the rest earns its place as the project grows.
