import type { Metadata } from "next";

export const metadata: Metadata = { title: "Release Notes" };

export default function ReleasesPage() {
  return (
    <main className="legal">
      <a className="back" href="/">← Back to Novelist</a>
      <h1>Release Notes</h1>
      <p className="updated">Public release history</p>
      <article>
        <span className="kicker">Current release</span>
        <h2>Novelist 0.2.0 — Analytical Review</h2>
        <p>
          Novelist 0.2.0 expands the plugin to nine skills with independent,
          evidence-backed outline and manuscript critique.
        </p>
        <ul>
          <li>Reviews outlines, chapters, and complete manuscripts without editing source by default.</li>
          <li>Organizes feedback into overall assessment, work examination, and line editing or proofreading.</li>
          <li>Includes the new review skill in eight-skill standalone workspace exports.</li>
          <li>Adds a bounded review, finding-disposition, revision, and regression-review loop only to fully autonomous start-to-publication work.</li>
          <li>Preserves ordinary planning, drafting, revision, and deterministic EPUB publication without silently adding literary review.</li>
        </ul>
      </article>
      <article>
        <span className="kicker">Agent-neutral source release</span>
        <h2>Novelist 0.1.1</h2>
        <p>
          This release makes the plugin payload canonical across Codex, Claude
          Code, and Antigravity CLI while preserving the installed plugin's
          eight-skill writing contract.
        </p>
        <ul>
          <li>Adds thin Claude Code and Antigravity plugin adapters.</li>
          <li>Removes duplicate root scaffold and skill trees.</li>
          <li>Adds safe standalone exports for POSIX, PowerShell, and Command Prompt users.</li>
          <li>Makes visual generation capability-aware and provider-neutral.</li>
          <li>Leads with story assets, continuity, and genre strategy; EPUB remains the final delivery step.</li>
        </ul>
        <p>
          The repository layout is breaking for clone-first scaffold users.
          Installed plugin users keep the same source and skill contracts. Read
          the <a href="https://github.com/comfuture/novelist/blob/main/MIGRATION.md">migration guide</a> before updating an authored clone.
        </p>
      </article>
      <article>
        <span className="kicker">Historical initial public submission</span>
        <h2>Novelist 0.1.0</h2>
        <p>
          The first release packaged eight Codex workflows for structured
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
