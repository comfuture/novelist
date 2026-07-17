# Novelist Codex Plugin

Novelist packages the repository's structured fiction-writing workflows as a
Codex plugin. It provides skills for project initialization, setting, character,
material and plot creation, whole-novel storytelling, visual assets, and
validated EPUB publication.

## Install From This Repository

Add the repository marketplace once, then install the plugin:

```bash
codex plugin marketplace add /absolute/path/to/novelist
codex plugin add novelist@novelist
```

Start a new Codex task after installation so the plugin skills are loaded.

## Public Information

- Website: https://novelist.comfuture.chatgpt.site
- Support: https://novelist.comfuture.chatgpt.site/support
- Privacy policy: https://novelist.comfuture.chatgpt.site/privacy
- Terms of use: https://novelist.comfuture.chatgpt.site/terms
- Release notes: https://novelist.comfuture.chatgpt.site/releases
- Contact: Changkyun Kim <comfuture@gmail.com>
- License: MIT

## Included Skills

- `create-novel-project`
- `create-setting`
- `create-character`
- `create-material`
- `create-plot`
- `novel-story-telling`
- `create-visual-asset`
- `publish-novel`

`create-novel-project` copies only the source scaffold into the destination.
It does not vendor a second copy of the installed plugin skills.

## Development

The repository-local `.agents/skills/` tree is canonical for the seven shared
writing skills. Synchronize it and the source scaffold into this plugin with:

```bash
python3 scripts/sync_novelist_plugin.py
```

Use `--check` in validation or CI to detect drift without modifying files.
