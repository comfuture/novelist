const skills = [
  ["Create a novel project", "Start from a structured Markdown workspace."],
  ["Build the world", "Develop settings with reusable, continuity-safe sources."],
  ["Shape characters", "Turn rough briefs into complete character sheets."],
  ["Gather materials", "Capture motifs, research, dialogue, and scene seeds."],
  ["Design the plot", "Build conflicts, reversals, reveals, and payoffs."],
  ["Control the story", "Plan chapters around reader understanding and continuity."],
  ["Create visuals", "Develop cover and illustration assets for the project."],
  ["Publish EPUB", "Package and validate a reader-ready EPUB."],
];

export default function Home() {
  return (
    <main>
      <nav className="nav" aria-label="Primary navigation">
        <a className="brand" href="#top" aria-label="Novelist home">
          <img src="/logo.png" alt="" width="48" height="48" />
          <span>Novelist</span>
        </a>
        <div className="navLinks">
          <a href="#workflows">Workflows</a>
          <a href="#install">Install</a>
          <a href="https://github.com/comfuture/novelist">GitHub</a>
        </div>
      </nav>

      <section className="hero" id="top">
        <div className="eyebrow">A Codex plugin for long-form fiction</div>
        <h1>Keep the whole novel in view.</h1>
        <p className="lede">
          Novelist turns a Markdown workspace into a continuity-safe writing
          system—from first premise to validated EPUB—without taking the story
          away from its author.
        </p>
        <div className="actions">
          <a className="button primary" href="#install">Install Novelist</a>
          <a className="button secondary" href="https://github.com/comfuture/novelist">
            Explore the source
          </a>
        </div>
        <div className="heroMark" aria-hidden="true">
          <img src="/logo.png" alt="" />
        </div>
      </section>

      <section className="manifesto">
        <p>Structure without rigidity.</p>
        <p>Continuity without context overload.</p>
        <p>Publishing without hidden steps.</p>
      </section>

      <section className="section" id="workflows">
        <div className="sectionHeading">
          <span>Eight focused workflows</span>
          <h2>From blank page to finished book.</h2>
        </div>
        <div className="skillGrid">
          {skills.map(([title, description], index) => (
            <article className="skillCard" key={title}>
              <span className="skillNumber">{String(index + 1).padStart(2, "0")}</span>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section install" id="install">
        <div>
          <span className="kicker">Public Git marketplace</span>
          <h2>Install in two commands.</h2>
          <p>
            Add the public Novelist marketplace, install the plugin, then open
            a new Codex task to begin.
          </p>
        </div>
        <pre aria-label="Installation commands"><code>{`codex plugin marketplace add comfuture/novelist --ref main
codex plugin add novelist@novelist`}</code></pre>
      </section>

      <section className="section responsibility">
        <div className="sectionHeading">
          <span>Built for author agency</span>
          <h2>Your story remains yours.</h2>
        </div>
        <p>
          Novelist is open-source software provided under the MIT License. It
          does not claim ownership of work created with it. You remain
          responsible for reviewing, editing, and publishing your output.
        </p>
      </section>

      <footer>
        <div>
          <strong>Novelist</strong>
          <span>Created by Changkyun Kim</span>
        </div>
        <div className="footerLinks">
          <a href="/support">Support</a>
          <a href="/privacy">Privacy</a>
          <a href="/terms">Terms</a>
          <a href="mailto:comfuture@gmail.com">Contact</a>
        </div>
        <p>© 2026 Changkyun Kim. Released under the MIT License.</p>
      </footer>
    </main>
  );
}
