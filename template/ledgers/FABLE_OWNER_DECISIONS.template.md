# FABLE OWNER DECISIONS — {{PROJECT_NAME}}

Every decision only the owner may make, in one place. Agents append questions; ONLY the
owner's quoted words close a row. An `{{OWNER:*}}` placeholder anywhere in the harness
must have a row here.

Rules:
- Agents never fill the Decision column — not with defaults, not with "obvious" answers,
  not provisionally. An empty Decision means the affected blocks stay `blocked_on_owner`.
- When the owner decides (in chat), the agent records the decision verbatim (quoted),
  dates it, and updates the affected blocks and status file in the same session.
- Spend, publish, push, delete, and protected-path decisions are ALWAYS owner rows, even
  when the answer seems obvious.

| # | Placeholder / question | Blocks affected | Status | Decision (owner's words, quoted) | Date |
|---|---|---|---|---|---|
| 1 | {{EXAMPLE_OWNER_GATE}} | block-NN | OPEN | | |
