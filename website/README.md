# Novelist Website

This directory contains the public Novelist product, support, privacy, terms,
and release pages. It is generated and maintained through Codex agent
workflows rather than the repository-wide GitHub Actions validation matrix.

## Local Development

Requirements:

- Node.js `>=22.13.0`
- the package versions pinned in `package-lock.json`

```bash
npm install
npm run dev
```

## Validation

```bash
npm test
npm run build
```

Run these checks through the managing agent when website source changes. The
rendered HTML test checks the agent-neutral product description, Codex, Claude
Code, and Antigravity installation paths, standalone scaffold option, legal
routes, and migration release note.

The deployment configuration lives in `.openai/hosting.json`. Production
publishing is performed separately from source-only pull requests.
