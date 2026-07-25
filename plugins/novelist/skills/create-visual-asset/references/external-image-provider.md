# External Image Provider

Use this path when the current agent does not expose a verified raster image
generator.

## Security Contract

- Keep credentials in environment variables or the host's secret store.
- Use placeholders such as `API_KEY` or `<PROVIDER>_API_KEY` in documentation.
- Never write a real key into the repository, plugin manifest, novel workspace,
  prompt file, example command, or log.
- Confirm the output path before invoking a paid provider.
- Do not register an image until a non-empty raster file exists and has been
  inspected.

## Connection Options

Choose one provider-neutral connection boundary:

1. Connect an image-generation MCP server to the current agent host.
2. Install a reviewed image-generation CLI and expose it to the agent.
3. Add a small local adapter for the author's chosen API.

Provider-specific endpoints, model names, payloads, and authentication remain
outside the shared skill. The provider's MCP server, CLI, or adapter should
read its own `<PROVIDER>_API_KEY` environment variable.

## Tested CLI Adapter Contract

The bundled `scripts/invoke_image_provider.py` wrapper gives agents a neutral
way to call a reviewed provider command without using a shell string. It sends
one JSON object on standard input:

```json
{
  "prompt": "<complete style-locked prompt>",
  "output": "<temporary absolute output path>",
  "format": "png"
}
```

The provider command must:

1. read that JSON object;
2. obtain its credential from its own environment variable;
3. generate one raster image;
4. write it to the supplied temporary `output` path;
5. exit successfully only after the complete file is present.

Example using placeholders:

```bash
export <PROVIDER>_API_KEY="<API_KEY>"

python scripts/invoke_image_provider.py \
  --prompt-file /path/to/style-locked-prompt.txt \
  --output assets/cover/cover.png \
  -- <provider-cli> generate --request-json-stdin
```

The wrapper does not interpret or print credentials. It validates the returned
PNG, JPEG, or WebP signature and atomically installs the result at the requested
workspace path. Its command, failure, collision, and raster-validation
contracts are covered by local tests using a fake provider; live provider use
still requires the author's chosen connector, account, and cost approval.

## Verification

1. Confirm the command reports the absolute saved path.
2. Inspect the image for style, composition, and continuity.
3. Revise the prompt rather than blindly retrying user-correctable failures.
4. Register the workspace-relative asset path only after approval.

If the author has not chosen or connected a provider, return the complete
style-locked prompt and stop. Do not silently select a commercial provider.
