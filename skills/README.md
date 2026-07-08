# skills/

## dmr-danmanreal-design — "Use DanManREAL DESIGN"

The canonized DanManREAL visual design system, exactly as it lives in the DanManREAL
workspace (all three files byte-identical to the originals):

- `dmr-danmanreal-design/SKILL.md` — the skill entry: when it triggers, what it enforces.
- `dmr-danmanreal-design/references/DANMANREAL_DESIGN.md` — the written canon: tokens,
  paint treatment, typography laws, ALWAYS/NEVER lists.
- `dmr-danmanreal-design/references/exemplar.html` — the byte-exact exemplar. When canon
  and prose ever seem to disagree, the exemplar is the truth.

**Install:** copy the whole `dmr-danmanreal-design/` folder into your project's
`.claude/skills/` directory (the genesis prompt does this for you as Phase 1). From then
on, telling your agent "Use DanManREAL DESIGN" applies the system to anything it builds.

**Provenance note:** the skill text references a few files from its home workspace (brand
token sources, an HTML fit-checker). Those references are provenance, not dependencies —
the canon document and the exemplar in this folder are complete and self-sufficient.
