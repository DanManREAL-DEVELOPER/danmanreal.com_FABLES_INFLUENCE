# FABLE PRE-BLOCK SANITY CHECK — {{PROJECT_NAME}}

Run this checklist BEFORE executing any block. Thirty seconds here has repeatedly saved
whole sessions. If any check fails, fix the state first — never execute a block against a
lying harness.

## The checklist

1. **Verifier green?** `python3 FABLES_HARNESS/verify_bundle.py` → exit 0. Exit 2 = HALT,
   report, repair before anything else.
2. **Right block?** The block you're about to run matches
   `current_state.current_next_block` (both `html_id` and `text_sha256`). If you're being
   asked to run a different block, stop and ask the owner.
3. **Tree honest?** `git status --short` (if the project uses git) shows nothing
   unexplained. Unexplained changes → reconcile and record before executing.
4. **Not blocked?** The block's text contains no unresolved `{{OWNER:*}}` placeholder and
   no OWNER GATE without a quoted decision in `ledgers/FABLE_OWNER_DECISIONS.md`.
5. **Crash residue?** No block sits `in_progress` from a dead session. If one does:
   reconcile its evidence first (RESUME prompt, step 2).
6. **Right actor?** BUILDER blocks run in the main build session; AUDITOR blocks run in a
   fresh, read-only, separate session. An auditor with write access or a builder auditing
   itself both void the audit.
