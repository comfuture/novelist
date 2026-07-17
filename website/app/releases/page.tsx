import type { Metadata } from "next";

export const metadata: Metadata = { title: "Release Notes" };

export default function ReleasesPage() {
  return (
    <main className="legal">
      <a className="back" href="/">← Back to Novelist</a>
      <h1>Release Notes</h1>
      <p className="updated">Public release history</p>
      <article>
        <span className="kicker">Initial public submission</span>
        <h2>Novelist 0.1.0</h2>
        <p>
          The first release packages eight Codex workflows for structured
          Markdown novel projects: project initialization, setting, character,
          material and plot development, whole-novel storytelling, visual asset
          creation, and validated EPUB publishing.
        </p>
        <ul>
          <li>Creates a safe, self-contained novel workspace from a reusable scaffold.</li>
          <li>Maintains continuity-aware source files and deterministic chapter checks.</li>
          <li>Publishes only manuscript draft content into a validated EPUB.</li>
          <li>Includes local scripts, templates, and guardrails with no external plugin service.</li>
        </ul>
        <p>
          This is an initial submission. No migration from a previous public
          version is required.
        </p>
        <p>
          Release questions can be sent to <a href="mailto:comfuture@gmail.com">comfuture@gmail.com</a>.
        </p>
      </article>
    </main>
  );
}
