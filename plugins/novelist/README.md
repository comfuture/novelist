# Novelist: Agent-Assisted Novel Writing

Novelist manages interconnected Markdown story assets and applies
genre-specific writing strategies so an agent can help an author write a
coherent long-form novel. EPUB packaging remains the final integrated delivery
step.

## Install

### Codex

Published installation:

```bash
codex plugin add novelist@openai-curated-remote
```

Local repository installation:

```bash
codex plugin marketplace add /absolute/path/to/novelist
codex plugin add novelist@novelist
```

Start a new Codex task after installation. Invoke skills as
`$create-character`, `$novel-story-telling`, and so on.

### Claude Code

```bash
claude plugin marketplace add comfuture/novelist
claude plugin install novelist@novelist --scope user
```

Reload plugins or start a new session. Invoke skills as
`/novelist:create-character`, `/novelist:novel-story-telling`, and so on.

### Antigravity CLI (`agy`)

```bash
agy plugins install https://github.com/comfuture/novelist
agy plugin list
```

Invoke installed skills by their frontmatter name, such as
`/create-character` or `/novel-story-telling`. This public-repository
installation was verified with `agy 1.1.7`.

## Included Skills

- `create-novel-project`
- `create-setting`
- `create-character`
- `create-material`
- `create-plot`
- `novel-story-telling`
- `create-visual-asset`
- `publish-novel`

The initializer copies only `assets/scaffold/`. Installed plugin skills remain
in the host's plugin cache and are not duplicated inside the generated novel.

The visual-asset skill selects from capabilities actually present in the host:
Codex `image_gen`, a configured MCP or CLI tool, or an author-selected external
provider. When none is available, it preserves the final prompt and does not
claim that an image exists.

## Standalone Alternative

Users who do not want to install a plugin can run the repository's
`scripts/create-scaffold.sh`, `.ps1`, or `.bat` wrapper. Standalone export
includes the scaffold and seven project-operating skills; the plugin-only
initializer is intentionally omitted. See the root `README.md` and
`MIGRATION.md`.

## Development And Validation

This directory is the canonical plugin payload. Shared skills and scaffold
files are maintained here directly.

```bash
python3 scripts/sync_novelist_plugin.py --check
claude plugin validate plugins/novelist --strict
agy plugin validate plugins/novelist
```

## Public Information

- Website: https://novelist.comfuture.chatgpt.site
- Support: https://novelist.comfuture.chatgpt.site/support
- Privacy policy: https://novelist.comfuture.chatgpt.site/privacy
- Terms of use: https://novelist.comfuture.chatgpt.site/terms
- Release notes: https://novelist.comfuture.chatgpt.site/releases
- Contact: Changkyun Kim <comfuture@gmail.com>
- License: MIT
