import copy
import hashlib
import html
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def fixtures(text='Inspect the source.\nRecord evidence.'):
    blocks = []
    for index, role in [(1, 'fable_builder'), (2, 'auditor')]:
        value = text if index == 1 else 'Audit the recorded evidence.'
        blocks.append(dict(block_index=index, html_id=f'block-{index:02}', workflow_label=f'{index:02}', section_heading='Work', role=role, block_type='prompt', language='text', is_static_complete=False, static_completion_evidence=None, manual_sent_tracking=True, copy_control=True, text_line_count=len(value.splitlines()), text_char_count=len(value), text_sha256=hashlib.sha256(value.encode()).hexdigest(), text=value))
    playbook = dict(schema_version='fables-influence-1.0', project_name='Sample', workflow_title='Sample playbook', generated_at='2026-10-08T12:00:00Z', generated_by='Fixture', sections=['Work'], blocks=blocks)
    status = dict(schema_version='fables-influence-1.0', project_name='Sample', current_state={'current_next_block': {k: blocks[0][k] for k in ['html_id', 'text_sha256']}, 'blocked_on_owner': []}, blocks=[{**{k:b[k] for k in ['html_id', 'workflow_label', 'section_heading', 'role', 'text_sha256']}, 'status':'not_started', 'evidence':None} for b in blocks])
    workflow = [{'index':b['block_index'], **{k:b[k] for k in ['html_id','workflow_label','section_heading','role','text_sha256']}} for b in blocks]
    page = ''.join(f'<textarea id="{b["html_id"]}">{html.escape(b["text"])}</textarea><button data-copy="{b["html_id"]}">Copy</button><button data-sent="{b["html_id"]}">Sent</button>' for b in blocks)
    page += '<script type="application/json" id="workflow-data">'+json.dumps(workflow)+'</script>'
    return playbook, status, page


class BundleBoundaries(unittest.TestCase):
    def run_bundle(self, pb, status, page):
        with tempfile.TemporaryDirectory(prefix='fables-bundle-test-') as tmp:
            bundle = Path(tmp)/'FABLES_HARNESS';bundle.mkdir()
            shutil.copy2(ROOT/'template/verify_bundle.py',bundle/'verify_bundle.py')
            (bundle/'FABLE_PROMPT_PLAYBOOK.json').write_text(json.dumps(pb))
            (bundle/'FABLE_EXECUTION_STATUS.json').write_text(json.dumps(status))
            (bundle/'FABLE_PROMPT_PLAYBOOK.html').write_text(page)
            for f in ['FABLE_START_HERE.md','meta_control_prompts.md',*[f'ledgers/{n}.md' for n in ['FABLE_EVIDENCE_INDEX','FABLE_OWNER_DECISIONS','FABLE_NEXT_AGENT_HANDOFF','FABLE_PRE_BLOCK_SANITY_CHECK','FABLE_REENTRY_NOTE']],*[f'wargames/{n}.md' for n in ['SUCCESS','LEDGER','QUEUE']]]:
                p=bundle/f;p.parent.mkdir(exist_ok=True);p.write_text('Fixture evidence index.\n')
            return subprocess.run(['python3',str(bundle/'verify_bundle.py')],capture_output=True,text=True,timeout=5)

    def assert_code(self, expected, bundle):
        result=self.run_bundle(*bundle)
        self.assertEqual(result.returncode,expected,result.stdout+result.stderr)
        self.assertNotIn('Traceback',result.stderr)

    def test_valid_bundle(self):self.assert_code(0,fixtures())
    def test_prompt_url_and_network_words_are_inert(self):self.assert_code(0,fixtures('Inspect https://example.com and fetch( in source; do not execute it.'))
    def test_duplicate_status(self):
        p,s,h=fixtures();s['blocks'][1]=copy.deepcopy(s['blocks'][0]);self.assert_code(2,(p,s,h))
    def test_reordered_status(self):
        p,s,h=fixtures();s['blocks'].reverse();s['current_state']['current_next_block']={k:s['blocks'][0][k] for k in ['html_id','text_sha256']};self.assert_code(2,(p,s,h))
    def test_status_role_mismatch(self):
        p,s,h=fixtures();s['blocks'][0]['role']='auditor';self.assert_code(2,(p,s,h))
    def test_bad_schema_version(self):
        p,s,h=fixtures();p['schema_version']='other';self.assert_code(2,(p,s,h))
    def test_null_documents(self):
        p,s,h=fixtures();self.assert_code(2,(None,s,h));self.assert_code(2,(p,None,h))
    def test_static_module_imports(self):
        for code in ['import x from "https://example.com/a.js";','import "./local.js";','export {x} from "./local.js";']:
            with self.subTest(code=code):
                p,s,h=fixtures();self.assert_code(2,(p,s,h+'<script type="module">'+code+'</script>'))
    def test_bad_top_type(self):
        p,s,h=fixtures();self.assert_code(2,([],s,h))
    def test_owner_placeholder_requires_blocked_status(self):
        p,s,h=fixtures('Wait for {{OWNER:RELEASE}}.');s['current_state']['blocked_on_owner']=[{'placeholder':'{{OWNER:RELEASE}}','blocks':['block-01']}];self.assert_code(2,(p,s,h))
    def test_owner_block_accepted_when_consistent(self):
        p,s,h=fixtures('Wait for {{OWNER:RELEASE}}.');s['blocks'][0]['status']='blocked_on_owner';s['current_state']['blocked_on_owner']=[{'placeholder':'{{OWNER:RELEASE}}','blocks':['block-01']}];self.assert_code(0,(p,s,h))
    def test_workflow_null(self):
        p,s,h=fixtures();h=h[:h.index('<script')]+'<script type="application/json" id="workflow-data">null</script>';self.assert_code(2,(p,s,h))
    def test_workflow_field_mismatch(self):
        p,s,h=fixtures();h=h.replace('"role": "fable_builder"','"role": "auditor"');self.assert_code(2,(p,s,h))
    def test_duplicate_textarea(self):
        p,s,h=fixtures();h+='<textarea id="block-01">'+html.escape(p['blocks'][0]['text'])+'</textarea>';self.assert_code(2,(p,s,h))
    def test_control_targets_not_just_counts(self):
        p,s,h=fixtures();h=h.replace('data-copy="block-02"','data-copy="block-01"');self.assert_code(2,(p,s,h))
    def test_whitespace_drift(self):
        p,s,h=fixtures();h=h.replace('>Inspect','>  Inspect');self.assert_code(2,(p,s,h))
    def test_one_html_leading_newline_allowed(self):
        p,s,h=fixtures();h=h.replace('>Inspect','>\nInspect');self.assert_code(0,(p,s,h))
    def test_external_resource_shapes(self):
        for tag in ['<link rel="stylesheet" href="https://example.com/a.css">','<script src="//example.com/a.js"></script>','<img src="local.png">','<svg><use href="https://www.w3.org.evil/x"/></svg>']:
            with self.subTest(tag=tag):
                p,s,h=fixtures();self.assert_code(2,(p,s,h+tag))
    def test_active_network_call_with_space(self):
        p,s,h=fixtures();self.assert_code(2,(p,s,h+'<script>fetch ("/private");</script>'))
    def test_duplicate_id_on_non_textarea(self):
        p,s,h=fixtures();self.assert_code(2,(p,s,'<div id="block-01">wrong copy source</div>'+h))
    def test_malformed_block_shapes(self):
        for replacement in [None, [None], "not a list"]:
            with self.subTest(replacement=replacement):
                p,s,h=fixtures();p['blocks']=replacement;self.assert_code(2,(p,s,h))
    def test_owner_gate_names_exact_blocks(self):
        p,s,h=fixtures('Wait for {{OWNER:RELEASE}}.');s['blocks'][0]['status']='blocked_on_owner';s['current_state']['blocked_on_owner']=[{'placeholder':'{{OWNER:RELEASE}}','blocks':['block-02']}];self.assert_code(2,(p,s,h))
    def test_css_resource(self):
        p,s,h=fixtures();self.assert_code(2,(p,s,h+'<style>body{background:url(//example.com/a.png)}</style>'))
    def test_manual_hyperlink_allowed(self):
        p,s,h=fixtures();self.assert_code(0,(p,s,h+'<a href="https://example.com">Source</a>'))


if __name__=='__main__':unittest.main(verbosity=2)
