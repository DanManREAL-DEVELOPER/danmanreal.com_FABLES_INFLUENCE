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
from html.parser import HTMLParser
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


def valid_shapes(pb, st):
    """Fail closed before comparing untrusted generated JSON structures."""
    for label, value in (("playbook", pb), ("status", st)):
        if not isinstance(value, dict):
            hard.append(f"A: {label} must be a JSON object")
            continue
        if value.get("schema_version") != "fables-influence-1.0":
            hard.append(f"A: {label} schema_version is unsupported")
        if not isinstance(value.get("project_name"), str) or not value["project_name"].strip():
            hard.append(f"A: {label} project_name is required")
        blocks = value.get("blocks")
        if not isinstance(blocks, list) or not blocks:
            hard.append(f"A: {label} blocks must be a non-empty list")
            continue
        fields = ("html_id", "workflow_label", "section_heading", "role", "text_sha256")
        if label == "playbook":
            fields += ("text",)
        else:
            fields += ("status",)
        for index, block in enumerate(blocks):
            if not isinstance(block, dict) or any(not isinstance(block.get(k), str) for k in fields):
                hard.append(f"A: {label} block {index + 1} has invalid fields")
            elif label == "playbook" and any(type(block.get(k)) is not int for k in ("block_index", "text_line_count", "text_char_count")):
                hard.append(f"A: playbook block {index + 1} counts must be integers")
            elif label == "status":
                ev = block.get("evidence")
                if ev is not None and not isinstance(ev, str) and not (isinstance(ev, list) and all(isinstance(x, str) and x.strip() for x in ev)):
                    hard.append(f"A: status block {index + 1} evidence must be text or a list of references")
    if hard:
        return False
    if pb["project_name"] != st["project_name"]:
        hard.append("A: playbook and status belong to different projects")
    if not isinstance(pb.get("sections"), list) or not all(isinstance(x, str) for x in pb["sections"]):
        hard.append("A: sections must be a list of headings")
    current = st.get("current_state")
    if not isinstance(current, dict):
        hard.append("A: current_state must be an object")
    else:
        if not isinstance(current.get("current_next_block"), dict):
            hard.append("A: current_next_block must be an object (empty when finished)")
        gates = current.get("blocked_on_owner")
        if not isinstance(gates, list) or any(not isinstance(x, dict) or not isinstance(x.get("placeholder"), str) or not isinstance(x.get("blocks"), list) or not all(isinstance(b, str) for b in x["blocks"]) for x in gates):
            hard.append("A: blocked_on_owner requires named placeholders and block lists")
    return not hard


class PlaybookHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.ids = []
        self.textareas = []
        self.scripts = []
        self.controls = {"data-copy": [], "data-sent": []}
        self.capture = None
        self.styles = []

    def handle_starttag(self, tag, attrs):
        if len({key for key, _ in attrs}) != len(attrs):
            hard.append("E: duplicate HTML attributes are ambiguous")
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        for attr in self.controls:
            if attr in attrs:
                self.controls[attr].append(attrs[attr])
        if tag in {"textarea", "script", "style"}:
            node = {"id": attrs.get("id"), "type": attrs.get("type", ""), "text": ""}
            self.capture = (tag, node)
            if tag == "textarea": self.textareas.append(node)
            elif tag == "script": self.scripts.append(node)
            else: self.styles.append(node)
        for attr, value in attrs.items():
            if not value:
                continue
            if attr in {"src", "srcset", "poster", "data", "xlink:href"} or (attr == "href" and tag != "a"):
                if not value.startswith(("data:", "#")):
                    hard.append(f"F: loaded resource is not inline: {tag} {attr}={value[:80]!r}")
            if attr == "href" and tag == "a" and value.strip().lower().startswith(("javascript:", "vbscript:")):
                hard.append("F: hyperlink contains executable code")
            if attr == "style": self.styles.append({"text": value})
            if attr.startswith("on"): self.scripts.append({"id": None, "type": "", "text": value})

    def handle_endtag(self, tag):
        if self.capture and self.capture[0] == tag:
            self.capture = None

    def handle_data(self, data):
        if self.capture:
            self.capture[1]["text"] += data

    def handle_entityref(self, name):
        import html
        self.handle_data(html.unescape("&" + name + ";"))

    def handle_charref(self, name):
        import html
        self.handle_data(html.unescape("&#" + name + ";"))


def check_html(page, blocks):
    parsed = PlaybookHTML()
    parsed.feed(page)
    if len(parsed.ids) != len(set(parsed.ids)):
        hard.append("E: duplicate HTML IDs make copy targets ambiguous")
    ids = [b["html_id"] for b in blocks]
    if [x["id"] for x in parsed.textareas] != ids:
        hard.append("E: textarea IDs must match playbook order exactly, without duplicates")
    for node, block in zip(parsed.textareas, blocks):
        got, want = node["text"], block["text"]
        if got != want and not (got.startswith("\n") and got[1:] == want):
            hard.append(f"E: HTML textarea {node['id']} text differs from playbook JSON")
    for attr, values in parsed.controls.items():
        if len(values) != len(ids) or sorted(values) != sorted(ids):
            hard.append(f"E: {attr} must target each block exactly once")
    workflow = [x for x in parsed.scripts if x["id"] == "workflow-data" and x["type"] == "application/json"]
    if len(workflow) != 1:
        hard.append("E: exactly one application/json workflow-data script is required")
    else:
        try:
            wf = json.loads(workflow[0]["text"])
            if isinstance(wf, dict): wf = wf.get("blocks")
            if not isinstance(wf, list) or not all(isinstance(x, dict) for x in wf):
                raise ValueError("workflow-data must contain a list of block objects")
            if [x.get("html_id") for x in wf] != ids:
                hard.append("E: workflow-data must match block order exactly, without duplicates")
            for node, block in zip(wf, blocks):
                for key in ("html_id", "workflow_label", "section_heading", "role", "text_sha256"):
                    if node.get(key) != block[key]: hard.append(f"E: workflow-data {key} mismatch for {block['html_id']}")
                if type(node.get("index")) is not int or node["index"] != block["block_index"]:
                    hard.append(f"E: workflow-data index mismatch for {block['html_id']}")
        except (ValueError, TypeError) as error:
            hard.append(f"E: invalid workflow-data: {error}")
    for node in parsed.scripts:
        if node["type"] in {"application/json", "importmap"}:
            continue
        if re.search(r"\b(?:fetch|import|WebSocket|EventSource)\s*\(|\bimport\s+(?:[\w*{]|[\"\'])|\bexport\s+.*?\bfrom\s*[\"\']|XMLHttpRequest|navigator\s*\.\s*sendBeacon", node["text"]):
            hard.append("F: active script contains a network-loading operation")
    for node in parsed.styles:
        if re.search(r"@import\b", node["text"], re.I): hard.append("F: CSS imports a resource")
        for value in re.findall(r"url\(\s*['\"]?([^)'\"]+)", node["text"], re.I):
            if not value.strip().startswith(("data:", "#")): hard.append("F: CSS resource is not inline")

def main():
    hard.clear()
    notes.clear()
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
    if hard:
        return finish()

    if not valid_shapes(pb, st):
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
    if [b["html_id"] for b in sblocks] != [b["html_id"] for b in blocks]:
        hard.append("C: status IDs must match playbook order exactly, without duplicates")
    pmap = {b.get("html_id"): b for b in blocks}
    owner_ph_open = set()
    for i, sb in enumerate(sblocks, start=1):
        sid = sb.get("html_id")
        p = pmap.get(sid)
        if p is None:
            hard.append(f"C: STATUS block {sid!r} not in playbook")
            continue
        for field in ("workflow_label", "section_heading", "role"):
            if sb.get(field) != p.get(field):
                hard.append(f"C: STATUS {sid} {field} does not match playbook")
        if sb.get("text_sha256") != p.get("text_sha256"):
            hard.append(f"C: STATUS {sid} text_sha256 does not match playbook")
        status = sb.get("status")
        if status not in VALID_STATUSES:
            hard.append(f"C: STATUS {sid} invalid status {status!r}")
        if status in COMPLETE_STATUSES and not sb.get("evidence"):
            hard.append(f"C: STATUS {sid} is {status} with empty evidence — "
                        "evidence or it didn't happen")
        placeholders = set(OWNER_PH_RE.findall(p.get("text") or ""))
        if placeholders and status not in SKIP_STATUSES:
            owner_ph_open.update(placeholders)
            if status != "blocked_on_owner":
                hard.append(f"C: {sid} contains unresolved owner values but is not blocked_on_owner")
        if status in SKIP_STATUSES and not sb.get("evidence"):
            hard.append(f"C: {sid} skipped without an owner-decision evidence reference")
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
        named = [row for row in st["current_state"]["blocked_on_owner"] if row["placeholder"] == ph]
        expected = {b["html_id"] for b in blocks if ph in b["text"] and next((x["status"] for x in sblocks if x["html_id"] == b["html_id"]), "") not in SKIP_STATUSES}
        if len(named) != 1 or set(named[0]["blocks"]) != expected:
            hard.append(f"C: owner placeholder {ph} must list its exact affected blocks once")
        if ph not in listed:
            hard.append(f"C: unresolved owner gate {ph} (in a non-complete block) is "
                        "missing from current_state.blocked_on_owner")

    # ---- E: HTML parity ------------------------------------------------------
    page = open(HTML, encoding="utf-8").read() if os.path.exists(HTML) else ""
    check_html(page, blocks)

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
