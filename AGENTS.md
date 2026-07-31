# AGENTS.md

## Repository Purpose

This repository develops and distributes Novelist, an agent-assisted
novel-writing plugin for Codex, Claude Code, and Antigravity CLI.

The repository root is not a novel workspace. The canonical plugin payload is
`plugins/novelist/`. Generated novel projects come from
`plugins/novelist/assets/scaffold/`.

## Canonical Sources

- `plugins/novelist/skills/`: all nine canonical plugin skills.
- `plugins/novelist/assets/scaffold/`: the canonical generated-workspace
  scaffold.
- `plugins/novelist/.codex-plugin/plugin.json`: Codex adapter metadata.
- `plugins/novelist/.claude-plugin/plugin.json`: Claude Code adapter metadata.
- `plugins/novelist/plugin.json`: Antigravity CLI adapter metadata.
- `.agents/plugins/marketplace.json`: Codex repository marketplace.
- `.claude-plugin/marketplace.json`: Claude Code repository marketplace.
- `scripts/create_scaffold.py`: canonical standalone scaffold exporter.
- `scripts/create-scaffold.sh`, `.ps1`, and `.bat`: thin platform entry points.

Do not recreate `.agents/skills/` or a novel scaffold at the repository root.
Do not edit installed plugin cache copies.

## Adapter Boundaries

Keep shared workflows in `plugins/novelist/skills/`. Do not fork complete skill
trees by host.

- `skills/*/agents/openai.yaml` is Codex/OpenAI presentation metadata.
- Claude-specific packaging belongs under `.claude-plugin/`.
- Antigravity's root `plugin.json` accepts only its documented minimal fields.
- Host-specific image-generation instructions belong in
  `create-visual-asset/references/`.
- The shared visual workflow must stay provider-neutral and must not claim an
  image was generated when no raster provider is connected.

## Scaffold Contract

Novel source files use Markdown with YAML frontmatter. Documentation files
named `README.md`, `AGENTS.md`, and `CLAUDE.md` do not need source frontmatter.

The canonical scaffold must remain self-contained inside the plugin. Never add
runtime reads from the repository root, symlinks, or hardlinks. Preserve:

- collision preflight and explicit `--force` behavior;
- destination and parent symlink rejection;
- plugin-installation boundary checks;
- `AGENTS.md` plus the `CLAUDE.md` import bridge;
- empty asset directories and generated-output ignore rules.

Standalone exports contain the scaffold plus eight project-operating skills.
The plugin-only `create-novel-project` initializer is intentionally excluded
because the standalone exporter has already performed that operation.

## Novel Workflow Compatibility

Do not change the novel source schema, chapter filename contract, chapter
section order, dialogue markup, continuity authority, or Draft-only EPUB
rendering unless an issue explicitly requires it.

EPUB publication remains an integrated final step, not the primary product
definition. Writing and documentation should lead with structured story assets,
continuity, reader-knowledge control, and genre-aware strategy.

Analytical review is a separate, read-only-by-default reviewer workflow. Invoke
it for an explicit outline, chapter, or manuscript review. Inject its bounded
whole-manuscript review, finding-disposition, revision, and regression-review
loop only when the author delegates a fully autonomous workflow from initial
planning through publication. Ordinary planning, drafting, revision, and
publication requests must keep their existing workflows and must not silently
add analytical review.

## Validation

Run focused tests first, then the complete relevant set:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/novelist/skills/create-novel-project/tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/novelist/skills/analytical-review/tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/novelist/skills/create-visual-asset/tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/novelist/skills/novel-story-telling/tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/novelist/skills/publish-novel/tests
python3 scripts/sync_novelist_plugin.py --check
uv run --with PyYAML python /path/to/plugin-creator/scripts/validate_plugin.py plugins/novelist
claude plugin validate plugins/novelist --strict
claude plugin validate . --strict
agy plugin validate plugins/novelist
```

These commands run the Python regression suites bundled with the skills. They
do not attempt to simulate an agent model invoking a skill; installed-host
discovery and invocation are separate smoke tests.

Validate `.sh` on POSIX and `.ps1` plus `.bat` on native Windows. Test installed
plugins from isolated host state when practical, and record tool versions when
host behavior is version-dependent.

The `website/` tree is maintained and validated through Codex agent workflows.
Keep it outside the repository-wide GitHub Actions matrix; when website source
changes, run its local tests and build through the managing agent.

## Documentation And Releases

Keep root, plugin, generated-workspace, website, migration, and release
documentation aligned. Installation choices must appear before development
details and EPUB examples.

Use semantic versions consistently across host manifests. The `0.1.1`
restructure changes clone-first scaffold usage but preserves the installed
plugin's core skill contract. The `0.2.0` release adds analytical review as the
ninth installed skill and the eighth standalone project-operating skill.

Never commit credentials. Documentation may use `API_KEY` or
`<PROVIDER>_API_KEY` placeholders only.

## Subagent Use

Use subagents only when necessary for independent discovery or validation.
Keep tasks concrete and non-overlapping, and do not let multiple agents edit
the same file.
