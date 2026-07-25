# Migrating To Novelist 0.1.1

Novelist 0.1.1 makes the installable plugin the canonical distribution. This is
a breaking layout change for people who cloned the repository and wrote a novel
directly in its root. The installed plugin's eight-skill workflow remains
compatible.

## If You Already Install The Plugin

Update or reinstall Novelist through your agent host and start a new session.
Your existing novel workspaces do not need to change their source schema,
chapter format, or EPUB workflow.

## If You Used A Clone As Your Novel Workspace

Do not pull this release directly over authored work and do not run a scaffold
command with `--force` against an existing novel.

1. Back up or commit the authored workspace.
2. Keep its `project.md`, story directories, assets, chapters, and style files.
3. Install Novelist in Codex, Claude Code, or Antigravity CLI and continue using
   that existing workspace; or create a new standalone workspace and copy the
   authored sources after reviewing collisions.
4. Re-run continuity and publication validation before replacing any generated
   output.

Existing authored repositories are not migrated automatically.

## Standalone Snapshot

To keep a self-contained repository without installing the plugin:

```bash
sh scripts/create-scaffold.sh --destination ../my-novel --agent all
```

PowerShell:

```powershell
.\scripts\create-scaffold.ps1 --destination ..\my-novel --agent all
```

Windows Command Prompt:

```bat
scripts\create-scaffold.bat --destination ..\my-novel --agent all
```

Modes:

- `codex`: scaffold plus seven skills under `.agents/skills/`
- `claude`: scaffold plus seven skills under `.claude/skills/`
- `antigravity`: scaffold plus seven skills under `.agents/skills/`
- `all`: scaffold plus both local skill layouts

Codex and Antigravity share the open `.agents/skills/` layout. Claude Code uses
`.claude/skills/`. The plugin-only `create-novel-project` initializer is not
copied because the standalone exporter has already initialized the workspace.

A standalone export is a snapshot. It remains usable without the source
repository or an installed Novelist plugin, but it does not receive later
skill, scaffold, or safety updates automatically.

## Collision And Safety Behavior

The exporter checks the entire scaffold and skill plan before writing anything.
It refuses:

- existing managed files unless `--force` is explicitly supplied;
- symbolic-link destinations, parents, or managed targets;
- non-regular managed targets;
- destinations inside the plugin installation.

`--force` replaces only managed regular files and preserves unrelated files.
Always prefer a new empty destination for migration.
