# HARNESS_SPEC — the authoritative contract

Audience: the agent (Fable) instantiating this kit for an owner's project.
Status: **generation contract**. Build to the shapes below, byte for byte where stated.
`verify_bundle.py` checks bounded structural integrity: required files, supported schema
version, project identity, block fields/order/hashes, HTML twins and controls, status
metadata, next-block and owner-gate consistency. It does not implement a complete JSON
Schema validator, execute prompts, establish evidence adequacy, or certify a project
finished. Review those semantic requirements separately. If a generated harness fails,
fix that harness; do not weaken its copied verifier to hide the defect.

## Output layout (generated at the owner's project root)

```
FABLES_HARNESS/
├── FABLE_START_HERE.md              ← from template/FABLE_START_HERE.template.md
├── FABLE_PROMPT_PLAYBOOK.json       ← schema below
├── FABLE_PROMPT_PLAYBOOK.html       ← per template/PLAYBOOK_HTML_SPEC.md
├── FABLE_EXECUTION_STATUS.json      ← from template/EXECUTION_STATUS.template.json
├── meta_control_prompts.md          ← from template/meta_control_prompts.template.md
├── verify_bundle.py                 ← COPIED from the kit, unmodified
├── ledgers/
│   ├── FABLE_EVIDENCE_INDEX.md
│   ├── FABLE_OWNER_DECISIONS.md
│   ├── FABLE_NEXT_AGENT_HANDOFF.md
│   ├── FABLE_PRE_BLOCK_SANITY_CHECK.md
│   └── FABLE_REENTRY_NOTE.md        ← all five from template/ledgers/
├── wargames/                        ← per wargames/WARGAME_METHOD.md
│   ├── SUCCESS.md
│   ├── LEDGER.md
│   ├── QUEUE.md
│   ├── wargames/NN-<slug>.md        ← full mission specs
│   ├── tasks/NN-<slug>.md           ← executor-blind briefs
│   └── reports/                     ← REPORT HOME (empty dir + .gitkeep at generation)
└── evidence/                        ← artifact drop zone referenced by the evidence index
```

Templates use `{{DOUBLE_BRACE}}` placeholders. Two kinds — do not confuse them:

- **Generation placeholders** (`{{PROJECT_NAME}}`, `{{PROJECT_ROOT}}`, `{{OWNER_NAME}}`,
  `{{GENERATED_AT}}`, `{{NEXT_BLOCK}}`…): you MUST resolve these while generating. None may
  survive into the generated harness — the verifier greps for them.
- **Owner-gate placeholders** (`{{OWNER:*}}`, e.g. `{{OWNER:PUBLIC_PUSH_GO}}`,
  `{{OWNER:SPEND_LIMIT}}`): resolve these only from an actual owner decision,
  recorded with provenance in the decision ledger; never invent the value. Until then,
  affected active blocks carry status `blocked_on_owner`. An owner-approved superseded
  block requires its skip evidence and is not an active gate.

## Compiling the playbook

Source material: your Phase 2 remainder map + the owner's Phase 3 interview answers +
`docs/FULL_SCOPE_CATALOG.md` (offer the owner the full-maximization scope; include the
catalog sections the owner accepts).

Rules:

1. **Blocks are ordered, atomic, and executor-blind.** One block = one session-sized
   mission with observable end-state, relevant paths, verification evidence, and scope
   boundaries sufficient for a fresh session. Ask only when missing information
   materially changes the work. Owner-only unknowns become named gate placeholders.
2. **Builder/auditor pairing.** Every builder block (`role: "fable_builder"`) is followed
   by a read-only auditor block (`role: "auditor"`) that verifies the builder's claimed
   evidence against disk, into the evidence ledger. Auditor blocks must forbid writes
   except to `FABLES_HARNESS/ledgers/` and `FABLES_HARNESS/wargames/reports/`.
3. **Every block text embeds the discipline footer**: update `FABLE_EXECUTION_STATUS.json`,
   append to the ledgers, halt on owner gates, and re-run `verify_bundle.py` before ending
   the session.
4. **Late-game blocks come from `meta_control_prompts.md`**: a read-only final audit block,
   an owner-gated commit block, and a post-commit wrap block close the playbook.
5. Size guidance: 10–60 blocks. Below 10, fold; above 60, split the project.

## FABLE_PROMPT_PLAYBOOK.json — exact schema

```json
{
  "schema_version": "fables-influence-1.0",
  "workflow_title": "<project name> — FABLE PROMPT PLAYBOOK",
  "project_name": "<resolved>",
  "generated_at": "<ISO-8601 UTC>",
  "generated_by": "<model id>",
  "execution_control_contract": {
    "one_block_at_a_time": true,
    "durable_artifacts_updated_after_every_block": [
      "FABLE_EXECUTION_STATUS.json",
      "ledgers/FABLE_EVIDENCE_INDEX.md",
      "ledgers/FABLE_OWNER_DECISIONS.md",
      "ledgers/FABLE_NEXT_AGENT_HANDOFF.md",
      "ledgers/FABLE_REENTRY_NOTE.md"
    ],
    "hard_stop_categories": [
      "anything matching an unresolved {{OWNER:*}} placeholder",
      "spending money or calling paid APIs",
      "publishing, pushing, or deploying",
      "deleting or rewriting history",
      "touching paths the owner listed as protected"
    ],
    "verify_command": "python3 FABLES_HARNESS/verify_bundle.py"
  },
  "starter_prompts_file": "FABLE_START_HERE.md",
  "sections": ["<ordered section headings>"],
  "blocks": [
    {
      "block_index": 1,
      "html_id": "block-01",
      "workflow_label": "01",
      "section_heading": "<one of sections>",
      "role": "fable_builder",
      "block_type": "prompt",
      "language": "text",
      "is_static_complete": false,
      "static_completion_evidence": null,
      "manual_sent_tracking": true,
      "copy_control": true,
      "text_line_count": 0,
      "text_char_count": 0,
      "text_sha256": "<sha256 of text, lowercase hex>",
      "text": "<the full copy-paste prompt>"
    }
  ]
}
```

Field laws (verifier-enforced):

- `html_id` = `block-` + zero-padded `block_index` (2 digits up to 99); unique; ascending
  and gapless from `block-01`.
- `text_line_count` = `len(text.splitlines())`; `text_char_count` = `len(text)`;
  `text_sha256` = SHA-256 of the exact UTF-8 `text`.
- `role` ∈ `fable_builder` | `auditor`. `is_static_complete: true` only for work you
  verified ALREADY DONE during the survey, with `static_completion_evidence` naming the
  on-disk proof.

## FABLE_EXECUTION_STATUS.json — exact schema

Use `template/EXECUTION_STATUS.template.json` as the skeleton. Laws:

- One entry in `blocks[]` per playbook block, same order, `html_id` + `workflow_label` +
  `text_sha256` copied exactly from the playbook.
- `status` ∈ `not_started` | `in_progress` | `complete` | `complete_static` |
  `skipped_superseded` | `blocked_on_owner`.
- `current_state.current_next_block` = `{html_id, text_sha256}` of the FIRST block whose
  status is not in {`complete`, `complete_static`, `skipped_superseded`} — blocked blocks
  ARE the next block (the system waits on the owner; it does not route around them).
- `current_state.blocked_on_owner[]` lists every unresolved `{{OWNER:*}}` placeholder with
  the blocks it blocks.
- Every `complete`/`complete_static` block carries non-empty `evidence` (paths or ledger
  line references).
- Agents update this file after EVERY block, then run the verifier.

## Ledgers, control prompts, wargames

- Instantiate all five `template/ledgers/*.template.md` with generation placeholders
  resolved and the seeded first entries filled.
- Instantiate `template/meta_control_prompts.template.md`; its prompts become the closing
  playbook blocks (rule 4 above).
- Generate wargames per `wargames/WARGAME_METHOD.md` for every playbook block that is
  irreversible, owner-gated, spend-adjacent, or touches the owner's protected paths.

## Acceptance (all must hold before handoff to the owner)

1. `python3 FABLES_HARNESS/verify_bundle.py` exits **0**.
2. No generation placeholder survives anywhere in `FABLES_HARNESS/`.
3. Every unresolved owner placeholder on an active block appears with exactly its
   affected block IDs in `current_state.blocked_on_owner`, and has an OPEN decision row.
   Preserve owner-approved skip evidence for superseded blocks.
4. The playbook HTML opens from disk with no network access and renders every block.
5. Handoff message to the owner names: the START_HERE path, the exact next block, all
   owner gates, all placeholders.
