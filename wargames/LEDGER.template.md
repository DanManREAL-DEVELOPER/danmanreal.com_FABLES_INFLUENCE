# WARGAME LEDGER — {{PROJECT_NAME}}

Grading truth for the wargame set. A wargame is `DONE` only when all eight SUCCESS.md
points hold point-by-point AND one honest attempt to break it has failed (the red-team
pass), with any landed attacks fixed and re-graded. `{{OWNER:*}}`-gated missions
additionally show `BLOCKED` until the owner decides — blocked is a status, never a
value an agent fills in.

Status vocabulary: `DRAFTED` → `DONE` (may carry `+ BLOCKED` while owner gates are open).

## Grades

| NN | Wargame | Status | Grade | Owner gates | Notes (defects found + fixes) |
|---|---|---|---|---|---|
| 01 | {{slug}} | DRAFTED | –/8 | {{gates or —}} | |

## Red-team record

One entry per attack (see WARGAME_METHOD.md for the six):

| Attack | Scope | Result (LANDED / held) | Defects found | Fixes |
|---|---|---|---|---|
| 1 grep audit | all | | | |
| 2 blind-executor | all briefs | | | |
| 3 per-move audit | top-risk set | | | |
| 4 fork-trigger | concurrent missions | | | |
| 5 invented-values | all | | | |
| 6 protected-path | write-heavy missions | | | |
