# Codex Image Generation

Use Codex's built-in `image_gen` capability when it is present in the current
task.

1. Build the complete style-locked prompt in the shared skill.
2. Invoke the image generator with that prompt.
3. Inspect the raster result before accepting it.
4. Save the selected output under `assets/cover/` or
   `assets/illustrations/`.
5. Register only the saved workspace-relative path.

Do not assume every Codex environment exposes image generation. If the
capability is absent, follow `external-image-provider.md` or return the final
prompt without claiming that an image was created.
