# Antigravity CLI Image Generation

Antigravity plugins can provide MCP configuration, but the presence of the
Novelist plugin does not itself prove that a raster image generator is
available.

Before generating:

1. inspect the tools available in the current `agy` session;
2. use a verified built-in or connected image-generation tool only if it can
   return a raster file;
3. otherwise connect an MCP/CLI provider or use the bundled external adapter
   described in `external-image-provider.md`;
4. save and inspect the raster file before registering it in the novel.

Do not infer a tool name or invocation syntax from Codex or Claude Code. If no
provider is available, return the final prompt and connection instructions
without claiming success.
