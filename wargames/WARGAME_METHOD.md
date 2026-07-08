# THE WARGAME METHOD — pressure-test the plan before anyone executes it

Audience: the agent generating a FABLES_HARNESS (and any human who wants to know why).

## Origin note

The wargames were not part of the original harness — they were built alongside it, as a
separate discipline, when it became clear that a plan you haven't attacked is a plan you
haven't finished writing. Running the method for real (24 missions over a 30+ project
workspace, every one graded to the eight-point bar and then red-teamed) changed how the
whole system works. It ships in this kit because it turned out to be the critical piece.
The receipts are in [`FINDINGS_FROM_THE_REAL_RUN.md`](FINDINGS_FROM_THE_REAL_RUN.md).

## What a wargame is

A wargame is a mission rehearsed on paper to the point where execution is boring:

- the **objective** is an observable end-state, not an activity;
- the **route** is a numbered sequence of moves, each with its expected observation, its
  most likely failure, that failure's cause, and a prepared **counter-move**;
- everything the plan couldn't verify read-only is confessed in **RECON NEEDED**;
- every value only the owner can supply is a `{{OWNER:*}}` placeholder that **blocks**
  instead of guessing;
- every irreversible act (spend, publish, delete, protected paths) sits behind an
  explicit **OWNER GATE**;
- **abort conditions** say when to stop trying;
- **verification runs** prove the end-state with commands, not adjectives.

Each wargame produces two files plus a report slot:

| File | Audience | Content |
|---|---|---|
| `wargames/NN-<slug>.md` | the planner | full mission spec (template: `wargame.template.md`) |
| `tasks/NN-<slug>.md` | the executor | executor-blind brief (template: `task-brief.template.md`) |
| `reports/NN-<slug>-REPORT.md` | everyone after | REPORT HOME — written during/after execution |

**Executor-blind** is the bar that matters: a mid-tier model must be able to execute the
brief without asking a single question. If the brief needs the planner's context to make
sense, the planning isn't done.

## Which playbook blocks get wargamed

Not all of them. Wargame every block that is: irreversible, owner-gated, spend-adjacent,
touches protected paths, crosses a trust boundary (publishing, credentials, production),
or has a failure mode that costs more than the block saves. Routine build blocks don't
need one — the harness discipline already covers them.

## The grading loop

1. Draft each wargame + brief from the templates → status `DRAFTED`.
2. Self-grade point-by-point against `SUCCESS.md` (instantiate `SUCCESS.template.md`
   first — the eight criteria plus the owner's standing walls as an addendum).
3. Record grades in `LEDGER.md`; order execution in `QUEUE.md`
   (value ÷ risk ÷ owner-dependency — owner-blocked missions never head the queue).
4. **Red-team your own wargames** (below). Fix what lands; regrade; only then `DONE`.

## The six red-team attacks

Run each attack against the drafted set. An attack "lands" when it finds a concrete
defect; fixes are recorded in the LEDGER.

1. **Grep audit** — mechanically scan every wargame for the required sections and the
   eight criteria. Missing section = defect. (Cheap, catches structure rot.)
2. **Blind-executor test** — give a brief to a fresh, cheaper agent with zero context.
   Every question it needs to ask is a defect in the brief.
3. **Per-move audit** — for the highest-risk wargames, walk move by move: does every move
   have expected-observation / failure / cause / counter? Missing rows = defects.
4. **Fork-trigger audit** — for missions with concurrency or shared state: does the spec
   have explicit IF→THEN fork triggers for collisions and races?
5. **Invented-values audit** — hunt for any owner-only value that got a "reasonable
   default" instead of a `{{OWNER:*}}` block. Any invented value is a critical defect.
6. **Protected-path audit** — trace every write in every route against the owner's
   protected paths and gates. Any ungated touch is a critical defect.

## Standing rules during execution

- Read-only recon before any mutating move, every time.
- The brief is the contract: an executor who improvises outside it has failed the
  mission even if the outcome looks right.
- REPORT HOME is mandatory: no mission ends without its report written.
- A `{{OWNER:*}}` placeholder encountered mid-run = stop that route, record it in the
  owner-decisions ledger, continue only on unblocked routes.
