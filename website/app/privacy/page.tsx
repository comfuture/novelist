import type { Metadata } from "next";

export const metadata: Metadata = { title: "Privacy Policy" };

export default function PrivacyPage() {
  return (
    <main className="legal">
      <a className="back" href="/">← Back to Novelist</a>
      <h1>Privacy Policy</h1>
      <p className="updated">Effective July 17, 2026</p>
      <p>
        Novelist is an open-source, skills-only Codex plugin maintained by
        Changkyun Kim. This policy explains how the plugin and this website
        handle information.
      </p>
      <h2>Plugin data</h2>
      <p>
        The Novelist plugin does not operate an external service, maintain user
        accounts, use analytics, or transmit manuscript content to a server
        controlled by the developer. Its bundled scripts work with files in the
        local project selected by the user. Codex and any model provider may
        process content under their own terms and privacy policies.
      </p>
      <h2>Website data</h2>
      <p>
        This informational website does not use cookies, forms, advertising,
        behavioral analytics, or tracking pixels. The hosting provider may
        process ordinary request data such as IP addresses, user-agent strings,
        and timestamps for security and reliable delivery.
      </p>
      <h2>Contact</h2>
      <p>
        Privacy questions can be sent to <a href="mailto:comfuture@gmail.com">comfuture@gmail.com</a>.
      </p>
    </main>
  );
}
