---
name: create-novel-project
description: Initialize a safe, self-contained Markdown novel workspace from the Novelist plugin scaffold. Use when the user wants to start, scaffold, bootstrap, or create a new novel project with source directories, templates, continuity rules, visual guidance, and EPUB output conventions.
---

# Create Novel Project

## Operating Contract

Create a novel source workspace from the scaffold bundled with this plugin. The
scaffold includes source directories, YAML-frontmatter templates, manuscript
markup rules, visual direction, and generated-output boundaries. It does not
copy another set of Agent Skills into the project; the installed Novelist plugin
continues to provide them.

Before running the bundled command, resolve `<skill-dir>` to the absolute
directory containing this `SKILL.md`.

## Workflow

1. Resolve the destination from the user's explicit path. If no path was given,
   use the current directory only when it is clearly the intended workspace;
   otherwise ask for the destination.
2. Gather a working title and BCP 47-style language tag when the user supplied
   them. Both are optional: the defaults remain `Untitled Novel` and `ko`.
3. Inspect the destination before writing. Preserve unrelated existing files.
4. Run the bundled initializer:

```bash
python3 "<skill-dir>/scripts/create_novel_project.py" \
  --project-root /absolute/path/to/novel \
  --title "Working Title" \
  --language ko
```

5. Do not pass `--force` merely because the destination exists. The initializer
   performs a complete collision preflight and writes nothing when a scaffold
   file would be overwritten. Use `--force` only after the user explicitly asks
   to replace the plugin-managed scaffold files.
6. Verify `project.md`, `AGENTS.md`, the source directories and templates, and
   `published/.gitignore`. Run `git status --short` when the destination is
   inside a Git repository.
7. Summarize the created paths and suggest the next relevant plugin skill, such
   as `$create-setting`, `$create-character`, or `$create-plot`.

## Safety Rules

- Never initialize into the plugin installation itself.
- Never delete unrelated destination files.
- Never copy `.git`, `.codex`, generated EPUB output, or project-local skill
  duplicates into the new workspace.
- Treat the copied Markdown files as canonical source and `published/` as
  generated output.
- Do not commit unless the user asks.
