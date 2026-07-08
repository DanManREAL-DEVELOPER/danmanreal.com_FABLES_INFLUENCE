#!/usr/bin/env python3
"""verify_bundle.py — integrity gate for a generated FABLES_HARNESS.

From the FABLES_INFLUENCE kit. This file is COPIED unmodified into the generated
FABLES_HARNESS/ folder and run from anywhere:

    python3 FABLES_HARNESS/verify_bundle.py

Exit codes (gate semantics):
    0  CLEAN PASS       — playbook JSON, status JSON, and playbook HTML all agree
    1  PASS WITH NOTES  — consistent, but soft findings worth reading
    2  HARD FAIL        — the harness is lying somewhere; HALT, repair, re-run

The one law behind every check: no agent may quietly drift the plan. If this gate
fails, fix the harness — never the verifier.
"""

import hashlib
import html as html_mod
import json
import os
import re
import sys

BUNDLE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BUNDLE)
PLAYBOOK = os.path.join(BUNDLE, "FABLE_PROMPT_PLAYBOOK.json")
STATUS = os.path.join(BUNDLE, "FABLE_EXECUTION_STATUS.json")
HTML = os.path.join(BUNDLE, "FABLE_PROMPT_PLAYBOOK.html")
START_HERE = os.path.join(BUNDLE, "FABLE_START_HERE.md")
META_PROMPTS = os.path.join(BUNDLE, "meta_control_prompts.md")
LEDGERS = [
    "ledgers/FABLE_EVIDENCE_INDEX.md",
    "ledgers/FABLE_OWNER_DECISIONS.md",
    "ledgers/FABLE_NEXT_AGENT_HANDOFF.md",
    "ledgers/FABLE_PRE_BLOCK_SANITY_CHECK.md",
    "ledgers/FABLE_REENTRY_NOTE.md",
]
WARGAME_FILES = ["wargames/SUCCESS.md", "wargames/LEDGER.md", "wargames/QUEUE.md"]

COMPLETE_STATUSES = {"complete", "complete_static"}
SKIP_STATUSES = {"skipped_superseded"}
VALID_STATUSES = COMPLETE_STATUSES | SKIP_STATUSES | {
    "not_started", "in_progress", "blocked_on_owner",
}
ROLES = {"fable_builder", "auditor"}
OWNER_PH_RE = re.compile(r"\{\{OWNER:[A-Za-z0-9_\-]+\}\}")
GEN_PH_RE = re.compile(r"\{\{(?!OWNER:)[A-Za-z0-9_\-: ]+\}\}")

hard, notes = [], []


def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001
        hard.append(f"A: JSON failed to load: {os.path.relpath(path, BUNDLE)}: {e}")
        return None


def main():
    # ---- A: files exist and parse -------------------------------------------
    for p in [PLAYBOOK, STATUS, HTML, START_HERE, META_PROMPTS] + [
        os.path.join(BUNDLE, x) for x in LEDGERS
    ]:
        if not os.path.exists(p):
            hard.append(f"A: required file missing: {os.path.relpath(p, BUNDLE)}")
        elif os.path.getsize(p) == 0:
            hard.append(f"A: required file empty: {os.path.relpath(p, BUNDLE)}")
    for x in WARGAME_FILES:
        if not os.path.exists(os.path.join(BUNDLE, x)):
            notes.append(f"A: wargame file not present: {x} (fine only if the owner "
                         "explicitly accepted a no-wargames run)")
    pb = load_json(PLAYBOOK) if os.path.exists(PLAYBOOK) else None
    st = load_json(STATUS) if os.path.exists(STATUS) else None
    if hard or pb is None or st is None:
        return finish()

    # ---- B: playbook internal consistency -----------------------------------
    blocks = pb.get("blocks") or []
    if not blocks:
        hard.append("B: playbook has no blocks")
        return finish()
    sections = pb.get("sections") or []
    seen_ids = set()
    for i, b in enumerate(blocks, start=1):
        bid = b.get("html_id")
        if b.get("block_index") != i:
            hard.append(f"B: block_index not gapless-ascending at position {i} ({b.get('block_index')})")
        if bid != f"block-{i:02d}":
            hard.append(f"B: html_id mismatch at index {i}: {bid!r} (want 'block-{i:02d}')")
        if bid in seen_ids:
            hard.append(f"B: duplicate html_id {bid}")
        seen_ids.add(bid)
        t = b.get("text") or ""
        if not t.strip():
            hard.append(f"B: {bid} has empty text")
        if b.get("text_line_count") != len(t.splitlines()):
            hard.append(f"B: {bid} text_line_count wrong")
        if b.get("text_char_count") != len(t):
            hard.append(f"B: {bid} text_char_count wrong")
        if b.get("text_sha256") != sha256(t):
            hard.append(f"B: {bid} text_sha256 wrong")
        if b.get("role") not in ROLES:
            hard.append(f"B: {bid} role {b.get('role')!r} not in {sorted(ROLES)}")
        if sections and b.get("section_heading") not in sections:
            hard.append(f"B: {bid} section_heading not in sections[]")
        if b.get("is_static_complete") and not b.get("static_completion_evidence"):
            hard.append(f"B: {bid} is_static_complete without static_completion_evidence")
    if len(blocks) > 60:
        notes.append(f"B: {len(blocks)} blocks (>60) — consider splitting the project")

    # ---- C: STATUS parity ----------------------------------------------------
    sblocks = st.get("blocks") or []
    if len(sblocks) != len(blocks):
        hard.append(f"C: STATUS has {len(sblocks)} blocks, playbook has {len(blocks)}")
    pmap = {b.get("html_id"): b for b in blocks}
    owner_ph_open = set()
    for i, sb in enumerate(sblocks, start=1):
        sid = sb.get("html_id")
        p = pmap.get(sid)
        if p is None:
            hard.append(f"C: STATUS block {sid!r} not in playbook")
            continue
        if sb.get("text_sha256") != p.get("text_sha256"):
            hard.append(f"C: STATUS {sid} text_sha256 does not match playbook")
        status = sb.get("status")
        if status not in VALID_STATUSES:
            hard.append(f"C: STATUS {sid} invalid status {status!r}")
        if status in COMPLETE_STATUSES and not sb.get("evidence"):
            hard.append(f"C: STATUS {sid} is {status} with empty evidence — "
                        "evidence or it didn't happen")
        if status not in COMPLETE_STATUSES:
            owner_ph_open.update(OWNER_PH_RE.findall(p.get("text") or ""))
    done_or_skip = COMPLETE_STATUSES | SKIP_STATUSES
    firsts = [sb.get("html_id") for sb in sblocks if sb.get("status") not in done_or_skip]
    cnb = (st.get("current_state") or {}).get("current_next_block") or {}
    if firsts:
        if cnb.get("html_id") != firsts[0]:
            hard.append(f"C: current_next_block={cnb.get('html_id')!r} but first "
                        f"non-complete non-skipped block is {firsts[0]!r}")
        want_sha = pmap.get(firsts[0], {}).get("text_sha256")
        if cnb.get("text_sha256") != want_sha:
            hard.append("C: current_next_block text_sha256 does not match the playbook")
    elif cnb.get("html_id"):
        notes.append("C: all blocks complete/skipped but current_next_block still set")
    listed = {row.get("placeholder") for row in
              (st.get("current_state") or {}).get("blocked_on_owner") or []}
    for ph in sorted(owner_ph_open):
        if ph not in listed:
            hard.append(f"C: unresolved owner gate {ph} (in a non-complete block) is "
                        "missing from current_state.blocked_on_owner")

    # ---- E: HTML parity ------------------------------------------------------
    page = open(HTML, encoding="utf-8").read() if os.path.exists(HTML) else ""
    tex = dict(re.findall(r'<textarea id="(block-\d+)"[^>]*>(.*?)</textarea>', page, re.S))
    for b in blocks:
        bid, want = b["html_id"], b.get("text") or ""
        if bid not in tex:
            hard.append(f"E: HTML missing <textarea id=\"{bid}\">")
            continue
        got = html_mod.unescape(tex[bid])
        if got != want and got.lstrip("\n") != want and got.strip() != want.strip():
            hard.append(f"E: HTML textarea {bid} text differs from playbook JSON")
    for attr in ("data-copy", "data-sent"):
        n = page.count(f'{attr}="block-')
        if n < len(blocks):
            hard.append(f"E: HTML has {n} {attr} controls for {len(blocks)} blocks")
    m = re.search(r'<script type="application/json" id="workflow-data">(.*?)</script>',
                  page, re.S)
    if not m:
        hard.append("E: HTML missing embedded workflow-data JSON blob")
    else:
        try:
            wf = json.loads(html_mod.unescape(m.group(1)))
        except Exception as e:  # noqa: BLE001
            wf = None
            hard.append(f"E: workflow-data blob is not valid JSON: {e}")
        if isinstance(wf, dict):
            wf = wf.get("blocks") or []
        if isinstance(wf, list):
            wmap = {w.get("html_id"): w for w in wf if isinstance(w, dict)}
            for b in blocks:
                w = wmap.get(b["html_id"])
                if w is None:
                    hard.append(f"E: workflow-data missing {b['html_id']}")
                elif w.get("text_sha256") != b.get("text_sha256"):
                    hard.append(f"E: workflow-data sha mismatch for {b['html_id']}")

    # ---- F: HTML self-containment -------------------------------------------
    for ref in re.findall(r'https?://[^\s"\'<>&)]+', page):
        if "www.w3.org" not in ref:
            hard.append(f"F: external reference in HTML: {ref[:80]}")
    for tok in ("fetch(", "XMLHttpRequest", "import("):
        if tok in page:
            hard.append(f"F: HTML contains forbidden network/exec token: {tok}")

    # ---- G: no leftover generation placeholders ------------------------------
    for root, _dirs, files in os.walk(BUNDLE):
        for fn in files:
            if not fn.endswith((".md", ".json", ".html", ".txt")):
                continue
            fp = os.path.join(root, fn)
            try:
                body = open(fp, encoding="utf-8").read()
            except Exception:  # noqa: BLE001
                continue
            for ph in sorted(set(GEN_PH_RE.findall(body))):
                hard.append(f"G: unresolved generation placeholder {{{{{ph.strip('{}')}}}}} "
                            f"in {os.path.relpath(fp, BUNDLE)}")

    # ---- H: soft signals -----------------------------------------------------
    for sb in sblocks:
        ev = sb.get("evidence")
        if sb.get("status") in COMPLETE_STATUSES and isinstance(ev, str):
            for cand in re.findall(r"[\w./\-]+/[\w./\-]+", ev):
                fp = os.path.join(PROJECT_ROOT, cand)
                if ("/" in cand and not os.path.exists(fp)
                        and not cand.startswith(("http", "www"))):
                    notes.append(f"H: {sb.get('html_id')} evidence path not found on "
                                 f"disk: {cand}")
    done = sum(1 for sb in sblocks if sb.get("status") in COMPLETE_STATUSES)
    notes.append(f"H: progress {done}/{len(blocks)} blocks complete; "
                 f"{len(owner_ph_open)} owner gate(s) open")
    return finish()


def finish():
    for x in hard:
        print(f"HARD FAIL  {x}")
    for x in notes:
        print(f"note       {x}")
    if hard:
        print(f"\nVERDICT: HARD FAIL ({len(hard)}) — exit 2. HALT and repair; "
              "fix the harness, never this verifier.")
        return 2
    if [n for n in notes if not n.startswith("H: progress")]:
        print("\nVERDICT: PASS WITH NOTES — exit 1")
        return 1
    print("\nVERDICT: CLEAN PASS — exit 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
