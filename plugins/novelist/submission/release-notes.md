# Novelist 0.1.1 — Agent-Neutral Plugin Packaging

Novelist 0.1.1 keeps the installed plugin's eight-skill writing contract while
making the plugin payload the canonical source for Codex, Claude Code, and
Antigravity CLI.

Highlights:

- adds thin Claude Code and Antigravity plugin manifests;
- removes duplicate root scaffold and skill trees;
- adds safe POSIX, PowerShell, and Command Prompt standalone exporters for
  clone-first users;
- makes visual generation capability-aware and provider-neutral;
- repositions EPUB publication as the final step of the continuity-safe writing
  workflow;
- adds migration guidance for authored repositories that previously used the
  clone root directly.

This is a breaking repository-layout change for clone-first scaffold users, not
a breaking change to the installed plugin's novel source or skill contracts.
Public marketplace publication is handled separately from this source update.

# Novelist 0.1.0 — Initial Public Submission

Novelist packages eight Codex workflows for planning, writing, illustrating,
and publishing structured Markdown novels. It initializes a safe project
scaffold, develops story sources, controls whole-novel continuity and reader
understanding, and builds a validated EPUB from manuscript Draft sections.

This is the first public submission. The plugin is skills-only, requires no
external service or authentication, and sends no project data to a service
operated by the developer. Bundled scripts operate on the user's selected local
workspace. Users remain responsible for reviewing and publishing generated
content.

Reviewer notes:

- Submission type: Skills only
- Version: 0.1.0
- Publisher: Changkyun Kim
- Support: https://novelist.comfuture.chatgpt.site/support
- Test coverage: five positive and three negative reviewer scenarios
- License: MIT
