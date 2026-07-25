# Novelist

Novelist is an agent-assisted novel-writing plugin for managing interconnected
Markdown assets and turning them into a coherent long-form story. It helps
authors develop worldbuilding, characters, materials, MacGuffins, plots,
outlines, style, chapters, continuity, and reader knowledge while applying
genre-specific storytelling strategies.

Validated EPUB publication is the final integrated delivery step, not the
plugin's primary purpose.

## Choose How To Use Novelist

### Install The Plugin (Recommended)

#### Codex

Install the published plugin, then start a new task:

```bash
codex plugin add novelist@openai-curated-remote
```

For local development, add this repository as a marketplace and install its
entry:

```bash
codex plugin marketplace add /absolute/path/to/novelist
codex plugin add novelist@novelist
```

Codex invokes skills as `$create-character`, `$novel-story-telling`, and so on.

#### Claude Code

Add this repository as a marketplace, install the plugin, and reload plugins:

```bash
claude plugin marketplace add /absolute/path/to/novelist
claude plugin install novelist@novelist --scope user
```

Claude Code invokes namespaced skills such as
`/novelist:create-character`.

#### Antigravity CLI (`agy`)

Install the plugin directory directly:

```bash
agy plugin install /absolute/path/to/novelist/plugins/novelist
agy plugin list
```

Antigravity exposes installed skills by their frontmatter name, for example
`/create-character` and `/novel-story-telling`. This form was verified against
the directly installed plugin with `agy 1.1.2`.

### Create A Standalone Scaffold

Use this compatibility path when you do not want to install a plugin. The
exported workspace contains the canonical scaffold and seven repository-local
writing skills. It is a snapshot and does not receive future plugin updates
automatically.

POSIX:

```bash
sh scripts/create-scaffold.sh \
  --destination ../my-novel \
  --agent all
```

PowerShell:

```powershell
.\scripts\create-scaffold.ps1 `
  --destination ..\my-novel `
  --agent all
```

Windows Command Prompt:

```bat
scripts\create-scaffold.bat --destination ..\my-novel --agent all
```

`--agent` accepts `codex`, `claude`, `antigravity`, or `all`. See
[MIGRATION.md](MIGRATION.md) before updating a repository that was previously
used directly as an authored novel workspace.

## Core Capabilities

- Keep story sources in reviewable Markdown with stable frontmatter IDs.
- Connect settings, characters, materials, MacGuffins, plots, outlines, and
  chapters without flattening them into one prompt.
- Build bounded context for a chapter and check structural plus semantic
  continuity.
- Track reader knowledge, reveal timing, active threads, and chapter state.
- Apply focused strategies for general story flow, wuxia, science fiction,
  time travel and loops, mystery, drama, and romantic entanglement.
- Create guarded chapter files without overwriting an existing chapter number.
- Plan visual assets through a provider-neutral workflow that can use a host
  tool, MCP server, or author-selected external provider.
- Finish by packaging only approved chapter Draft content into a validated
  EPUB.

## Included Skills

| Skill | Role |
| --- | --- |
| `create-novel-project` | Initialize a safe Markdown novel workspace. |
| `create-setting` | Develop world rules, locations, timelines, and institutions. |
| `create-character` | Develop characters, relationships, motivations, and continuity facts. |
| `create-material` | Capture motifs, objects, clues, research, dialogue seeds, and scene seeds. |
| `create-plot` | Build the central plot and supporting threads. |
| `novel-story-telling` | Control causality, escalation, reveals, continuity, and chapter handoffs. |
| `create-visual-asset` | Build style-locked prompts and create assets through an available raster provider. |
| `publish-novel` | Render approved Draft content and validate the final EPUB. |

## Typical Writing Flow

1. Initialize a workspace and define its premise, language, and constraints.
2. Establish world rules and the central cast.
3. Develop materials, MacGuffins, plots, and outlines.
4. Choose genre strategies and define the story promise, escalation, reveals,
   convergence, climax, cost, and aftermath.
5. Build a bounded context pack before each chapter.
6. Resolve continuity questions, approve the chapter contract, and write the
   guarded Draft.
7. Update newly established canon and reader-knowledge state.
8. Create optional visual assets through an available raster provider.
9. Publish the completed manuscript as a validated EPUB.

## Repository Layout

- `plugins/novelist/skills/`: canonical shared skills.
- `plugins/novelist/assets/scaffold/`: canonical generated project.
- `plugins/novelist/.codex-plugin/`: Codex adapter.
- `plugins/novelist/.claude-plugin/`: Claude Code adapter.
- `plugins/novelist/plugin.json`: Antigravity adapter.
- `.agents/plugins/marketplace.json`: Codex marketplace.
- `.claude-plugin/marketplace.json`: Claude Code marketplace.
- `scripts/create_scaffold.py`: standalone exporter shared by all wrappers.
- `tests/`: package and standalone export regression tests.
- `website/`: public product, support, policy, and release pages.

The plugin package is self-contained because installed hosts copy it into an
isolated cache. Runtime code must never depend on repository-root scaffold
files.

## Development

Validate the canonical payload and host adapters:

```bash
python3 scripts/sync_novelist_plugin.py --check
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/novelist/skills
claude plugin validate plugins/novelist --strict
claude plugin validate . --strict
agy plugin validate plugins/novelist
```

Codex validation uses the validator bundled with the `plugin-creator` system
skill and requires PyYAML:

```bash
uv run --with PyYAML python \
  /path/to/plugin-creator/scripts/validate_plugin.py \
  plugins/novelist
```

Public information is available at
[novelist.comfuture.chatgpt.site](https://novelist.comfuture.chatgpt.site).
