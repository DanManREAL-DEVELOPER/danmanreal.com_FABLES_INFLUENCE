# FABLE REENTRY NOTE — {{PROJECT_NAME}}

The crash-recovery note. Updated at the START of every block (one line: what is about to
happen) and at the END (what actually happened). If a session dies mid-block, this file
is the difference between clean recovery and archaeology.

Format — append, newest at the bottom:

```
[UTC timestamp] [actor] STARTING block-NN: <one line of intent>
[UTC timestamp] [actor] ENDED block-NN: <done / partial: exactly what remains / aborted: why>
```

A STARTING line without a matching ENDED line = the previous session died mid-block.
The recovering session must reconcile that block's real state (disk evidence vs claims)
before running anything, and record the reconciliation here.

---

[{{GENERATED_AT}}] [{{GENERATED_BY}}] ENDED generation: harness created, verifier exit 0,
no blocks executed.
