# FABLE EVIDENCE INDEX — {{PROJECT_NAME}}

The proof ledger. A claim without a row here did not happen. Append-only; newest at the
bottom; never rewrite an existing row (corrections get a new row referencing the old).

Rules:
- One row per completed block (and per audit verdict). Evidence = paths that exist on
  disk at write time, plus the command output or measurement that proves the end-state.
- Confidence is honest: HIGH (disk-verified this session), MEDIUM (verified indirectly),
  LOW (claimed but not independently verified — a LOW row is a to-audit flag, not a pass).
- Auditor blocks write their verdicts here: `AUDIT block-NN: PASS` or the numbered
  discrepancies.

| When (UTC) | Block | Actor | Evidence (paths + proof) | Confidence |
|---|---|---|---|---|
| {{GENERATED_AT}} | — | {{GENERATED_BY}} | Harness generated; verify_bundle.py exit 0 | HIGH |
