# Claude Code Image Generation

Claude Code can inspect image inputs, but plain installations should not be
treated as having a built-in raster image generator.

Before generating:

1. inspect the tools connected to the current Claude Code session;
2. use a configured image-generation MCP server or external CLI only when its
   output and destination contract are known;
3. keep API keys in environment variables or the host's secret configuration;
4. save and inspect the raster file before registering it in the novel.

If no generator is connected, preserve the complete style-locked prompt and
follow `external-image-provider.md`. Never describe image analysis capability
as image generation.
