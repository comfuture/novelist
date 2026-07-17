import type { Metadata } from "next";

export const metadata: Metadata = { title: "Support" };

export default function SupportPage() {
  return (
    <main className="legal">
      <a className="back" href="/">← Back to Novelist</a>
      <h1>Support</h1>
      <p className="updated">Help with the Novelist Codex plugin</p>
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
      <p>Add the marketplace and install the plugin:</p>
      <pre><code>{`codex plugin marketplace add comfuture/novelist --ref main
codex plugin add novelist@novelist`}</code></pre>
    </main>
  );
}
