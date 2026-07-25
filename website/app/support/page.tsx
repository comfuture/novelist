import type { Metadata } from "next";

export const metadata: Metadata = { title: "Support" };

export default function SupportPage() {
  return (
    <main className="legal">
      <a className="back" href="/">← Back to Novelist</a>
      <h1>Support</h1>
      <p className="updated">Help with the Novelist agent-assisted writing plugin</p>
      <h2>Report a problem</h2>
      <p>
        For reproducible bugs, documentation problems, or feature requests,
        open an issue in the <a href="https://github.com/comfuture/novelist/issues">public GitHub repository</a>.
        Please remove private manuscript text, credentials, and personal data
        before posting.
      </p>
      <h2>Contact the developer</h2>
      <p>
        For security or privacy matters that should not be public, email
        <a href="mailto:comfuture@gmail.com"> comfuture@gmail.com</a>.
      </p>
      <h2>Installation</h2>
      <p>Choose the installation path for your agent:</p>
      <pre><code>{`# Codex
codex plugin add novelist@openai-curated-remote

# Claude Code
claude plugin marketplace add comfuture/novelist
claude plugin install novelist@novelist

# Antigravity CLI, from a repository checkout
agy plugin install ./plugins/novelist`}</code></pre>
      <p>
        To use Novelist without installing a plugin, follow the standalone
        scaffold instructions in the <a href="https://github.com/comfuture/novelist/blob/main/MIGRATION.md">migration guide</a>.
      </p>
    </main>
  );
}
