# WARGAME QUEUE — {{PROJECT_NAME}}

Execution order for `DONE` wargames. Ranked by **value ÷ risk ÷ owner-dependency**:
high value first, but a mission blocked on an open `{{OWNER:*}}` gate never heads the
queue — the queue must always offer the executor something runnable NOW.

Standing preamble for every mission in this queue:
- The executor brief (`tasks/NN-*.md`) is the contract; the wargame spec is planner
  reference only.
- REPORT HOME first-class: `reports/NN-<slug>-REPORT.md` is written during execution.
- Any brief that forces a question goes back to the planner as a defect.

## Order

| Pos | NN | Mission | Why this position | Runnable now? (open gates) |
|---|---|---|---|---|
| 1 | {{NN}} | {{slug}} | {{one line}} | {{yes / blocked on OWNER:X}} |
