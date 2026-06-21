---
name: create-visual-asset
description: Create cover and illustration image assets for the el_empiezo novel project using the built-in image generation workflow. Use when the user wants to plan, generate, refine, or save a book cover, chapter illustration, spot illustration, visual motif, or image prompt while preserving a consistent visual style across assets.
---

# Create Visual Asset

## Overview

Use this skill to create project-bound cover and illustration assets for the novel.

Always preserve visual consistency by reading `style/visual-style-guide.md` first. Use the built-in image generation skill/tool for raster image generation. Save final project-bound assets under `assets/cover/` or `assets/illustrations/`; never leave a referenced asset only in the image generator's default output location.

## Required Context

Read before generating:

- `AGENTS.md`
- `project.md`
- `style/visual-style-guide.md`
- relevant `chapters/*.md`, `outlines/`, `plot/`, `world/`, `characters/`, `materials/`, and `macguffins/` files for the requested asset
- existing files in `assets/cover/` and `assets/illustrations/`

If `style/visual-style-guide.md` is incomplete, ask the user for missing visual direction before generating a final asset.

## Workflow

### 1. Identify Asset Type

Classify the request as one of:

- `cover`: front cover image for EPUB packaging
- `chapter-illustration`: full-width or full-page illustration tied to a chapter
- `spot-illustration`: smaller image embedded within a chapter
- `motif`: reusable visual symbol, object, or atmospheric plate
- `reference`: visual exploration not yet used in the manuscript

Confirm the intended destination and filename slug before saving.

### 2. Gather Direction

Summarize the likely image in Korean:

- subject
- narrative moment or symbolic function
- setting and time period
- characters shown or deliberately omitted
- composition and crop
- mood, lighting, palette, and texture
- continuity constraints from source files
- whether text should be included

Ask for missing direction when it affects the image. For covers, ask about tone, central image, and whether the title/author text should be left out for later typography. Prefer no generated text unless the user explicitly asks for it.

### 3. Build A Style-Locked Prompt

Use the visual style guide as the stable base. Keep the prompt concise but specific:

```text
Use case: illustration-story
Asset type: <cover|chapter-illustration|spot-illustration|motif|reference>
Primary request: <specific image>
Story context: <chapter/plot/world context>
Style/medium: <from style/visual-style-guide.md>
Composition/framing: <crop, subject placement, negative space>
Lighting/mood: <from style guide plus asset-specific mood>
Color palette: <from style guide>
Materials/textures: <paper, ink, grain, brush, lens, etc.>
Continuity constraints: <must match story facts>
Text: no text, no title, no watermark unless explicitly requested
Avoid: <style guide avoid list plus asset-specific avoid list>
```

### 4. Generate With Imagegen

Use the built-in image generation path. Do not substitute SVG, HTML, or placeholder art.

For project-bound assets:

1. Generate the image with the built-in image generation workflow.
2. Inspect the result for style, subject, composition, and continuity.
3. Iterate only with targeted changes.
4. Move or copy the final selected image into the project:
   - cover: `assets/cover/<slug>.<ext>`
   - chapter illustration, spot illustration, motif, or reference: `assets/illustrations/<slug>.<ext>`
5. Report the saved path and final prompt.

### 5. Register In Markdown

For cover assets, store or update the cover path in `project.md` frontmatter when the user confirms it as the active cover:

```yaml
cover_image: assets/cover/cover.png
```

For chapter illustrations, add a normal Markdown image reference inside the target chapter when the user asks to insert it:

```markdown
![Alt text](../assets/illustrations/001-scene-slug.png)
```

Do not edit manuscript prose merely to place an image unless requested.

## Cover Missing During EPUB Build

If another workflow needs a cover and no usable cover exists, ask whether to generate one. Ask for the desired feeling, central image, and whether it should include text. If the user approves, use this skill to create the cover before building the EPUB.

## Verification

Before finishing:

- Confirm the final asset exists inside the workspace.
- Confirm the filename is filesystem-safe.
- Confirm project or chapter references use relative paths that the EPUB builder can resolve.
- Confirm the image follows `style/visual-style-guide.md`.
- Run `git status --short` and report changed files.
