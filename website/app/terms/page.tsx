import type { Metadata } from "next";

export const metadata: Metadata = { title: "Terms of Use" };

export default function TermsPage() {
  return (
    <main className="legal">
      <a className="back" href="/">← Back to Novelist</a>
      <h1>Terms of Use</h1>
      <p className="updated">Effective July 17, 2026</p>
      <p>
        Novelist is provided under the MIT License. You may use, copy, modify,
        merge, publish, distribute, sublicense, and sell copies subject to the
        license notice and conditions.
      </p>
      <h2>Your content and decisions</h2>
      <p>
        The developer claims no ownership of manuscripts or other content you
        create with Novelist. You are solely responsible for reviewing outputs,
        confirming factual and legal suitability, preserving backups, and
        deciding whether and how to publish them.
      </p>
      <h2>No warranty</h2>
      <p>
        The software is provided “as is,” without warranty of any kind. To the
        fullest extent permitted by law, the author and copyright holders are
        not liable for claims, damages, or other liability arising from the
        software or its use.
      </p>
      <h2>Third-party services</h2>
      <p>
        Codex, model providers, publishing tools, and hosting services are
        governed by their own terms. You are responsible for complying with
        those terms when using Novelist with them.
      </p>
      <h2>Contact</h2>
      <p>Questions may be sent to <a href="mailto:comfuture@gmail.com">comfuture@gmail.com</a>.</p>
    </main>
  );
}
